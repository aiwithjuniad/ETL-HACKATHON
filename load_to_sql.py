import pandas as pd
import pyodbc

# -----------------------------
# 1️⃣ Load cleaned data
# -----------------------------
CSV_PATH = r"C:\Users\Junaid\Desktop\cde-course\banggood_products.csv"
df = pd.read_csv(CSV_PATH)

# Convert numeric columns properly
numeric_cols = [
    'price', 'rating', 'reviews', 
    'price_clean', 'rating_clean', 'reviews_clean', 
    'price_per_review', 'value_score'
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Fill NaN in boolean columns
df['is_popular'] = df['is_popular'].fillna(False)
df['is_expensive'] = df['is_expensive'].fillna(False)

# -----------------------------
# 2️⃣ Connect to SQL Server
# -----------------------------
server = 'DESKTOP-8PF23D1'
database = 'BanggoodDB'
driver = 'ODBC Driver 17 for SQL Server'

conn_str = f"DRIVER={{{driver}}};SERVER={server};DATABASE=master;Trusted_Connection=yes;"
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# -----------------------------
# 3️⃣ Create database if not exists
# -----------------------------
cursor.execute(f"""
IF DB_ID('{database}') IS NULL
    CREATE DATABASE {database}
""")
conn.commit()

# Switch to the new database
cursor.execute(f"USE {database}")
conn.commit()

# -----------------------------
# 4️⃣ Create table if not exists
# -----------------------------
cursor.execute("""
IF OBJECT_ID('BanggoodProducts', 'U') IS NULL
CREATE TABLE BanggoodProducts (
    id INT IDENTITY(1,1) PRIMARY KEY,
    main_category NVARCHAR(200),
    subcategory NVARCHAR(200),
    title NVARCHAR(500),
    price FLOAT,
    rating FLOAT,
    reviews INT,
    url NVARCHAR(500),
    price_clean FLOAT,
    rating_clean FLOAT,
    reviews_clean INT,
    price_per_review FLOAT,
    value_score FLOAT,
    is_popular BIT,
    is_expensive BIT
)
""")
conn.commit()

# -----------------------------
# 5️⃣ Insert data into SQL Server
# -----------------------------
for index, row in df.iterrows():
    cursor.execute("""
    INSERT INTO BanggoodProducts
    (main_category, subcategory, title, price, rating, reviews, url,
     price_clean, rating_clean, reviews_clean, price_per_review, value_score,
     is_popular, is_expensive)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    row.get('main_category_clean', ''),
    row.get('subcategory_clean', ''),
    row.get('title', ''),
    None if pd.isna(row.get('price')) else float(row.get('price')),
    None if pd.isna(row.get('rating')) else float(row.get('rating')),
    None if pd.isna(row.get('reviews')) else int(row.get('reviews')),
    row.get('url', ''),
    None if pd.isna(row.get('price_clean')) else float(row.get('price_clean')),
    None if pd.isna(row.get('rating_clean')) else float(row.get('rating_clean')),
    None if pd.isna(row.get('reviews_clean')) else int(row.get('reviews_clean')),
    None if pd.isna(row.get('price_per_review')) else float(row.get('price_per_review')),
    None if pd.isna(row.get('value_score')) else float(row.get('value_score')),
    int(row.get('is_popular', False)),
    int(row.get('is_expensive', False))
    )

conn.commit()
print("✅ Data inserted into SQL Server successfully!")

# -----------------------------
# 6️⃣ Optional: check row count
# -----------------------------
cursor.execute("SELECT COUNT(*) FROM BanggoodProducts")
row_count = cursor.fetchone()[0]
print(f"Total rows in BanggoodProducts: {row_count}")

# Close connection
cursor.close()
conn.close()
