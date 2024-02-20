CREATE TABLE IF NOT EXISTS customer (
    customer_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    gender VARCHAR(10),
    DOB DATE,
    job_title VARCHAR(100),
    job_industry_category VARCHAR(100),
    wealth_segment VARCHAR(50),
    deceased_indicator CHAR(1),
    owns_car BOOLEAN,
    address VARCHAR(255),
    postcode INT,
    state VARCHAR(100),
    country VARCHAR(100),
    property_valuation INT
);