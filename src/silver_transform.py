from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

BRONZE_DIR = BASE_DIR / "data" / "bronze"
SILVER_DIR = BASE_DIR / "data" / "silver"
SILVER_DIR.mkdir(parents=True, exist_ok=True)

catalog_path = BRONZE_DIR / "product_catalog" / "data.parquet"
tx_path = BRONZE_DIR / "sample_transactions" / "data.parquet"

df_catalog = pd.read_parquet(catalog_path)
df_tx = pd.read_parquet(tx_path)

df_catalog["unit_price"] = pd.to_numeric(df_catalog["unit_price"], errors="coerce")

df_tx["quantity"] = pd.to_numeric(df_tx["quantity"], errors="coerce").astype("Int64")
df_tx["unit_price"] = pd.to_numeric(df_tx["unit_price"], errors="coerce")
df_tx["amount"] = pd.to_numeric(df_tx["amount"], errors="coerce")

df_tx["tx_ts"] = pd.to_datetime(df_tx["tx_ts"], errors="coerce")

df_tx = df_tx.dropna(subset=["tx_id", "customer_id", "tx_ts", "product_id", "quantity", "unit_price"])
df_tx = df_tx[df_tx["quantity"] > 0]
df_tx = df_tx[df_tx["unit_price"] >= 0]

df_tx = df_tx.merge(df_catalog, on="product_id", how="left", suffixes=("", "_catalog"))

df_tx["unit_price_final"] = df_tx["unit_price_catalog"].fillna(df_tx["unit_price"])

df_tx["amount_final"] = (df_tx["unit_price_final"] * df_tx["quantity"]).round(2)

df_tx = df_tx.drop_duplicates(subset=["tx_id"])

df_tx_clean = df_tx[[
    "tx_id",
    "customer_id",
    "tx_ts",
    "product_id",
    "quantity",
    "unit_price_final",
    "amount_final"
]].rename(columns={
    "unit_price_final": "unit_price",
    "amount_final": "amount"
})

catalog_out = SILVER_DIR / "product_catalog_clean"
tx_out = SILVER_DIR / "transactions_clean"
catalog_out.mkdir(exist_ok=True)
tx_out.mkdir(exist_ok=True)

df_catalog.to_parquet(catalog_out / "data.parquet", index=False)
df_tx_clean.to_parquet(tx_out / "data.parquet", index=False)

print("SILVER concluída: product_catalog_clean e transactions_clean salvos em data/silver/")
print("Linhas transações (antes):", len(pd.read_parquet(tx_path)))
print("Linhas transações (depois):", len(df_tx_clean))
