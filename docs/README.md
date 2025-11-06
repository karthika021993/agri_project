# AgriData Explorer: Understanding Indian Agriculture with EDA

## 📊 Project Overview

**AgriData Explorer** is a comprehensive data analytics platform that visualizes and analyzes Indian agricultural data from the ICRISAT District Level Database. The project provides insights into crop production, yields, and cultivation areas across different states and districts in India.

### 🎯 Objective

To create an interactive data visualization platform that helps:
- **Farmers**: Make informed crop selection decisions
- **Policymakers**: Identify regions requiring intervention
- **Researchers**: Analyze agricultural trends and patterns

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|-------------|
| **Programming** | Python 3.8+ |
| **Data Processing** | Pandas, NumPy |
| **Visualization** | Matplotlib, Seaborn, Plotly |
| **Database** | MySQL 8.0+ |
| **BI Tool** | Power BI Desktop |
| **Version Control** | Git & GitHub |

---



## 📁 Project Structure

```
agri-data-explorer/
├── etl/
│   ├── clean_ingest.py          # Data cleaning pipeline
│   ├── load_to_sql.py            # SQL loader script
│   └── data_quality_report.ipynb # Data quality analysis
├── sql/
│   ├── schema.sql                # Database schema
│   ├── seed_data.sql             # Initial data
│   └── analysis_queries.sql      # 10 business queries
├── analysis/
│   ├── eda_rice.ipynb            # Rice production EDA
│   ├── eda_wheat.ipynb           # Wheat production EDA
│   └── plotly_exports/           # Visualization outputs
├── models/
│   ├── forecast_train.ipynb      # ML forecasting models
│   └── model_utils.py            # Model utilities
├── powerbi/
│   └── AgriDataExplorer.pbix     # Power BI dashboard
├── docs/
│   ├── README.md                 # This file
│   ├── data_dictionary.md        # Data field descriptions
│   └── handover.md               # Project handover guide
├── presentation/
│   └── agri_explorer_presentation.pptx
├── data/
│   ├── raw/                      # Original ICRISAT data
│   └── processed/                # Cleaned data
└── requirements.txt              # Python dependencies
```

---

## 🚀 Getting Started

### Prerequisites

1. **Python 3.8 or higher**
2. **MySQL 8.0 or higher**
3. **Power BI Desktop** (Free version available)
4. **Git** (for version control)

### Installation Steps

#### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/agri-data-explorer.git
cd agri-data-explorer
```

#### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt content:**
```
pandas>=1.5.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0
plotly>=5.14.0
mysql-connector-python>=8.0.33
sqlalchemy>=2.0.0
jupyter>=1.0.0
notebook>=6.5.0
openpyxl>=3.1.0
```

#### 4. Setup MySQL Database

```bash
# Login to MySQL
mysql -u root -p

# Create database
CREATE DATABASE agridata_db;

