import pandas as pd
import re

# 1. Load scraped data
df = pd.read_csv("banggood_products.csv")   # adjust path if needed


# --- Helper function to clean price ---
def clean_price(value):
    if pd.isna(value):
        return None
    match = re.search(r"[\d\.]+", str(value))
    return float(match.group()) if match else None


# 2. Cleaning price, ratings, review counts
df["price_clean"] = df["price"].apply(clean_price)

df["rating_clean"] = pd.to_numeric(df["rating"], errors="coerce")

df["reviews_clean"] = (
    df["reviews"]
    .astype(str)
    .str.extract(r"(\d+)")
    .astype(float)
)

# Handle missing values
df["rating_clean"].fillna(df["rating_clean"].median(), inplace=True)
df["reviews_clean"].fillna(0, inplace=True)


# 3. Derived Features
# Derived Feature 1: Price per review
df["price_per_review"] = df["price_clean"] / (df["reviews_clean"] + 1)

# Derived Feature 2: Value score (rating normalized by price)
df["value_score"] = df["rating_clean"] / df["price_clean"]


# --- Optional: print verification ---
print(df.head())
print("\nColumns Available:", df.columns.tolist())