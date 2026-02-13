from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

SILVER_DIR = BASE_DIR / "data" / "silver"
GOLD_DIR = BASE_DIR / "data" / "gold"
GOLD_DIR.mkdir(parents=True, exist_ok=True)

tx_path = SILVER_DIR / "transactions_clean" / "data.parquet"

df_tx = pd.read_parquet(tx_path)

df_tx["tx_ts"] = pd.to_datetime(df_tx["tx_ts"], errors="coerce")

# Defino a data de referência para cálculo do Recency
# Aqui uso a data atual para refletir um cenário mais realista
ref_date = pd.Timestamp.today().normalize()

# Agrego os dados por cliente para calcular as métricas RFM básicas
df_rfm = (
    df_tx.groupby("customer_id")
    .agg(
        last_purchase=("tx_ts", "max"),   
        frequency=("tx_id", "count"),    
        monetary=("amount", "sum")       
    )
    .reset_index()
)

# Calculo o Recency em dias (quantos dias desde a última compra)
df_rfm["recency"] = (ref_date - df_rfm["last_purchase"]).dt.days

# Arredondo o valor monetário para duas casas decimais
df_rfm["monetary"] = df_rfm["monetary"].round(2)

# Transformo as métricas contínuas em notas de 1 a 5

# Para Recency, quanto menor o valor, melhor o cliente
df_rfm["R_score"] = pd.qcut(
    df_rfm["recency"],
    q=5,
    labels=[5, 4, 3, 2, 1]
)

# Para Frequency, quanto maior, melhor
df_rfm["F_score"] = pd.qcut(
    df_rfm["frequency"].rank(method="first"),
    q=5,
    labels=[1, 2, 3, 4, 5]
)

# Para Monetary, quanto maior o gasto, melhor
df_rfm["M_score"] = pd.qcut(
    df_rfm["monetary"].rank(method="first"),
    q=5,
    labels=[1, 2, 3, 4, 5]
)

# Garanto que os scores fiquem como inteiros
df_rfm[["R_score", "F_score", "M_score"]] = df_rfm[
    ["R_score", "F_score", "M_score"]
].astype(int)

# Classifico os clientes em segmentos de negócio com base no RFM Score

def rfm_segment(row):
    if row["R_score"] >= 4 and row["F_score"] >= 4 and row["M_score"] >= 4:
        return "Campeões"
    elif row["F_score"] >= 4 and row["M_score"] >= 3:
        return "Leais"
    elif row["R_score"] >= 4 and row["F_score"] <= 3:
        return "Potenciais"
    elif row["R_score"] <= 2 and row["F_score"] >= 3:
        return "Em risco"
    else:
        return "Perdidos"

df_rfm["segment"] = df_rfm.apply(rfm_segment, axis=1)

df_rfm["Soma_clientes"] = 1

# Seleciono e organizo as colunas finais da tabela Gold RFM
df_rfm = df_rfm[
    [
        "customer_id",
        "recency",
        "frequency",
        "monetary",
        "R_score",
        "F_score",
        "M_score",
        "segment",
        "Soma_clientes",
        "last_purchase"
    ]
]

out_dir = GOLD_DIR / "rfm_customer"
out_dir.mkdir(exist_ok=True)

df_rfm.to_parquet(out_dir / "data.parquet", index=False)

print("GOLD RFM concluída e salva em data/gold/rfm_customer/data.parquet")
print("Data de referência utilizada:", ref_date)
print("Total de clientes:", len(df_rfm))
print(
    df_rfm.sort_values(
        ["recency", "frequency", "monetary"],
        ascending=[True, False, False]
    ).head(10)
)
