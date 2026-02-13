import uuid
import random
from datetime import datetime, timedelta
import csv
from pathlib import Path

n_customers = 500
n_tx = 5000
num_products = 200

start_date = datetime.now() - timedelta(days=365)

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

product_ids = [f"prod_{i}" for i in range(1, num_products + 1)]
product_prices = {
    pid: round(random.uniform(5.0, 200.0), 2)
    for pid in product_ids
}

catalog_path = RAW_DIR / "product_catalog.csv"
with open(catalog_path, "w", newline="", encoding="utf-8") as cf:
    w = csv.writer(cf)
    w.writerow(["product_id", "unit_price"])
    for pid, price in product_prices.items():
        w.writerow([pid, price])

tx_path = RAW_DIR / "sample_transactions.csv"
with open(tx_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "tx_id",
        "customer_id",
        "tx_ts",
        "amount",
        "product_id",
        "quantity",
        "unit_price"
    ])

    for _ in range(n_tx):
        tx_id = str(uuid.uuid4())
        customer_id = f"cust_{random.randint(1, n_customers)}"

        tx_ts = (
            start_date
            + timedelta(
                days=random.randint(0, 365),
                seconds=random.randint(0, 86400)
            )
        ).isoformat()

        product_id = random.choice(product_ids)
        quantity = random.randint(1, 3)
        unit_price = product_prices[product_id]
        amount = round(unit_price * quantity, 2)

        writer.writerow([
            tx_id,
            customer_id,
            tx_ts,
            amount,
            product_id,
            quantity,
            unit_price
        ])

print("Dados sintéticos gerados com sucesso em data/raw/")
print("BASE_DIR =", BASE_DIR)
