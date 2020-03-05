DROP TABLE IF EXISTS commisions;
DROP TABLE IF EXISTS order_lines;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS product_promotions;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS promotions;

CREATE TABLE commissions (
  date TEXT,
  vendor_id INTEGER NOT NULL,
  rate TEXT REAL NULL
);

CREATE TABLE promotions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  description TEXT
);

CREATE TABLE products (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  description TEXT
);

CREATE TABLE product_promotions (
  date TEXT,
  product_id TEXT NOT NULL,
  promotion_id TEXT NOT NULL
);

CREATE TABLE orders (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at TEXT,
  vendor_id INTEGER NOT NULL,
  customer_id INTEGER NOT NULL
);

CREATE TABLE order_lines (
  order_id INTEGER NOT NULL,
  product_id INTEGER NOT NULL,
  product_description TEXT NOT NULL,
  product_price REAL NOT NULL,
  product_vat_rate REAL NOT NULL,
  discount_rate REAL NOT NULL,
  quantity INTEGER NOT NULL,
  full_price_amount REAL NOT NULL,
  discounted_amount REAL NOT NULL,
  vat_amount REAL NOT NULL,
  total_amount REAL NOT NULL
);
