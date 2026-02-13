from pathlib import Path
import pandas as pd

# 1) Caminhos base
BASE_DIR = Path(__file__).resolve().parent.parent

BRONZE_DIR = BASE_DIR / "data" / "bronze"
SILVER_DIR = BASE_DIR / "data" / "silver"
SILVER_DIR.mkdir(parents=True, exist_ok=True)

# 2) Ler Parquet da Bronze
catalog_path = BRONZE_DIR / "product_catalog" / "data.parquet"
tx_path = BRONZE_DIR / "sample_transactions" / "data.parquet"

df_catalog = pd.read_parquet(catalog_path)
df_tx = pd.read_parquet(tx_path)

# 3) Tipagem e padronização (SILVER)
# 3.1) Catalog: garantir unit_price numérico
df_catalog["unit_price"] = pd.to_numeric(df_catalog["unit_price"], errors="coerce")

# 3.2) Transactions: tipar colunas
df_tx["quantity"] = pd.to_numeric(df_tx["quantity"], errors="coerce").astype("Int64")
df_tx["unit_price"] = pd.to_numeric(df_tx["unit_price"], errors="coerce")
df_tx["amount"] = pd.to_numeric(df_tx["amount"], errors="coerce")

# 3.3) Converter tx_ts para datetime
df_tx["tx_ts"] = pd.to_datetime(df_tx["tx_ts"], errors="coerce")

# 4) Regras de qualidade básicas
# Remove linhas inválidas
df_tx = df_tx.dropna(subset=["tx_id", "customer_id", "tx_ts", "product_id", "quantity", "unit_price"])
df_tx = df_tx[df_tx["quantity"] > 0]
df_tx = df_tx[df_tx["unit_price"] >= 0]

# 5) Join com catálogo para garantir preço oficial
df_tx = df_tx.merge(df_catalog, on="product_id", how="left", suffixes=("", "_catalog"))

# Se existir unit_price_catalog, usamos ele como "fonte de verdade"
df_tx["unit_price_final"] = df_tx["unit_price_catalog"].fillna(df_tx["unit_price"])

# 6) Recalcular amount como fonte de verdade
df_tx["amount_final"] = (df_tx["unit_price_final"] * df_tx["quantity"]).round(2)

# 7) Remover duplicatas por tx_id (se acontecer)
df_tx = df_tx.drop_duplicates(subset=["tx_id"])

# 8) Selecionar colunas finais (organização)
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

# 9) Salvar SILVER
catalog_out = SILVER_DIR / "product_catalog_clean"
tx_out = SILVER_DIR / "transactions_clean"
catalog_out.mkdir(exist_ok=True)
tx_out.mkdir(exist_ok=True)

df_catalog.to_parquet(catalog_out / "data.parquet", index=False)
df_tx_clean.to_parquet(tx_out / "data.parquet", index=False)

print("SILVER concluída: product_catalog_clean e transactions_clean salvos em data/silver/")
print("Linhas transações (antes):", len(pd.read_parquet(tx_path)))
print("Linhas transações (depois):", len(df_tx_clean))
