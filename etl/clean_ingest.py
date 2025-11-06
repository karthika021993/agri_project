"""
AgriData Explorer - ETL Pipeline
File: etl/clean_ingest.py
Purpose: Clean and prepare raw agricultural data for analysis
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('etl_process.log'),
        logging.StreamHandler()
    ]
)

class AgriDataCleaner:
    """Clean and standardize agricultural data"""
    
    def __init__(self, input_path, output_dir='data/processed'):
        self.input_path = input_path
        self.output_dir = output_dir
        self.df_raw = None
        self.df_clean = None
        self.cleaning_report = {}
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
    
    def load_data(self):
        """Load raw data"""
        logging.info(f"Loading data from {self.input_path}")
        self.df_raw = pd.read_csv(self.input_path, encoding='utf-8')
        logging.info(f"Loaded {len(self.df_raw)} rows and {len(self.df_raw.columns)} columns")
        self.cleaning_report['original_rows'] = len(self.df_raw)
        self.cleaning_report['original_columns'] = len(self.df_raw.columns)
        return self
    
    def standardize_columns(self):
        """Standardize column names"""
        logging.info("Standardizing column names...")
        
        # Strip whitespace
        self.df_raw.columns = self.df_raw.columns.str.strip()
        
        # Column mapping for consistency
        column_mapping = {
            'Dist Code': 'district_code',
            'Year': 'year',
            'State Code': 'state_code',
            'State Name': 'state_name',
            'Dist Name': 'district_name'
        }
        
        # Rename columns
        self.df_raw.rename(columns=column_mapping, inplace=True)
        
        # Standardize crop columns (lowercase with underscores)
        for col in self.df_raw.columns:
            if col not in column_mapping.values():
                new_col = col.lower().replace(' ', '_').replace('(', '').replace(')', '').replace('/', '_')
                self.df_raw.rename(columns={col: new_col}, inplace=True)
        
        logging.info("Column standardization complete")
        return self
    
    def handle_missing_values(self):
        """Handle missing values appropriately"""
        logging.info("Handling missing values...")
        
        missing_before = self.df_raw.isnull().sum().sum()
        
        # Fill missing state/district names
        self.df_raw.loc[:, 'state_name'] = self.df_raw['state_name'].fillna('UNKNOWN')
        self.df_raw.loc[:, 'district_name'] = self.df_raw['district_name'].fillna('UNKNOWN')
        
        # For numeric columns (area, production, yield), fill with 0
        numeric_cols = self.df_raw.select_dtypes(include=[np.number]).columns
        self.df_raw[numeric_cols] = self.df_raw[numeric_cols].fillna(0)
        
        missing_after = self.df_raw.isnull().sum().sum()
        
        self.cleaning_report['missing_values_handled'] = missing_before - missing_after
        logging.info(f"Handled {missing_before - missing_after} missing values")
        return self
    
    def remove_duplicates(self):
        """Remove duplicate rows"""
        logging.info("Removing duplicates...")
        
        duplicates_before = self.df_raw.duplicated().sum()
        self.df_raw.drop_duplicates(inplace=True)
        duplicates_after = self.df_raw.duplicated().sum()
        
        self.cleaning_report['duplicates_removed'] = duplicates_before - duplicates_after
        logging.info(f"Removed {duplicates_before - duplicates_after} duplicate rows")
        return self
    
    def validate_data_types(self):
        """Ensure correct data types"""
        logging.info("Validating data types...")
        
        # Ensure year is integer
        self.df_raw['year'] = self.df_raw['year'].astype(int)
        
        # Ensure codes are strings
        if 'district_code' in self.df_raw.columns:
            self.df_raw['district_code'] = self.df_raw['district_code'].astype(str)
        if 'state_code' in self.df_raw.columns:
            self.df_raw['state_code'] = self.df_raw['state_code'].astype(str)
        
        # Ensure numeric columns are float
        numeric_cols = [col for col in self.df_raw.columns 
                       if 'area' in col or 'production' in col or 'yield' in col]
        for col in numeric_cols:
            self.df_raw[col] = pd.to_numeric(self.df_raw[col], errors='coerce').fillna(0)
        
        logging.info("Data type validation complete")
        return self
    
    def add_derived_columns(self):
        """Add useful derived columns"""
        logging.info("Adding derived columns...")
        
        # Add decade column
        self.df_raw['decade'] = (self.df_raw['year'] // 10) * 10
        
        # Add season classification (if year data allows)
        self.df_raw['is_recent'] = self.df_raw['year'] >= 2015
        
        logging.info("Derived columns added")
        return self
    
    def filter_invalid_records(self):
        """Remove invalid records"""
        logging.info("Filtering invalid records...")
        
        rows_before = len(self.df_raw)
        
        # Remove rows where state or district is UNKNOWN and all production is 0
        production_cols = [col for col in self.df_raw.columns if 'production' in col]
        self.df_raw = self.df_raw[
            ~((self.df_raw['state_name'] == 'UNKNOWN') & 
              (self.df_raw[production_cols].sum(axis=1) == 0))
        ]
        
        rows_after = len(self.df_raw)
        self.cleaning_report['invalid_records_removed'] = rows_before - rows_after
        
        logging.info(f"Removed {rows_before - rows_after} invalid records")
        return self
    
    def finalize_cleaning(self):
        """Finalize and prepare clean dataset"""
        logging.info("Finalizing cleaned dataset...")
        
        self.df_clean = self.df_raw.copy()
        self.cleaning_report['final_rows'] = len(self.df_clean)
        self.cleaning_report['final_columns'] = len(self.df_clean.columns)
        self.cleaning_report['cleaning_timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        logging.info("Data cleaning complete!")
        return self
    
    def save_cleaned_data(self, filename='agri_data_cleaned.csv'):
        """Save cleaned data"""
        output_path = os.path.join(self.output_dir, filename)
        self.df_clean.to_csv(output_path, index=False)
        logging.info(f"Cleaned data saved to {output_path}")
        
        # Save cleaning report
        report_path = os.path.join(self.output_dir, 'cleaning_report.txt')
        with open(report_path, 'w') as f:
            f.write("AgriData Cleaning Report\n")
            f.write("="*50 + "\n\n")
            for key, value in self.cleaning_report.items():
                f.write(f"{key}: {value}\n")
        
        logging.info(f"Cleaning report saved to {report_path}")
        return self
    
    def run_pipeline(self):
        """Run complete cleaning pipeline"""
        logging.info("Starting ETL Pipeline...")
        
        (self.load_data()
            .standardize_columns()
            .handle_missing_values()
            .remove_duplicates()
            .validate_data_types()
            .add_derived_columns()
            .filter_invalid_records()
            .finalize_cleaning()
            .save_cleaned_data())
        
        logging.info("ETL Pipeline completed successfully!")
        return self.df_clean

# Main execution
if __name__ == "__main__":
    # Configure paths (relative to project root)
    import os
    
    # Get the project root directory (parent of etl folder)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    
    INPUT_FILE = os.path.join(project_root, 'data', 'raw', 'icrisat_district_data.csv')
    OUTPUT_DIR = os.path.join(project_root, 'data', 'processed')
    
    # Check if input file exists
    if not os.path.exists(INPUT_FILE):
        print("\n" + "="*70)
        print("❌ ERROR: Data file not found!")
        print("="*70)
        print(f"Looking for: {INPUT_FILE}")
        print("\n📋 TO FIX THIS:")
        print("1. Download ICRISAT dataset from:")
        print("   https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/AFDMSU")
        print(f"2. Create folder: {os.path.join(project_root, 'data', 'raw')}")
        print("3. Save the CSV file as: icrisat_district_data.csv")
        print(f"4. Full path should be: {INPUT_FILE}")
        print("="*70)
        exit(1)
    
    # Run cleaning pipeline
    cleaner = AgriDataCleaner(INPUT_FILE, OUTPUT_DIR)
    cleaned_data = cleaner.run_pipeline()
    
    # Display summary
    print("\n" + "="*60)
    print("DATA CLEANING SUMMARY")
    print("="*60)
    for key, value in cleaner.cleaning_report.items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    
    print(f"\nCleaned dataset shape: {cleaned_data.shape}")
    print("\nSample of cleaned data:")
    print(cleaned_data.head())