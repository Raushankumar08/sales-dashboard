import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
import os

fake = Faker()

# Create data folder if not exists
os.makedirs("data", exist_ok=True)

products = [
    "Laptop", "Smartphone", "Tablet", "Headphones", "Smartwatch",
    "Camera", "Printer", "Keyboard", "Mouse", "Monitor"
]

categories = {
    "Laptop": "Electronics",
    "Smartphone": "Electronics",
    "Tablet": "Electronics",
    "Headphones": "Accessories",
    "Smartwatch": "Accessories",
    "Camera": "Electronics",
    "Printer": "Office",
    "Keyboard": "Accessories",
    "Mouse": "Accessories",
    "Monitor": "Electronics"
}

regions = ["North", "South", "East", "West"]

data = []
start_date = datetime(2023, 1, 1)

for i in range(1, 501):
    product = random.choice(products)
    quantity = random.randint(1, 10)
    unit_price = round(random.uniform(100, 2000), 2)

    row = {
        "Order ID": f"ORD{i:04d}",
        "Date": start_date + timedelta(days=random.randint(0, 365)),
        "Product": product,
        "Category": categories[product],
        "Quantity": quantity,
        "Unit Price": unit_price,
        "Total Sales": round(quantity * unit_price, 2),
        "Region": random.choice(regions),
        "Customer Name": fake.name()
    }

    data.append(row)

df = pd.DataFrame(data)

df.to_csv("data/retail_sales.csv", index=False)

print("✅ Dataset created in data/retail_sales.csv")