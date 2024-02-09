CREATE TABLE customer (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    gender VARCHAR(50),
    DOB DATE,
    job_title VARCHAR(255),
    job_industry_category VARCHAR(255),
    wealth_segment VARCHAR(255),
    deceased_indicator CHAR(1),
    owns_car VARCHAR(50),
    address VARCHAR(255),
    postcode INTEGER,
    property_valuation INTEGER,
    FOREIGN KEY (postcode) REFERENCES location(postcode)
);