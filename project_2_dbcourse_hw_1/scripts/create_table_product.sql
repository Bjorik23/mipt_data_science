CREATE TABLE product (
    product_id SERIAL PRIMARY KEY,
    brand VARCHAR(255),
    product_line VARCHAR(255),
    product_class VARCHAR(255),
    product_size VARCHAR(255),
    list_price NUMERIC(10, 2)
);