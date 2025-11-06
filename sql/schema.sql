-- AgriData Explorer Database Schema
-- File: sql/schema.sql

-- Create Database
CREATE DATABASE IF NOT EXISTS agridata_db;
USE agridata_db;

-- Drop existing tables (for clean setup)
DROP TABLE IF EXISTS fact_production;
DROP TABLE IF EXISTS dim_district;
DROP TABLE IF EXISTS dim_state;
DROP TABLE IF EXISTS dim_year;

-- ============================================================================
-- DIMENSION TABLES
-- ============================================================================

-- State Dimension
CREATE TABLE dim_state (
    state_id INT PRIMARY KEY AUTO_INCREMENT,
    state_code VARCHAR(10) UNIQUE,
    state_name VARCHAR(100) NOT NULL,
    region VARCHAR(50) COMMENT 'North, South, East, West, Central',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_state_name (state_name),
    INDEX idx_state_code (state_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- District Dimension
CREATE TABLE dim_district (
    district_id INT PRIMARY KEY AUTO_INCREMENT,
    district_code VARCHAR(20),
    district_name VARCHAR(100) NOT NULL,
    state_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (state_id) REFERENCES dim_state(state_id),
    INDEX idx_district_name (district_name),
    INDEX idx_state_id (state_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Year Dimension
CREATE TABLE dim_year (
    year_id INT PRIMARY KEY,
    decade INT NOT NULL,
    is_recent BOOLEAN DEFAULT FALSE COMMENT 'Year >= 2015',
    season_type VARCHAR(20) COMMENT 'Kharif, Rabi, Zaid',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_decade (decade),
    INDEX idx_is_recent (is_recent)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================================
-- FACT TABLE
-- ============================================================================

CREATE TABLE fact_production (
    production_id INT PRIMARY KEY AUTO_INCREMENT,
    district_id INT NOT NULL,
    year_id INT NOT NULL,
    
    -- Rice
    rice_area DECIMAL(12,2) DEFAULT 0.00 COMMENT 'in 1000 hectares',
    rice_production DECIMAL(12,2) DEFAULT 0.00 COMMENT 'in 1000 tons',
    rice_yield DECIMAL(12,2) DEFAULT 0.00 COMMENT 'in kg per hectare',
    
    -- Wheat
    wheat_area DECIMAL(12,2) DEFAULT 0.00,
    wheat_production DECIMAL(12,2) DEFAULT 0.00,
    wheat_yield DECIMAL(12,2) DEFAULT 0.00,
    
    -- Maize
    maize_area DECIMAL(12,2) DEFAULT 0.00,
    maize_production DECIMAL(12,2) DEFAULT 0.00,
    maize_yield DECIMAL(12,2) DEFAULT 0.00,
    
    -- Sorghum (Jowar)
    sorghum_area DECIMAL(12,2) DEFAULT 0.00,
    sorghum_production DECIMAL(12,2) DEFAULT 0.00,
    sorghum_yield DECIMAL(12,2) DEFAULT 0.00,
    
    -- Pearl Millet (Bajra)
    pearl_millet_area DECIMAL(12,2) DEFAULT 0.00,
    pearl_millet_production DECIMAL(12,2) DEFAULT 0.00,
    pearl_millet_yield DECIMAL(12,2) DEFAULT 0.00,
    
    -- Finger Millet (Ragi)
    finger_millet_area DECIMAL(12,2) DEFAULT 0.00,
    finger_millet_production DECIMAL(12,2) DEFAULT 0.00,
    finger_millet_yield DECIMAL(12,2) DEFAULT 0.00,
    
    -- Barley
    barley_area DECIMAL(12,2) DEFAULT 0.00,
    barley_production DECIMAL(12,2) DEFAULT 0.00,
    barley_yield DECIMAL(12,2) DEFAULT 0.00,
    
    -- Chickpea (Gram)
    chickpea_area DECIMAL(12,2) DEFAULT 0.00,
    chickpea_production DECIMAL(12,2) DEFAULT 0.00,
    chickpea_yield DECIMAL(12,2) DEFAULT 0.00,
    
    -- Pigeonpea (Arhar/Tur)
    pigeonpea_area DECIMAL(12,2) DEFAULT 0.00,
    pigeonpea_production DECIMAL(12,2) DEFAULT 0.00,
    pigeonpea_yield DECIMAL(12,2) DEFAULT 0.00,
    
    -- Groundnut
    groundnut_area DECIMAL(12,2) DEFAULT 0.00,
    groundnut_production DECIMAL(12,2) DEFAULT 0.00,
    groundnut_yield DECIMAL(12,2) DEFAULT 0.00,
    
    -- Sesamum (Til)
    sesamum_area DECIMAL(12,2) DEFAULT 0.00,
    sesamum_production DECIMAL(12,2) DEFAULT 0.00,
    sesamum_yield DECIMAL(12,2) DEFAULT 0.00,
    
    -- Rapeseed and Mustard
    rapeseed_mustard_area DECIMAL(12,2) DEFAULT 0.00,
    rapeseed_mustard_production DECIMAL(12,2) DEFAULT 0.00,
    rapeseed_mustard_yield DECIMAL(12,2) DEFAULT 0.00,
    
    -- Safflower
    safflower_area DECIMAL(12,2) DEFAULT 0.00,
    safflower_production DECIMAL(12,2) DEFAULT 0.00,
    safflower_yield DECIMAL(12,2) DEFAULT 0.00,
    
    -- Castor
    castor_area DECIMAL(12,2) DEFAULT 0.00,
    castor_production DECIMAL(12,2) DEFAULT 0.00,
    castor_yield DECIMAL(12,2) DEFAULT 0.00,
    
    -- Linseed
    linseed_area DECIMAL(12,2) DEFAULT 0.00,
    linseed_production DECIMAL(12,2) DEFAULT 0.00,
    linseed_yield DECIMAL(12,2) DEFAULT 0.00,
    
    -- Sunflower
    sunflower_area DECIMAL(12,2) DEFAULT 0.00,
    sunflower_production DECIMAL(12,2) DEFAULT 0.00,
    sunflower_yield DECIMAL(12,2) DEFAULT 0.00,
    
    -- Soybean
    soybean_area DECIMAL(12,2) DEFAULT 0.00,
    soybean_production DECIMAL(12,2) DEFAULT 0.00,
    soybean_yield DECIMAL(12,2) DEFAULT 0.00,
    
    -- Sugarcane
    sugarcane_area DECIMAL(12,2) DEFAULT 0.00,
    sugarcane_production DECIMAL(12,2) DEFAULT 0.00,
    sugarcane_yield DECIMAL(12,2) DEFAULT 0.00,
    
    -- Cotton
    cotton_area DECIMAL(12,2) DEFAULT 0.00,
    cotton_production DECIMAL(12,2) DEFAULT 0.00,
    cotton_yield DECIMAL(12,2) DEFAULT 0.00,
    
    -- Oilseeds (Total)
    oilseeds_area DECIMAL(12,2) DEFAULT 0.00,
    oilseeds_production DECIMAL(12,2) DEFAULT 0.00,
    oilseeds_yield DECIMAL(12,2) DEFAULT 0.00,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (district_id) REFERENCES dim_district(district_id),
    FOREIGN KEY (year_id) REFERENCES dim_year(year_id),
    
    INDEX idx_district_year (district_id, year_id),
    INDEX idx_year (year_id),
    INDEX idx_rice_production (rice_production),
    INDEX idx_wheat_production (wheat_production)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================================
-- VIEWS FOR COMMON QUERIES
-- ============================================================================

-- View: State-wise aggregate production
CREATE OR REPLACE VIEW vw_state_production AS
SELECT 
    s.state_name,
    y.year_id as year,
    SUM(f.rice_production) as total_rice_production,
    SUM(f.wheat_production) as total_wheat_production,
    SUM(f.maize_production) as total_maize_production,
    SUM(f.oilseeds_production) as total_oilseeds_production,
    SUM(f.sugarcane_production) as total_sugarcane_production,
    SUM(f.cotton_production) as total_cotton_production
FROM fact_production f
JOIN dim_district d ON f.district_id = d.district_id
JOIN dim_state s ON d.state_id = s.state_id
JOIN dim_year y ON f.year_id = y.year_id
GROUP BY s.state_name, y.year_id;

-- View: District-wise current year production
CREATE OR REPLACE VIEW vw_district_current_production AS
SELECT 
    s.state_name,
    d.district_name,
    f.year_id as year,
    f.rice_production,
    f.rice_yield,
    f.wheat_production,
    f.wheat_yield,
    f.maize_production,
    f.maize_yield
FROM fact_production f
JOIN dim_district d ON f.district_id = d.district_id
JOIN dim_state s ON d.state_id = s.state_id
WHERE f.year_id = (SELECT MAX(year_id) FROM fact_production);

-- ============================================================================
-- STORED PROCEDURES
-- ============================================================================

DELIMITER //

-- Get top producing states for any crop
CREATE PROCEDURE sp_top_states_by_crop(
    IN crop_name VARCHAR(50),
    IN top_n INT,
    IN start_year INT,
    IN end_year INT
)
BEGIN
    SET @sql = CONCAT(
        'SELECT s.state_name, 
                SUM(f.', crop_name, '_production) as total_production,
                AVG(f.', crop_name, '_yield) as avg_yield
         FROM fact_production f
         JOIN dim_district d ON f.district_id = d.district_id
         JOIN dim_state s ON d.state_id = s.state_id
         WHERE f.year_id BETWEEN ', start_year, ' AND ', end_year,
        ' GROUP BY s.state_name
          ORDER BY total_production DESC
          LIMIT ', top_n
    );
    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END //

DELIMITER ;

-- ============================================================================
-- INDEXES FOR PERFORMANCE
-- ============================================================================

-- Additional composite indexes for common queries
CREATE INDEX idx_state_year ON fact_production(year_id, district_id);
CREATE INDEX idx_rice_metrics ON fact_production(rice_area, rice_production, rice_yield);
CREATE INDEX idx_wheat_metrics ON fact_production(wheat_area, wheat_production, wheat_yield);