# Run schema
mysql -u root -p agridata_db < sql/schema.sql
```

#### 5. Download ICRISAT Dataset

- Download from: [ICRISAT District Level Data](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/AFDMSU)
- Place CSV file in `data/raw/` folder
- Rename to: `icrisat_district_data.csv`

---



## 📝 Usage Guide

### Step 1: Data Cleaning

```bash
cd D:\agri_project\etl
python clean_ingest.py
```

**Output:**
- Cleaned CSV: `data/processed/agri_data_cleaned.csv`
- Cleaning Report: `data/processed/cleaning_report.txt`




### Step 2: Load Data to MySQL

```bash
# Update database credentials in load_to_sql.py
cd ..\analysis
python comprehensive_eda.py
```
# Check output
dir ..\data\processed
Generate Visualizations:
bash# Generate all charts



### Step 3: Load Data to MySQL

```bash
# Update database credentials in load_to_sql.py
cd ..\etl
python load_to_sql.py
```

# output 
-🎨 Using Your Visualizations
Your 15 visualizations are saved in:
D:\agri_project\analysis\plotly_exports\

 


### Step 4: Exploratory Data Analysis

```bash
cd analysis
jupyter notebook eda_rice.ipynb
```

**Available Notebooks:**
- `eda_rice.ipynb` - Rice production analysis
- `eda_wheat.ipynb` - Wheat production analysis
- `eda_comprehensive.ipynb` - Complete multi-crop analysis




### Step 5: Open Power BI Dashboard

1. Open Power BI Desktop
2. File → Open → `powerbi/AgriDataExplorer.pbix`
3. Update database connection:
   - Home → Transform Data → Data Source Settings
   - Change server/database credentials
4. Refresh data

---






## 📊 Key Analyses Performed

### 1. Top Producing States
- Rice: West Bengal, Uttar Pradesh, Punjab
- Wheat: Uttar Pradesh, Punjab, Haryana
- Oilseeds: Madhya Pradesh, Rajasthan, Gujarat

### 2. Trend Analysis
- 50-year production trends
- Year-over-year growth rates
- Seasonal variations

### 3. Yield Efficiency
- District-wise yield comparisons
- Area vs. production correlation
- Best performing regions

### 4. Regional Insights
- State-wise production patterns
- District-level deep dives
- Geographical heatmaps

---

## 🔍 10 Key Business Questions Answered

1. **Year-wise Trend of Rice Production Across States (Top 3)**
   - Query: `analysis_queries.sql` - Query 1
   - Visualization: Power BI Dashboard

2. **Top 5 Districts by Wheat Yield Increase (Last 5 Years)**
   - Identifies high-growth districts
   - Useful for policy intervention

3. **States with Highest Growth in Oilseed Production**
   - 5-year growth rate analysis
   - Investment opportunity identification

4. **Area-Production Correlation for Major Crops**
   - Rice, Wheat, Maize efficiency
   - District-wise comparison

5. **Yearly Cotton Production Growth (Top 5 States)**
   - Tracks cotton belt performance
   - Year-over-year growth trends

6. **Highest Groundnut Production Districts (2020)**
   - Current year snapshot
   - Regional specialization

7. **Annual Average Maize Yield Across States**
   - National and state-level trends
   - Productivity benchmarking

8. **Total Oilseed Cultivation Area by State**
   - Comprehensive oilseed analysis
   - Crop composition breakdown

9. **Districts with Highest Rice Yield**
   - Top performers identification
   - Best practice replication

10. **Rice vs Wheat Production Comparison (10 Years)**
    - Dual-crop analysis
    - Substitution patterns

---

## 📈 Power BI Dashboard Features

### Pages Included:

1. **Overview Dashboard**
   - KPI cards (Total Production, Area, Yield)
   - National production trends
   - State-wise distribution map

2. **Crop-Specific Analysis**
   - Rice production deep dive
   - Wheat production analysis
   - Oilseeds performance

3. **Regional Comparison**
   - State vs State comparison
   - District rankings
   - Geographical heatmaps

4. **Trend Analysis**
   - 50-year historical trends
   - Growth rate calculations
   - Forecasting (if ML models included)

### Interactive Features:

- **Slicers**: Year, State, District, Crop Type
- **Drill-through**: State → District level
- **Tooltips**: Detailed hover information
- **Cross-filtering**: Click to filter related visuals

---

## 🤖 Machine Learning Models (Optional)

### Crop Yield Forecasting

```python
# Located in models/forecast_train.ipynb

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# Features: Area, Previous yields, State, Year
# Target: Next year's yield
```

### Models Implemented:
- Linear Regression (Baseline)
- Random Forest Regressor
- Gradient Boosting
- Time Series (ARIMA/Prophet)

---

## 📋 Data Dictionary

### Dimension Tables

**dim_state**
| Column | Type | Description |
|--------|------|-------------|
| state_id | INT | Primary key |
| state_code | VARCHAR(10) | Unique state code |
| state_name | VARCHAR(100) | Full state name |

**dim_district**
| Column | Type | Description |
|--------|------|-------------|
| district_id | INT | Primary key |
| district_name | VARCHAR(100) | District name |
| state_id | INT | Foreign key to dim_state |

**dim_year**
| Column | Type | Description |
|--------|------|-------------|
| year_id | INT | Primary key (year value) |
| decade | INT | Decade classification |
| is_recent | BOOLEAN | Year >= 2015 |

### Fact Table

**fact_production**
- All area measurements in **1000 hectares**
- All production in **1000 tons**
- All yields in **kg per hectare**

---

## 🐛 Troubleshooting

### Common Issues

**1. MySQL Connection Error**
```
Error: Can't connect to MySQL server
```
**Solution:**
- Check MySQL service is running
- Verify username/password in `load_to_sql.py`
- Ensure firewall allows port 3306

**2. Power BI Connection Failed**
```
Error: Unable to connect to database
```
**Solution:**
- Install MySQL ODBC Driver
- Update connection string in Power BI
- Test connection in MySQL Workbench first

**3. Missing Python Packages**
```
ModuleNotFoundError: No module named 'pandas'
```
**Solution:**
```bash
pip install -r requirements.txt
```

**4. Memory Error During Data Load**
```
MemoryError: Unable to allocate array
```
**Solution:**
- Process data in chunks (already implemented)
- Increase available RAM
- Use data sampling for testing

---

## 📊 Sample Visualizations

### Generated Outputs

All visualizations are saved in `analysis/plotly_exports/`:

- `top7_rice_states_bar.png`
- `west_bengal_districts_rice.png`
- `india_rice_production_50years.png`
- `rice_vs_wheat_50years.png`
- `rice_yield_efficiency.png`
- `*_interactive.html` (Interactive Plotly charts)

---

## 🤝 Contributing

### How to Contribute

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

### Coding Standards

- Follow PEP 8 for Python code
- Use meaningful variable names
- Comment complex logic
- Write docstrings for functions

---


---

## 📜 License

This project is licensed under the MIT License - @karthika.

---

## 🙏 Acknowledgments

- **ICRISAT** for providing district-level agricultural data
- **Ministry of Agriculture, India** for data validation
- **Power BI Community** for dashboard inspiration
- **Open Source Contributors** for libraries used

---

## 📚 Additional Resources

- [ICRISAT Data Documentation](https://dataverse.harvard.edu/)
- [Power BI Documentation](https://docs.microsoft.com/power-bi/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

---

## 🎓 Learning Outcomes

By completing this project, you will have learned:

✅ **Data Engineering**
- ETL pipeline development
- Database design and normalization
- Data quality assurance

✅ **Data Analysis**
- Exploratory Data Analysis (EDA)
- Statistical analysis
- Trend identification

✅ **Data Visualization**
- Creating effective visualizations
- Dashboard design principles
- Interactive storytelling

✅ **Business Intelligence**
- Translating data to insights
- KPI definition and tracking
- Executive-level reporting

✅ **Technical Skills**
- Python scripting
- SQL query optimization
- Power BI development
- Git version control

---

**Last Updated**: November 2024  
**Version**: 1.0.0

---

## 🚀 Next Steps

1. **Enhancements**
   - Add weather data integration
   - Include soil quality metrics
   - Implement real-time data updates

2. **Advanced Analytics**
   - Crop recommendation system
   - Price prediction models
   - Risk assessment tools

3. **Deployment**
   - Cloud hosting (AWS/Azure)
   - Web application development
   - Mobile app integration

---

*Made with ❤️ for Indian Agriculture*