from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent


RAW_DIR = BASE_DIR / "data" / "raw"
BRONZE_DIR = BASE_DIR / "data" / "bronze"


BRONZE_DIR.mkdir(parents=True, exist_ok=True)


csv_files = list(RAW_DIR.glob("*.csv"))


if not csv_files:
    raise RuntimeError("Nenhum arquivo CSV encontrado em data/raw")

for csv_path in csv_files:
    print(f"Ingerindo {csv_path.name}")


    df = pd.read_csv(csv_path)


    table_name = csv_path.stem


    output_path = BRONZE_DIR / table_name
    output_path.mkdir(exist_ok=True)


    df.to_parquet(output_path / "data.parquet", index=False)

print("Ingestão BRONZE concluída com sucesso.")
