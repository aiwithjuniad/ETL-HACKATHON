# step_5_sql_aggregated.py

import pyodbc
import pandas as pd

# -----------------------------
# 1. Connect to SQL Server
# -----------------------------
server = r'DESKTOP-8PF23D1'
database = 'BanggoodDB'
driver = 'ODBC Driver 17 for SQL Server'

conn_str = f'DRIVER={{{driver}}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
conn = pyodbc.connect(conn_str)

# -----------------------------
# 2. SQL Queries Execution
# -----------------------------

# 2.1 Average price per category
query_avg_price = """
SELECT main_category, AVG(price_clean) AS avg_price
FROM BanggoodProducts
GROUP BY main_category
ORDER BY avg_price DESC
"""
df_avg_price = pd.read_sql(query_avg_price, conn)
print("Average Price per Category:")
print(df_avg_price)
print("\n--------------------------------------------------\n")

# 2.2 Average rating per category
query_avg_rating = """
SELECT main_category, AVG(rating_clean) AS avg_rating
FROM BanggoodProducts
GROUP BY main_category
ORDER BY avg_rating DESC
"""
df_avg_rating = pd.read_sql(query_avg_rating, conn)
print("Average Rating per Category:")
print(df_avg_rating)
print("\n--------------------------------------------------\n")

# 2.3 Product count per category
query_count_category = """
SELECT main_category, COUNT(*) AS product_count
FROM BanggoodProducts
GROUP BY main_category
ORDER BY product_count DESC
"""
df_count_category = pd.read_sql(query_count_category, conn)
print("Product Count per Category:")
print(df_count_category)
print("\n--------------------------------------------------\n")

# 2.4 Top 5 reviewed items per category
query_top5_reviews = """
WITH Ranked AS (
    SELECT *,
        ROW_NUMBER() OVER (PARTITION BY main_category ORDER BY reviews_clean DESC) AS rn
    FROM BanggoodProducts
)
SELECT main_category, title, price_clean, rating_clean, reviews_clean
FROM Ranked
WHERE rn <= 5
ORDER BY main_category, reviews_clean DESC
"""
df_top5_reviews = pd.read_sql(query_top5_reviews, conn)
print("Top 5 Reviewed Products per Category:")
print(df_top5_reviews)
print("\n--------------------------------------------------\n")

# 2.5 Stock availability percentage
# Assuming there is a column 'stock' (1=in stock, 0=out of stock)
query_stock_percent = """
SELECT main_category,
       SUM(CAST(stock AS FLOAT)) / COUNT(*) * 100 AS stock_percentage
FROM BanggoodProducts
GROUP BY main_category
"""
try:
    df_stock_percent = pd.read_sql(query_stock_percent, conn)
    print("Stock Availability Percentage per Category:")
    print(df_stock_percent)
except:
    print("Column 'stock' not found. Skipping stock availability analysis.")

# -----------------------------
# 3. Close connection
# -----------------------------
conn.close()
