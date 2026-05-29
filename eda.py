import pandas as pd
import numpy as np

# Summary statistics
def summary_stats(df):
    return df.describe()


# Correlation matrix
def correlation(df):
    return df.corr(numeric_only=True)


# Monthly trend
def monthly_trend(df):
    return df.groupby("Month")["Total Sales"].sum().reset_index()


# Sales by category
def sales_by_category(df):
    return df.groupby("Category")["Total Sales"].sum().reset_index()


# Sales by region
def sales_by_region(df):
    return df.groupby("Region")["Total Sales"].sum().reset_index()


# Top products
def top_products(df):
    return (
        df.groupby("Product")["Total Sales"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )


# Business KPIs
def key_metrics(df):
    return {
        "Total Revenue": np.sum(df["Total Sales"]),
        "Total Orders": df["Order ID"].nunique(),
        "Avg Order Value": np.mean(df["Total Sales"]),
        "Top Product": df.groupby("Product")["Total Sales"].sum().idxmax()
    }