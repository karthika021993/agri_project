-- AgriData Explorer - Analysis Queries
-- File: sql/analysis_queries.sql
-- Purpose: Answer 10 key business questions

USE agridata_db;

-- ============================================================================
-- QUERY 1: Year-wise Trend of Rice Production Across States (Top 3)
-- ============================================================================

SELECT 
    s.state_name,
    f.year_id as year,
    SUM(f.rice_production) as total_rice_production,
    RANK() OVER (PARTITION BY f.year_id ORDER BY SUM(f.rice_production) DESC) as state_rank
FROM fact_production f
JOIN dim_district d ON f.district_id = d.district_id
JOIN dim_state s ON d.state_id = s.state_id
GROUP BY s.state_name, f.year_id
HAVING state_rank <= 3
ORDER BY f.year_id, state_rank;


-- ============================================================================
-- QUERY 2: Top 5 Districts by Wheat Yield Increase Over the Last 5 Years
-- ============================================================================

WITH wheat_yield_change AS (
    SELECT 
        d.district_name,
        s.state_name,
        MAX(CASE WHEN f.year_id = (SELECT MAX(year_id) FROM fact_production) 
            THEN f.wheat_yield END) as current_yield,
        MAX(CASE WHEN f.year_id = (SELECT MAX(year_id) - 5 FROM fact_production) 
            THEN f.wheat_yield END) as past_yield
    FROM fact_production f
    JOIN dim_district d ON f.district_id = d.district_id
    JOIN dim_state s ON d.state_id = s.state_id
    WHERE f.wheat_yield > 0
    GROUP BY d.district_name, s.state_name
    HAVING current_yield IS NOT NULL AND past_yield IS NOT NULL
)
SELECT 
    district_name,
    state_name,
    current_yield,
    past_yield,
    (current_yield - past_yield) as yield_increase,
    ROUND(((current_yield - past_yield) / past_yield * 100), 2) as pct_increase
FROM wheat_yield_change
WHERE past_yield > 0
ORDER BY yield_increase DESC
LIMIT 5;


-- ============================================================================
-- QUERY 3: States with Highest Growth in Oilseed Production (5-Year Growth Rate)
-- ============================================================================

WITH oilseed_growth AS (
    SELECT 
        s.state_name,
        SUM(CASE WHEN f.year_id >= (SELECT MAX(year_id) - 4 FROM fact_production) 
            THEN f.oilseeds_production END) as recent_5yr_production,
        SUM(CASE WHEN f.year_id BETWEEN (SELECT MAX(year_id) - 9 FROM fact_production) 
                                    AND (SELECT MAX(year_id) - 5 FROM fact_production)
            THEN f.oilseeds_production END) as previous_5yr_production
    FROM fact_production f
    JOIN dim_district d ON f.district_id = d.district_id
    JOIN dim_state s ON d.state_id = s.state_id
    GROUP BY s.state_name
    HAVING recent_5yr_production > 0 AND previous_5yr_production > 0
)
SELECT 
    state_name,
    recent_5yr_production,
    previous_5yr_production,
    ROUND(((recent_5yr_production - previous_5yr_production) / previous_5yr_production * 100), 2) as growth_rate_pct
FROM oilseed_growth
ORDER BY growth_rate_pct DESC
LIMIT 10;


-- ============================================================================
-- QUERY 4: District-wise Correlation Between Area and Production for Major Crops
-- ============================================================================

SELECT 
    s.state_name,
    d.district_name,
    
    -- Rice metrics
    AVG(f.rice_area) as avg_rice_area,
    AVG(f.rice_production) as avg_rice_production,
    ROUND(AVG(f.rice_yield), 2) as avg_rice_yield,
    
    -- Wheat metrics
    AVG(f.wheat_area) as avg_wheat_area,
    AVG(f.wheat_production) as avg_wheat_production,
    ROUND(AVG(f.wheat_yield), 2) as avg_wheat_yield,
    
    -- Maize metrics
    AVG(f.maize_area) as avg_maize_area,
    AVG(f.maize_production) as avg_maize_production,
    ROUND(AVG(f.maize_yield), 2) as avg_maize_yield,
    
    -- Efficiency score (production per unit area)
    ROUND((AVG(f.rice_production) / NULLIF(AVG(f.rice_area), 0)), 2) as rice_efficiency,
    ROUND((AVG(f.wheat_production) / NULLIF(AVG(f.wheat_area), 0)), 2) as wheat_efficiency,
    ROUND((AVG(f.maize_production) / NULLIF(AVG(f.maize_area), 0)), 2) as maize_efficiency
    
