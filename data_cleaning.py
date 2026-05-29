import pandas as pd
import numpy as np

def load_data(path):
    """Load dataset"""
    return pd.read_csv(path)


def clean_data(df):
    """Clean dataset and prepare for analysis"""

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Handle missing values
    df.fillna({
        "Quantity": df["Quantity"].median(),
        "Unit Price": df["Unit Price"].mean(),
        "Region": "Unknown"
    }, inplace=True)

    # Convert date column
    df["Date"] = pd.to_datetime(df["Date"])

    # Create Month column
    df["Month"] = df["Date"].dt.to_period("M").astype(str)

    # Save cleaned file
    df.to_csv("data/cleaned_sales.csv", index=False)

    return df