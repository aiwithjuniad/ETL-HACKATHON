import pandas as pd

# df = pd.read_csv(r"C:\Users\Junaid\Desktop\cde-course\banggood_products.csv")
# df["main_category"] = df["main_category"].replace({
#     "https://www.banggood.com/Wholesale-Lights-and-Lighting-ca-14001.html?bid=210710&from=nav": "Lights-and-Lighting",
#     "https://www.banggood.com/Wholesale-Men-and-Womens-Clothing-ca-18941.html?bid=210711&from=nav": "Men-and-Womens-Clothing",
#     "https://www.banggood.com/Wholesale-Automobiles-and-Motorcycles-ca-4001.html?bid=210704&from=nav": "Automobiles-and-Motorcycles",
#     "https://www.banggood.com/Wholesale-Sports-and-Outdoors-ca-6001.html?bid=210702&from=nav": "Sports-and-Outdoors",
#     "https://www.banggood.com/Wholesale-Computers-and-Office-ca-5001.html?bid=210707&from=nav": "Computers-and-Office"
# })
# df.to_csv("banggood_products.csv")
# print(df.head(50))
# print(df.sample(30))

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load cleaned data
df = pd.read_csv(r"C:\Users\Junaid\Desktop\cde-course\banggood_products.csv")

# -----------------------------
# 1. Price distribution per category
# -----------------------------
plt.figure(figsize=(12,6))
sns.boxplot(x="main_category_clean", y="price_clean", data=df)
plt.xticks(rotation=45, ha='right')
plt.title("Price Distribution per Main Category")
plt.ylabel("Price (£)")
plt.xlabel("Main Category")
plt.tight_layout()
plt.show()

# -----------------------------
# 2. Rating vs Price correlation
# -----------------------------
plt.figure(figsize=(10,6))
sns.scatterplot(x="price_clean", y="rating_clean", hue="main_category_clean", data=df)
plt.title("Rating vs Price Scatter Plot")
plt.xlabel("Price (£)")
plt.ylabel("Rating")
plt.legend(bbox_to_anchor=(1.05,1), loc='upper left')
plt.tight_layout()
plt.show()

print("Correlation between Price and Rating:")
print(df[['price_clean','rating_clean']].corr())

# -----------------------------
# 3. Top reviewed products
# -----------------------------
top_reviewed = df.sort_values("reviews_clean", ascending=False).head(10)
plt.figure(figsize=(12,6))
sns.barplot(x="reviews_clean", y="title", data=top_reviewed)
plt.title("Top 10 Most Reviewed Products")
plt.xlabel("Number of Reviews")
plt.ylabel("Product Title")
plt.tight_layout()
plt.show()

# -----------------------------
# 4. Best value metric per category
# Value = rating / price
# -----------------------------
best_value = df.loc[df.groupby("main_category_clean")["value_score"].idxmax()]
plt.figure(figsize=(12,6))
sns.barplot(x="main_category_clean", y="value_score", data=best_value)
plt.title("Best Value Product per Category (Rating / Price)")
plt.xlabel("Main Category")
plt.ylabel("Value Score")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

print("\nBest Value Products per Category:")
print(best_value[['main_category_clean','title','price_clean','rating_clean','value_score']])

# -----------------------------
# 5. Stock availability analysis (simulated)
# We'll assume products with price < median are "available" for demo
# -----------------------------
price_median = df['price_clean'].median()
df['is_available'] = df['price_clean'] <= price_median

availability_counts = df.groupby('main_category_clean')['is_available'].mean().reset_index()
availability_counts['availability_percent'] = availability_counts['is_available'] * 100

plt.figure(figsize=(12,6))
sns.barplot(x='main_category_clean', y='availability_percent', data=availability_counts)
plt.title("Stock Availability Percentage per Category (Simulated)")
plt.ylabel("Availability (%)")
plt.xlabel("Main Category")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

print("\nStock Availability Percentage per Category (Simulated):")
print(availability_counts[['main_category_clean','availability_percent']])
