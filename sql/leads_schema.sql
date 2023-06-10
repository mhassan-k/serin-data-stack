CREATE DATABASE lead_data_analytics;
CREATE TABLE IF NOT EXISTS leads_parquet
(
    "lead_UUID" TEXT NOT NULL,
    "phone_hash" TEXT NOT NULL,
    "email_hash" TEXT DEFAULT NULL,
    "index" INT DEFAULT NULL
);