FROM fact_production f
JOIN dim_district d ON f.district_id = d.district_id
JOIN dim_state s ON d.state_id = s.state_id
WHERE f.year_id >= (SELECT MAX(year_id) - 10 FROM fact_production)
GROUP BY s.state_name, d.district_name
HAVING avg_rice_area > 0 OR avg_wheat_area > 0 OR avg_maize_area > 0
ORDER BY s.state_name, d.district_name;


-- ============================================================================
-- QUERY 5: Yearly Production Growth of Cotton in Top 5 Cotton Producing States
-- ============================================================================

WITH top_cotton_states AS (
    SELECT s.state_name
    FROM fact_production f
    JOIN dim_district d ON f.district_id = d.district_id
    JOIN dim_state s ON d.state_id = s.state_id
    GROUP BY s.state_name
    ORDER BY SUM(f.cotton_production) DESC
    LIMIT 5
)
SELECT 
    s.state_name,
    f.year_id as year,
    SUM(f.cotton_production) as total_cotton_production,
    LAG(SUM(f.cotton_production)) OVER (PARTITION BY s.state_name ORDER BY f.year_id) as prev_year_production,
    ROUND(
        ((SUM(f.cotton_production) - LAG(SUM(f.cotton_production)) OVER (PARTITION BY s.state_name ORDER BY f.year_id)) 
        / NULLIF(LAG(SUM(f.cotton_production)) OVER (PARTITION BY s.state_name ORDER BY f.year_id), 0) * 100), 
        2
    ) as yoy_growth_pct
FROM fact_production f
JOIN dim_district d ON f.district_id = d.district_id
JOIN dim_state s ON d.state_id = s.state_id
WHERE s.state_name IN (SELECT state_name FROM top_cotton_states)
GROUP BY s.state_name, f.year_id
ORDER BY s.state_name, f.year_id;


-- ============================================================================
-- QUERY 6: Districts with the Highest Groundnut Production in 2020
-- ============================================================================

SELECT 
    s.state_name,
    d.district_name,
    f.groundnut_area,
    f.groundnut_production,
    f.groundnut_yield,
    RANK() OVER (ORDER BY f.groundnut_production DESC) as production_rank
FROM fact_production f
JOIN dim_district d ON f.district_id = d.district_id
JOIN dim_state s ON d.state_id = s.state_id
WHERE f.year_id = 2020
    AND f.groundnut_production > 0
ORDER BY f.groundnut_production DESC
LIMIT 20;


-- ============================================================================
-- QUERY 7: Annual Average Maize Yield Across All States
-- ============================================================================

SELECT 
    f.year_id as year,
    s.state_name,
    ROUND(AVG(f.maize_yield), 2) as avg_maize_yield,
    SUM(f.maize_area) as total_maize_area,
    SUM(f.maize_production) as total_maize_production,
    COUNT(DISTINCT d.district_id) as num_districts
FROM fact_production f
JOIN dim_district d ON f.district_id = d.district_id
JOIN dim_state s ON d.state_id = s.state_id
WHERE f.maize_yield > 0
GROUP BY f.year_id, s.state_name
ORDER BY f.year_id, s.state_name;

-- Summary across all states per year
SELECT 
    f.year_id as year,
    ROUND(AVG(f.maize_yield), 2) as national_avg_yield,
    SUM(f.maize_area) as total_national_area,
    SUM(f.maize_production) as total_national_production
FROM fact_production f
WHERE f.maize_yield > 0
GROUP BY f.year_id
ORDER BY f.year_id;


-- ============================================================================
-- QUERY 8: Total Area Cultivated for Oilseeds in Each State
-- ============================================================================

