CREATE TABLE shop_category (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT NOT NULL DEFAULT '',
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE shop_brand (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    country VARCHAR(100) NOT NULL DEFAULT '',
    website VARCHAR(200) NOT NULL DEFAULT '',
    description TEXT NOT NULL DEFAULT '',
    logo VARCHAR(100)
);

CREATE TABLE shop_supplier (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    contact_person VARCHAR(120) NOT NULL DEFAULT '',
    phone VARCHAR(30) NOT NULL,
    email VARCHAR(254) NOT NULL,
    address VARCHAR(255) NOT NULL DEFAULT ''
);

CREATE TABLE shop_customer (
    id BIGSERIAL PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    phone VARCHAR(30) NOT NULL,
    email VARCHAR(254) NOT NULL UNIQUE,
    address VARCHAR(255) NOT NULL DEFAULT '',
    registered_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE shop_product (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    category_id BIGINT NOT NULL REFERENCES shop_category(id) ON DELETE RESTRICT,
    brand_id BIGINT NOT NULL REFERENCES shop_brand(id) ON DELETE RESTRICT,
    supplier_id BIGINT REFERENCES shop_supplier(id) ON DELETE SET NULL,
    price NUMERIC(10,2) NOT NULL CHECK (price >= 0),
    stock INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0),
    description TEXT NOT NULL DEFAULT '',
    image VARCHAR(100),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE shop_order (
    id BIGSERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES auth_user(id) ON DELETE SET NULL,
    customer_id BIGINT NOT NULL REFERENCES shop_customer(id) ON DELETE RESTRICT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) NOT NULL DEFAULT 'new',
    total_amount NUMERIC(12,2) NOT NULL DEFAULT 0 CHECK (total_amount >= 0),
    delivery_address VARCHAR(255) NOT NULL DEFAULT '',
    delivery_type VARCHAR(20) NOT NULL DEFAULT 'pickup',
    comment TEXT NOT NULL DEFAULT ''
);

CREATE TABLE shop_orderitem (
    id BIGSERIAL PRIMARY KEY,
    order_id BIGINT NOT NULL REFERENCES shop_order(id) ON DELETE CASCADE,
    product_id BIGINT NOT NULL REFERENCES shop_product(id) ON DELETE RESTRICT,
    quantity INTEGER NOT NULL DEFAULT 1 CHECK (quantity >= 1),
    price NUMERIC(10,2) NOT NULL CHECK (price >= 0)
);

CREATE TABLE shop_review (
    id BIGSERIAL PRIMARY KEY,
    product_id BIGINT NOT NULL REFERENCES shop_product(id) ON DELETE CASCADE,
    customer_id BIGINT NOT NULL REFERENCES shop_customer(id) ON DELETE CASCADE,
    rating SMALLINT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    text TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_product_customer_review UNIQUE (product_id, customer_id)
);

CREATE INDEX shop_product_category_idx ON shop_product(category_id);
CREATE INDEX shop_product_brand_idx ON shop_product(brand_id);
CREATE INDEX shop_product_supplier_idx ON shop_product(supplier_id);
CREATE INDEX shop_order_user_idx ON shop_order(user_id);
CREATE INDEX shop_order_customer_idx ON shop_order(customer_id);
CREATE INDEX shop_orderitem_order_idx ON shop_orderitem(order_id);
CREATE INDEX shop_orderitem_product_idx ON shop_orderitem(product_id);
CREATE INDEX shop_review_product_idx ON shop_review(product_id);
CREATE INDEX shop_review_customer_idx ON shop_review(customer_id);
