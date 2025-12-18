CREATE TABLE IF NOT EXISTS categories (
  id SERIAL PRIMARY KEY,
  name VARCHAR(200) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS products (
  id SERIAL PRIMARY KEY,
  sku VARCHAR(64) NOT NULL UNIQUE,
  name VARCHAR(255) NOT NULL,
  description TEXT NULL,
  price_cents INTEGER NOT NULL,
  category_id INTEGER NULL REFERENCES categories(id)
);

CREATE INDEX IF NOT EXISTS ix_products_category_id ON products(category_id);
