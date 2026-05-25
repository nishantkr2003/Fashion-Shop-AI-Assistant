"""
Seed script — loads products.csv into the Neon PostgreSQL database.

Usage:
    pip install psycopg2-binary python-dotenv
    python seed.py

Place this file in the backend/ folder alongside your .env file.
"""

import csv
import os
import sys
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import execute_batch

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("❌  DATABASE_URL not found in .env — please set it and try again.")
    sys.exit(1)

CSV_PATH = os.path.join(os.path.dirname(__file__), "products.csv")
if not os.path.exists(CSV_PATH):
    print(f"❌  products.csv not found at {CSV_PATH}")
    print("    Place products.csv in the same folder as seed.py and retry.")
    sys.exit(1)


CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS products (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(500),
    brand       VARCHAR(255),
    category    VARCHAR(255),
    color       VARCHAR(255),
    size        VARCHAR(100),
    price       FLOAT,
    rating      FLOAT,
    stock       INTEGER,
    description TEXT,
    image_url   TEXT
);
"""

INSERT_SQL = """
INSERT INTO products (name, brand, category, color, size, price, rating, stock, description, image_url)
VALUES (%(name)s, %(brand)s, %(category)s, %(color)s, %(size)s, %(price)s, %(rating)s, %(stock)s, %(description)s, %(image_url)s)
ON CONFLICT DO NOTHING;
"""


def parse_float(val):
    try:
        return float(val) if val.strip() else None
    except ValueError:
        return None


def parse_int(val):
    try:
        return int(val) if val.strip() else None
    except ValueError:
        return None


MIGRATE_COLUMNS = [
    ("size",        "VARCHAR(100)"),
    ("rating",      "FLOAT"),
    ("description", "TEXT"),
    ("image_url",   "TEXT"),
]


def migrate_table(cur, conn):
    """Add any missing columns to an existing products table."""
    cur.execute("""
        SELECT column_name FROM information_schema.columns
        WHERE table_name = 'products';
    """)
    existing = {row[0] for row in cur.fetchall()}

    added = []
    for col_name, col_type in MIGRATE_COLUMNS:
        if col_name not in existing:
            cur.execute(f'ALTER TABLE products ADD COLUMN "{col_name}" {col_type};')
            added.append(col_name)

    if added:
        conn.commit()
        print(f"🔧  Added missing columns: {', '.join(added)}")
    else:
        print("✔️   Table schema is up to date.")


def main():
    print(f"🔌  Connecting to database…")
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    print("📦  Creating products table if it doesn't exist…")
    cur.execute(CREATE_TABLE)
    conn.commit()

    print("🔍  Checking for missing columns…")
    migrate_table(cur, conn)

    print(f"📂  Reading {CSV_PATH}…")
    rows = []
    with open(CSV_PATH, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({
                "name":        row.get("name", "").strip(),
                "brand":       row.get("brand", "").strip(),
                "category":    row.get("category", "").strip(),
                "color":       row.get("color", "").strip(),
                "size":        row.get("size", "").strip(),
                "price":       parse_float(row.get("price", "")),
                "rating":      parse_float(row.get("rating", "")),
                "stock":       parse_int(row.get("stock", "")),
                "description": row.get("description", "").strip(),
                "image_url":   row.get("image_url", "").strip(),
            })

    print(f"⬆️   Inserting {len(rows)} products…")
    execute_batch(cur, INSERT_SQL, rows, page_size=100)
    conn.commit()

    cur.execute("SELECT COUNT(*) FROM products;")
    total = cur.fetchone()[0]

    cur.close()
    conn.close()

    print(f"✅  Done! Total rows in products table: {total}")


if __name__ == "__main__":
    main()