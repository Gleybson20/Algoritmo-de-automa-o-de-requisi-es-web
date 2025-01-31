CREATE DATABASE IF NOT EXISTS ads_database;
USE ads_database;

CREATE TABLE IF NOT EXISTS ads_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    adset_id VARCHAR(255),
    adset_name VARCHAR(255),
    date_start DATE,
    date_stop DATE,
    impressions INT,
    reach INT,
    spend FLOAT,
    action_type VARCHAR(255),
    value INT,
    clicks INT,
    engagements INT,
    leads INT,
    messaging_conversation_started INT,
    custom_conversion INT,
    CTR FLOAT,
    CPL FLOAT,
    ROI FLOAT,
    CPC FLOAT,
    CPA FLOAT,
    CR FLOAT,
    cost_per_messaging_conversation_started FLOAT,
    cost_per_custom_conversion FLOAT
);
