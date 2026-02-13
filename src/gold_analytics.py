from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

SILVER_DIR = BASE_DIR / "data" / "silver"
GOLD_DIR = BASE_DIR / "data" / "gold"
GOLD_DIR.mkdir(parents=True, exist_ok=True)


tx_path = SILVER_DIR / "transactions_clean" / "data.parquet"
df_tx = pd.read_parquet(tx_path)

# Agregações por cliente
df_gold = (
    df_tx
    .groupby("customer_id")
    .agg(
        total_gasto=("amount", "sum"),
        ticket_medio=("amount", "mean"),
        num_compras=("tx_id", "count"),
        ultima_compra=("tx_ts", "max")
    )
    .reset_index()
)

df_gold["total_gasto"] = df_gold["total_gasto"].round(2)
df_gold["ticket_medio"] = df_gold["ticket_medio"].round(2)

output_path = GOLD_DIR / "customer_metrics"
output_path.mkdir(exist_ok=True)

df_gold.to_parquet(output_path / "data.parquet", index=False)

print("GOLD concluída: métricas por cliente salvas em data/gold/")
print("Total de clientes:", len(df_gold))
