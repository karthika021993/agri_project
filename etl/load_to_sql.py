"""
AgriData Explorer - SQL Data Loader
File: etl/load_to_sql.py
Purpose: Load cleaned data into MySQL database
"""

import pandas as pd
import mysql.connector
from mysql.connector import Error
import logging
from sqlalchemy import create_engine
import os

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AgriDataLoader:
    """Load agricultural data into MySQL database"""
    
    def __init__(self, host='localhost', database='agridata_db', user='root', password=''):
        """Initialize database connection parameters"""
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.engine = None
    
    def create_database(self):
        """Create database if not exists"""
        try:
            # Connect without database selection
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            cursor = connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            logging.info(f"Database '{self.database}' created/verified")
            cursor.close()
            connection.close()
        except Error as e:
            logging.error(f"Error creating database: {e}")
            raise
    
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            
            # Create SQLAlchemy engine for pandas
            connection_string = f"mysql+mysqlconnector://{self.user}:{self.password}@{self.host}/{self.database}"
            self.engine = create_engine(connection_string)
            
            if self.connection.is_connected():
                logging.info(f"Connected to MySQL database: {self.database}")
                return True
        except Error as e:
            logging.error(f"Error connecting to MySQL: {e}")
            return False
    
    def create_tables(self):
        """Create normalized database schema"""
        cursor = self.connection.cursor()
        
        # Drop existing tables
        drop_tables = [
            "DROP TABLE IF EXISTS fact_production",
            "DROP TABLE IF EXISTS dim_district",
            "DROP TABLE IF EXISTS dim_state",
            "DROP TABLE IF EXISTS dim_year"
        ]
        
        for query in drop_tables:
            cursor.execute(query)
            logging.info(f"Executed: {query}")
        
        # Create dimension tables
        create_queries = [
            """
            CREATE TABLE dim_state (
                state_id INT PRIMARY KEY AUTO_INCREMENT,
                state_code VARCHAR(10) UNIQUE,
                state_name VARCHAR(100) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE dim_district (
                district_id INT PRIMARY KEY AUTO_INCREMENT,
                district_code VARCHAR(20),
                district_name VARCHAR(100) NOT NULL,
                state_id INT,
                FOREIGN KEY (state_id) REFERENCES dim_state(state_id),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE dim_year (
                year_id INT PRIMARY KEY,
                decade INT,
                is_recent BOOLEAN,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE fact_production (
                production_id INT PRIMARY KEY AUTO_INCREMENT,
                district_id INT,
                year_id INT,
                rice_area DECIMAL(12,2),
                rice_production DECIMAL(12,2),
                rice_yield DECIMAL(12,2),
                wheat_area DECIMAL(12,2),
                wheat_production DECIMAL(12,2),
                wheat_yield DECIMAL(12,2),
                maize_area DECIMAL(12,2),
                maize_production DECIMAL(12,2),
                maize_yield DECIMAL(12,2),
                sorghum_area DECIMAL(12,2),
                sorghum_production DECIMAL(12,2),
                sorghum_yield DECIMAL(12,2),
                pearl_millet_area DECIMAL(12,2),
                pearl_millet_production DECIMAL(12,2),
                pearl_millet_yield DECIMAL(12,2),
                groundnut_area DECIMAL(12,2),
                groundnut_production DECIMAL(12,2),
                groundnut_yield DECIMAL(12,2),
                soybean_area DECIMAL(12,2),
                soybean_production DECIMAL(12,2),
                soybean_yield DECIMAL(12,2),
                sunflower_area DECIMAL(12,2),
                sunflower_production DECIMAL(12,2),
                sunflower_yield DECIMAL(12,2),
                sugarcane_area DECIMAL(12,2),
                sugarcane_production DECIMAL(12,2),
                sugarcane_yield DECIMAL(12,2),
                cotton_area DECIMAL(12,2),
                cotton_production DECIMAL(12,2),
                cotton_yield DECIMAL(12,2),
                oilseeds_area DECIMAL(12,2),
                oilseeds_production DECIMAL(12,2),
                oilseeds_yield DECIMAL(12,2),
                FOREIGN KEY (district_id) REFERENCES dim_district(district_id),
                FOREIGN KEY (year_id) REFERENCES dim_year(year_id),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        ]
        
        for query in create_queries:
            cursor.execute(query)
            logging.info("Table created successfully")
        
        self.connection.commit()
        cursor.close()
        logging.info("All tables created successfully")
    
    def load_dimension_tables(self, df):
        """Load dimension tables from cleaned data"""
        
        # Load dim_state
        states_df = df[['state_code', 'state_name']].drop_duplicates()
        states_df.to_sql('dim_state', self.engine, if_exists='append', index=False)
        logging.info(f"Loaded {len(states_df)} states into dim_state")
        
        # Get state_id mapping
        state_mapping = pd.read_sql("SELECT state_id, state_code FROM dim_state", self.engine)
        df = df.merge(state_mapping, on='state_code', how='left')
        
        # Load dim_district
        districts_df = df[['district_code', 'district_name', 'state_id']].drop_duplicates()
        districts_df.to_sql('dim_district', self.engine, if_exists='append', index=False)
        logging.info(f"Loaded {len(districts_df)} districts into dim_district")
        
        # Load dim_year
        years_df = df[['year', 'decade', 'is_recent']].drop_duplicates()
        years_df = years_df.rename(columns={'year': 'year_id'})
        years_df.to_sql('dim_year', self.engine, if_exists='append', index=False)
        logging.info(f"Loaded {len(years_df)} years into dim_year")
        
        return df
    
    def load_fact_table(self, df):
        """Load fact table with production data"""
        
        # Get district_id mapping
        district_mapping = pd.read_sql(
            "SELECT district_id, district_code FROM dim_district", 
            self.engine
        )
        df = df.merge(district_mapping, on='district_code', how='left')
        
        # Prepare fact table data
        fact_columns = {
            'district_id': 'district_id',
            'year': 'year_id',
            'rice_area_1000_ha': 'rice_area',
            'rice_production_1000_tons': 'rice_production',
            'rice_yield_kg_per_ha': 'rice_yield',
            'wheat_area_1000_ha': 'wheat_area',
            'wheat_production_1000_tons': 'wheat_production',
            'wheat_yield_kg_per_ha': 'wheat_yield',
            'maize_area_1000_ha': 'maize_area',
            'maize_production_1000_tons': 'maize_production',
            'maize_yield_kg_per_ha': 'maize_yield',
            'sorghum_area_1000_ha': 'sorghum_area',
            'sorghum_production_1000_tons': 'sorghum_production',
            'sorghum_yield_kg_per_ha': 'sorghum_yield',
            'groundnut_area_1000_ha': 'groundnut_area',
            'groundnut_production_1000_tons': 'groundnut_production',
            'groundnut_yield_kg_per_ha': 'groundnut_yield',
            'soybean_area_1000_ha': 'soybean_area',
            'soybean_production_1000_tons': 'soybean_production',
            'soybean_yield_kg_per_ha': 'soybean_yield',
            'sunflower_area_1000_ha': 'sunflower_area',
            'sunflower_production_1000_tons': 'sunflower_production',
            'sunflower_yield_kg_per_ha': 'sunflower_yield',
            'sugarcane_area_1000_ha': 'sugarcane_area',
            'sugarcane_production_1000_tons': 'sugarcane_production',
            'sugarcane_yield_kg_per_ha': 'sugarcane_yield',
            'cotton_area_1000_ha': 'cotton_area',
            'cotton_production_1000_tons': 'cotton_production',
            'cotton_yield_kg_per_ha': 'cotton_yield',
            'oilseeds_area_1000_ha': 'oilseeds_area',
            'oilseeds_production_1000_tons': 'oilseeds_production',
            'oilseeds_yield_kg_per_ha': 'oilseeds_yield'
        }
        
        # Select and rename columns that exist
        available_cols = {k: v for k, v in fact_columns.items() if k in df.columns}
        fact_df = df[list(available_cols.keys())].rename(columns=available_cols)
        
        # Load to database in chunks
        chunk_size = 10000
        total_rows = len(fact_df)
        
        for i in range(0, total_rows, chunk_size):
            chunk = fact_df.iloc[i:i+chunk_size]
            chunk.to_sql('fact_production', self.engine, if_exists='append', index=False)
            logging.info(f"Loaded {min(i+chunk_size, total_rows)}/{total_rows} rows")
        
        logging.info(f"Loaded {total_rows} rows into fact_production")
    
    def verify_data_load(self):
        """Verify data was loaded correctly"""
        cursor = self.connection.cursor()
        
        tables = ['dim_state', 'dim_district', 'dim_year', 'fact_production']
        
        print("\n" + "="*60)
        print("DATA LOAD VERIFICATION")
        print("="*60)
        
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"{table}: {count:,} rows")
        
        cursor.close()
    
    def close(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logging.info("MySQL connection closed")
    
    def run_pipeline(self, csv_file):
        """Run complete data loading pipeline"""
        try:
            # Create database
            self.create_database()
            
            # Connect
            if not self.connect():
                raise Exception("Failed to connect to database")
            
            # Create tables
            self.create_tables()
            
            # Load data
            logging.info(f"Loading data from {csv_file}")
            df = pd.read_csv(csv_file)
            
            # Load dimensions
            df = self.load_dimension_tables(df)
            
            # Load facts
            self.load_fact_table(df)
            
            # Verify
            self.verify_data_load()
            
            logging.info("Data loading pipeline completed successfully!")
            
        except Exception as e:
            logging.error(f"Error in pipeline: {e}")
            raise
        finally:
            self.close()

# Main execution
if __name__ == "__main__":
    # Database configuration
    DB_CONFIG = {
        'host': 'localhost',
        'database': 'agridata_db',
        'user': 'root',
        'password': 'your_password_here'  # Update with your MySQL password
    }
    
    # Path to cleaned data
    CLEANED_DATA_PATH = 'data/processed/agri_data_cleaned.csv'
    
    # Run loader
    loader = AgriDataLoader(**DB_CONFIG)
    loader.run_pipeline(CLEANED_DATA_PATH)