SELECT 
    s.state_name,
    SUM(f.oilseeds_area) as total_oilseeds_area,
    SUM(f.groundnut_area) as total_groundnut_area,
    SUM(f.soybean_area) as total_soybean_area,
    SUM(f.sunflower_area) as total_sunflower_area,
    SUM(f.rapeseed_mustard_area) as total_rapeseed_mustard_area,
    COUNT(DISTINCT f.year_id) as years_of_data,
    ROUND(AVG(f.oilseeds_area), 2) as avg_annual_oilseeds_area
FROM fact_production f
JOIN dim_district d ON f.district_id = d.district_id
JOIN dim_state s ON d.state_id = s.state_id
GROUP BY s.state_name
ORDER BY total_oilseeds_area DESC;


-- ============================================================================
-- QUERY 9: Districts with the Highest Rice Yield
-- ============================================================================

SELECT 
    s.state_name,
    d.district_name,
    ROUND(AVG(f.rice_yield), 2) as avg_rice_yield,
    AVG(f.rice_area) as avg_rice_area,
    AVG(f.rice_production) as avg_rice_production,
    COUNT(f.year_id) as years_cultivated
FROM fact_production f
JOIN dim_district d ON f.district_id = d.district_id
JOIN dim_state s ON d.state_id = s.state_id
WHERE f.rice_yield > 0
    AND f.year_id >= (SELECT MAX(year_id) - 10 FROM fact_production)
GROUP BY s.state_name, d.district_name
HAVING years_cultivated >= 5
ORDER BY avg_rice_yield DESC
LIMIT 20;


-- ============================================================================
-- QUERY 10: Compare Production of Wheat and Rice for Top 5 States Over 10 Years
-- ============================================================================

WITH top_states AS (
    SELECT s.state_name
    FROM fact_production f
    JOIN dim_district d ON f.district_id = d.district_id
    JOIN dim_state s ON d.state_id = s.state_id
    WHERE f.year_id >= (SELECT MAX(year_id) - 10 FROM fact_production)
    GROUP BY s.state_name
    ORDER BY (SUM(f.rice_production) + SUM(f.wheat_production)) DESC
    LIMIT 5
)
SELECT 
    s.state_name,
    f.year_id as year,
    SUM(f.rice_area) as rice_area,
    SUM(f.rice_production) as rice_production,
    ROUND(AVG(f.rice_yield), 2) as avg_rice_yield,
    SUM(f.wheat_area) as wheat_area,
    SUM(f.wheat_production) as wheat_production,
    ROUND(AVG(f.wheat_yield), 2) as avg_wheat_yield,
    ROUND((SUM(f.rice_production) / NULLIF(SUM(f.wheat_production), 0)), 2) as rice_to_wheat_ratio
FROM fact_production f
JOIN dim_district d ON f.district_id = d.district_id
JOIN dim_state s ON d.state_id = s.state_id
WHERE s.state_name IN (SELECT state_name FROM top_states)
    AND f.year_id >= (SELECT MAX(year_id) - 10 FROM fact_production)
GROUP BY s.state_name, f.year_id
ORDER BY s.state_name, f.year_id;


-- ============================================================================
-- BONUS: Performance Analysis Queries
-- ============================================================================

-- State-wise crop diversification index
SELECT 
    s.state_name,
    COUNT(DISTINCT CASE WHEN f.rice_production > 0 THEN d.district_id END) as districts_growing_rice,
    COUNT(DISTINCT CASE WHEN f.wheat_production > 0 THEN d.district_id END) as districts_growing_wheat,
    COUNT(DISTINCT CASE WHEN f.maize_production > 0 THEN d.district_id END) as districts_growing_maize,
    COUNT(DISTINCT CASE WHEN f.cotton_production > 0 THEN d.district_id END) as districts_growing_cotton,
    COUNT(DISTINCT d.district_id) as total_districts
FROM fact_production f
JOIN dim_district d ON f.district_id = d.district_id
JOIN dim_state s ON d.state_id = s.state_id
WHERE f.year_id = (SELECT MAX(year_id) FROM fact_production)
GROUP BY s.state_name
ORDER BY s.state_name;

-- Year-over-year growth trends
SELECT 
    year_id as year,
    SUM(rice_production) as total_rice,
    SUM(wheat_production) as total_wheat,
    SUM(cotton_production) as total_cotton,
    SUM(oilseeds_production) as total_oilseeds
FROM fact_production
GROUP BY year_id
ORDER BY year_id;