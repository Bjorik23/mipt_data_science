CREATE TABLE "customer" (
  "customer_id" integer PRIMARY KEY,
  "first_name" varchar,
  "last_name" varchar,
  "gender" varchar,
  "DOB" timestamp,
  "job_title" varchar,
  "job_industry_category" varchar,
  "wealth_segment" varchar,
  "deceased_indicator" varchar,
  "owns_car" varchar,
  "address" varchar,
  "postcode" integer,
  "property_valuation" integer
);

CREATE TABLE "location" (
  "postcode" integer PRIMARY KEY,
  "state" varchar,
  "country" varchar
);

CREATE TABLE "product" (
  "product_id" integer PRIMARY KEY,
  "brand" varchar,
  "product_line" varchar,
  "product_class" varchar,
  "product_size" varchar,
  "list_price" float
);

CREATE TABLE "transaction" (
  "transaction_id" integer PRIMARY KEY,
  "product_id" integer,
  "customer_id" integer,
  "transaction_date" timestamp,
  "online_order" varchar,
  "order_status" varchar,
  "standard_cost" float
);

ALTER TABLE "customer" ADD FOREIGN KEY ("postcode") REFERENCES "location" ("postcode");

ALTER TABLE "transaction" ADD FOREIGN KEY ("product_id") REFERENCES "product" ("product_id");

ALTER TABLE "transaction" ADD FOREIGN KEY ("customer_id") REFERENCES "customer" ("customer_id");
