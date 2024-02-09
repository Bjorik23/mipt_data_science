CREATE TABLE transaction (
    transaction_id SERIAL PRIMARY KEY,
    product_id INTEGER,
    customer_id INTEGER,
    transaction_date DATE,
    online_order BOOLEAN,
    order_status VARCHAR(255),
    standard_cost NUMERIC(10, 2),
    FOREIGN KEY (product_id) REFERENCES product(product_id),
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
);