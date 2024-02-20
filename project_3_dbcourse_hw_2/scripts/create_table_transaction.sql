CREATE TABLE IF NOT EXISTS transaction (
    transaction_id INT PRIMARY KEY,
    product_id INT,
    customer_id INT,
    transaction_date DATE,
    online_order BOOLEAN,
    order_status VARCHAR(50),
    brand VARCHAR(50),
    product_line VARCHAR(50),
    product_class VARCHAR(50),
    product_size VARCHAR(50),
    list_price DECIMAL(10, 2),
    standard_cost DECIMAL(10, 2),
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
);