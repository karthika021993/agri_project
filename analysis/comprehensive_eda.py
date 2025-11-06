"""
AgriData Explorer - Comprehensive EDA
File: analysis/comprehensive_eda.py
Purpose: Generate all 15 required visualizations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import warnings
warnings.filterwarnings('ignore')

# Configuration
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")
OUTPUT_DIR = 'plotly_exports'
os.makedirs(OUTPUT_DIR, exist_ok=True)

class AgriEDAVisualizer:
    """Generate all required EDA visualizations"""
    
    def __init__(self, data_path):
        self.df = pd.read_csv(data_path)
        print(f"✓ Data loaded: {self.df.shape}")
        print(f"✓ Years covered: {self.df['year'].min()} - {self.df['year'].max()}")
        
        # Auto-detect column names (handle different naming conventions)
        self.col_map = self._detect_columns()
    
    def _detect_columns(self):
        """Detect actual column names in the dataset"""
        col_map = {}
        
        # Map expected names to actual column names
        patterns = {
            'rice_production': ['rice_production', 'rice production'],
            'rice_area': ['rice_area', 'rice area'],
            'rice_yield': ['rice_yield', 'rice yield'],
            'wheat_production': ['wheat_production', 'wheat production'],
            'wheat_area': ['wheat_area', 'wheat area'],
            'wheat_yield': ['wheat_yield', 'wheat yield'],
            'maize_production': ['maize_production', 'maize production'],
            'maize_area': ['maize_area', 'maize area'],
            'maize_yield': ['maize_yield', 'maize yield'],
            'sorghum_production': ['sorghum_production', 'sorghum production'],
            'sorghum_area': ['sorghum_area', 'sorghum area'],
            'soybean_production': ['soybean_production', 'soybean production'],
            'soybean_area': ['soybean_area', 'soybean area'],
            'soybean_yield': ['soybean_yield', 'soybean yield'],
            'groundnut_production': ['groundnut_production', 'groundnut production'],
            'sunflower_production': ['sunflower_production', 'sunflower production'],
            'oilseeds_production': ['oilseeds_production', 'oilseed', 'oil seed'],
            'sugarcane_production': ['sugarcane_production', 'sugarcane production'],
            'cotton_production': ['cotton_production', 'cotton production'],
            'pearl_millet_production': ['pearl_millet_production', 'pearl millet production'],
            'finger_millet_production': ['finger_millet_production', 'finger millet production'],
            'rapeseed_mustard_production': ['rapeseed_mustard', 'rapeseed and mustard']
        }
        
        # Find matching columns
        for key, patterns_list in patterns.items():
            for pattern in patterns_list:
                matching = [col for col in self.df.columns if pattern.lower() in col.lower()]
                if matching:
                    col_map[key] = matching[0]
                    break
        
        return col_map
    
    def _get_col(self, key):
        """Get actual column name from map"""
        return self.col_map.get(key, key)
    
    def eda_1_top7_rice_states(self):
        """EDA 1: Top 7 Rice Production States (Bar Plot)"""
        print("\n" + "="*70)
        print("EDA 1: Top 7 Rice Producing States")
        print("="*70)
        
        col = self._get_col('rice_production')
        state_rice = self.df.groupby('state_name')[col].sum()
        top7 = state_rice.nlargest(7)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        top7.plot(kind='bar', color='#2ecc71', edgecolor='black', ax=ax)
        ax.set_title('Top 7 Rice Producing States in India', fontsize=16, fontweight='bold')
        ax.set_xlabel('State', fontsize=12)
        ax.set_ylabel('Rice Production (1000 tons)', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(f'{OUTPUT_DIR}/01_top7_rice_states.png', dpi=300)
        plt.close()
        
        print(top7)
        return top7
    
    def eda_2_top5_wheat_states(self):
        """EDA 2: Top 5 Wheat Producing States (Bar + Pie Chart)"""
        print("\n" + "="*70)
        print("EDA 2: Top 5 Wheat Producing States")
        print("="*70)
        
        state_wheat = self.df.groupby('state_name')['wheat_production_1000_tons'].sum()
        top5 = state_wheat.nlargest(5)
        
        # Bar Chart
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        top5.plot(kind='bar', color='#e74c3c', edgecolor='black', ax=ax1)
        ax1.set_title('Top 5 Wheat Producing States', fontsize=14, fontweight='bold')
        ax1.set_xlabel('State', fontsize=12)
        ax1.set_ylabel('Wheat Production (1000 tons)', fontsize=12)
        ax1.tick_params(axis='x', rotation=45)
        
        # Pie Chart
        colors = ['#e74c3c', '#e67e22', '#f39c12', '#f1c40f', '#d35400']
        ax2.pie(top5.values, labels=top5.index, autopct='%1.1f%%', 
               startangle=90, colors=colors, explode=[0.05]*5)
        ax2.set_title('Wheat Production Share (%)', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(f'{OUTPUT_DIR}/02_top5_wheat_states.png', dpi=300)
        plt.close()
        
        print(top5)
        return top5
    
    def eda_3_oilseed_top5_states(self):
        """EDA 3: Oilseed Production by Top 5 States"""
        print("\n" + "="*70)
        print("EDA 3: Oilseed Production by Top 5 States")
        print("="*70)
        
        state_oil = self.df.groupby('state_name')['oilseeds_production_1000_tons'].sum()
        top5 = state_oil.nlargest(5)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        top5.plot(kind='barh', color='#f39c12', edgecolor='black', ax=ax)
        ax.set_title('Top 5 Oilseed Producing States', fontsize=16, fontweight='bold')
        ax.set_xlabel('Oilseed Production (1000 tons)', fontsize=12)
        ax.set_ylabel('State', fontsize=12)
        plt.tight_layout()
        plt.savefig(f'{OUTPUT_DIR}/03_top5_oilseed_states.png', dpi=300)
        plt.close()
        
        print(top5)
        return top5
    
    def eda_4_top7_sunflower_states(self):
        """EDA 4: Top 7 Sunflower Production States"""
        print("\n" + "="*70)
        print("EDA 4: Top 7 Sunflower Production States")
        print("="*70)
        
        state_sun = self.df.groupby('state_name')['sunflower_production_1000_tons'].sum()
        top7 = state_sun.nlargest(7)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        top7.plot(kind='bar', color='#f1c40f', edgecolor='black', ax=ax)
        ax.set_title('Top 7 Sunflower Producing States', fontsize=16, fontweight='bold')
        ax.set_xlabel('State', fontsize=12)
        ax.set_ylabel('Sunflower Production (1000 tons)', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(f'{OUTPUT_DIR}/04_top7_sunflower_states.png', dpi=300)
        plt.close()
        
        print(top7)
        return top7
    
    def eda_5_sugarcane_50years(self):
        """EDA 5: India's Sugarcane Production (Last 50 Years)"""
        print("\n" + "="*70)
        print("EDA 5: Sugarcane Production Over 50 Years")
        print("="*70)
        
        yearly = self.df.groupby('year')['sugarcane_production_1000_tons'].sum()
        
        fig, ax = plt.subplots(figsize=(14, 7))
        ax.plot(yearly.index, yearly.values, marker='o', linewidth=2.5, 
               markersize=6, color='#16a085')
        ax.fill_between(yearly.index, yearly.values, alpha=0.3, color='#16a085')
        ax.set_title("India's Sugarcane Production (Last 50 Years)", 
                    fontsize=16, fontweight='bold')
        ax.set_xlabel('Year', fontsize=12)
        ax.set_ylabel('Sugarcane Production (1000 tons)', fontsize=12)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'{OUTPUT_DIR}/05_sugarcane_50years.png', dpi=300)
        plt.close()
        
        print(f"Growth: {((yearly.iloc[-1] / yearly.iloc[0]) - 1) * 100:.2f}%")
        return yearly
    
    def eda_6_rice_vs_wheat_50years(self):
        """EDA 6: Rice vs Wheat Production (Last 50 Years)"""
        print("\n" + "="*70)
        print("EDA 6: Rice vs Wheat Production Comparison")
        print("="*70)
        
        yearly = self.df.groupby('year').agg({
            'rice_production_1000_tons': 'sum',
            'wheat_production_1000_tons': 'sum'
        })
        
        fig, ax = plt.subplots(figsize=(14, 7))
        ax.plot(yearly.index, yearly['rice_production_1000_tons'], 
               marker='o', linewidth=2.5, label='Rice', color='#27ae60')
        ax.plot(yearly.index, yearly['wheat_production_1000_tons'], 
               marker='s', linewidth=2.5, label='Wheat', color='#e67e22')
        ax.set_title('Rice vs Wheat Production in India (50 Years)', 
                    fontsize=16, fontweight='bold')
        ax.set_xlabel('Year', fontsize=12)
        ax.set_ylabel('Production (1000 tons)', fontsize=12)
        ax.legend(fontsize=12)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'{OUTPUT_DIR}/06_rice_vs_wheat_50years.png', dpi=300)
        plt.close()
        
        return yearly
    
    def eda_7_wb_districts_rice(self):
        """EDA 7: Rice Production by West Bengal Districts"""
        print("\n" + "="*70)
        print("EDA 7: West Bengal Districts Rice Production")
        print("="*70)
        
        wb = self.df[self.df['state_name'] == 'West Bengal']
        dist_rice = wb.groupby('district_name')['rice_production_1000_tons'].sum()
        top10 = dist_rice.nlargest(10)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        top10.plot(kind='barh', color='#3498db', edgecolor='black', ax=ax)
        ax.set_title('Top 10 Rice Producing Districts in West Bengal', 
                    fontsize=16, fontweight='bold')
        ax.set_xlabel('Rice Production (1000 tons)', fontsize=12)
        ax.set_ylabel('District', fontsize=12)
        plt.tight_layout()
        plt.savefig(f'{OUTPUT_DIR}/07_wb_districts_rice.png', dpi=300)
        plt.close()
        
        print(top10)
        return top10
    
    def eda_8_up_wheat_top10_years(self):
        """EDA 8: Top 10 Wheat Production Years from UP"""
        print("\n" + "="*70)
        print("EDA 8: Top 10 Wheat Production Years in Uttar Pradesh")
        print("="*70)
        
        up = self.df[self.df['state_name'] == 'Uttar Pradesh']
        yearly = up.groupby('year')['wheat_production_1000_tons'].sum()
        top10 = yearly.nlargest(10)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        top10.plot(kind='bar', color='#e74c3c', edgecolor='black', ax=ax)
        ax.set_title('Top 10 Wheat Production Years in Uttar Pradesh', 
                    fontsize=16, fontweight='bold')
        ax.set_xlabel('Year', fontsize=12)
        ax.set_ylabel('Wheat Production (1000 tons)', fontsize=12)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'{OUTPUT_DIR}/08_up_wheat_top10_years.png', dpi=300)
        plt.close()
        
        print(top10)
        return top10
    
    def eda_9_millet_50years(self):
        """EDA 9: Millet Production (Last 50 Years)"""
        print("\n" + "="*70)
        print("EDA 9: Millet Production Over 50 Years")
        print("="*70)
        
        # Combine all millets
        yearly = self.df.groupby('year').agg({
            'pearl_millet_production_1000_tons': 'sum',
            'finger_millet_production_1000_tons': 'sum'
        })
        yearly['total_millet'] = yearly.sum(axis=1)
        
        fig, ax = plt.subplots(figsize=(14, 7))
        ax.plot(yearly.index, yearly['pearl_millet_production_1000_tons'], 
               marker='o', label='Pearl Millet', linewidth=2)
        ax.plot(yearly.index, yearly['finger_millet_production_1000_tons'], 
               marker='s', label='Finger Millet', linewidth=2)
        ax.plot(yearly.index, yearly['total_millet'], 
               marker='^', label='Total Millet', linewidth=2.5, color='black')
        ax.set_title('Millet Production Trends (50 Years)', fontsize=16, fontweight='bold')
        ax.set_xlabel('Year', fontsize=12)
        ax.set_ylabel('Production (1000 tons)', fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'{OUTPUT_DIR}/09_millet_50years.png', dpi=300)
        plt.close()
        
        return yearly
    
    def eda_10_sorghum_by_region(self):
        """EDA 10: Sorghum Production by Region"""
        print("\n" + "="*70)
        print("EDA 10: Sorghum Production by Region")
        print("="*70)
        
        state_sorghum = self.df.groupby('state_name')['sorghum_production_1000_tons'].sum()
        top8 = state_sorghum.nlargest(8)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        top8.plot(kind='bar', color='#9b59b6', edgecolor='black', ax=ax)
        ax.set_title('Top 8 Sorghum Producing States', fontsize=16, fontweight='bold')
        ax.set_xlabel('State', fontsize=12)
        ax.set_ylabel('Sorghum Production (1000 tons)', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(f'{OUTPUT_DIR}/10_sorghum_by_region.png', dpi=300)
        plt.close()
        
        print(top8)
        return top8
    
    def eda_11_groundnut_top7(self):
        """EDA 11: Top 7 States for Groundnut Production"""
        print("\n" + "="*70)
        print("EDA 11: Top 7 Groundnut Producing States")
        print("="*70)
        
        state_gnut = self.df.groupby('state_name')['groundnut_production_1000_tons'].sum()
        top7 = state_gnut.nlargest(7)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        top7.plot(kind='bar', color='#d35400', edgecolor='black', ax=ax)
        ax.set_title('Top 7 Groundnut Producing States', fontsize=16, fontweight='bold')
        ax.set_xlabel('State', fontsize=12)
        ax.set_ylabel('Groundnut Production (1000 tons)', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(f'{OUTPUT_DIR}/11_groundnut_top7.png', dpi=300)
        plt.close()
        
        print(top7)
        return top7
    
    def eda_12_soybean_top5_yield(self):
        """EDA 12: Soybean Production by Top 5 States and Yield Efficiency"""
        print("\n" + "="*70)
        print("EDA 12: Soybean Production and Yield Efficiency")
        print("="*70)
        
        # Check if soybean columns exist
        soy_prod_cols = [c for c in self.df.columns if 'soybean' in c.lower() and 'production' in c.lower()]
        soy_yield_cols = [c for c in self.df.columns if 'soybean' in c.lower() and 'yield' in c.lower()]
        
        if not soy_prod_cols:
            print("⚠️  Soybean production column not found. Skipping...")
            print("Available oilseed crops:")
            oilseed_cols = [c for c in self.df.columns if any(x in c.lower() for x in ['groundnut', 'sunflower', 'rapeseed', 'mustard'])]
            for col in oilseed_cols[:5]:
                print(f"  - {col}")
            return None
        
        prod_col = soy_prod_cols[0]
        yield_col = soy_yield_cols[0] if soy_yield_cols else None
        
        if yield_col:
            state_soy = self.df.groupby('state_name').agg({
                prod_col: 'sum',
                yield_col: 'mean'
            })
            top5 = state_soy.nlargest(5, prod_col)
        else:
            state_soy = self.df.groupby('state_name')[prod_col].sum()
            top5 = state_soy.nlargest(5).to_frame()
            top5['avg_yield'] = 0
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        top5[prod_col].plot(kind='bar', color='#1abc9c', 
                            edgecolor='black', ax=ax1)
        ax1.set_title('Top 5 Soybean Producing States', fontsize=14, fontweight='bold')
        ax1.set_xlabel('State', fontsize=12)
        ax1.set_ylabel('Production (1000 tons)', fontsize=12)
        ax1.tick_params(axis='x', rotation=45)
        
        if yield_col:
            top5[yield_col].plot(kind='bar', color='#16a085', 
                                edgecolor='black', ax=ax2)
            ax2.set_title('Average Soybean Yield', fontsize=14, fontweight='bold')
            ax2.set_xlabel('State', fontsize=12)
            ax2.set_ylabel('Yield (kg/ha)', fontsize=12)
            ax2.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig(f'{OUTPUT_DIR}/12_soybean_top5_yield.png', dpi=300)
        plt.close()
        
        print(top5)
        return top5
    
    def eda_13_oilseed_major_states(self):
        """EDA 13: Oilseed Production in Major States"""
        print("\n" + "="*70)
        print("EDA 13: Oilseed Production in Major States")
        print("="*70)
        
        # Find available oilseed columns
        oilseed_crops = {}
        for crop in ['groundnut', 'soybean', 'sunflower', 'rapeseed']:
            cols = [c for c in self.df.columns if crop in c.lower() and 'production' in c.lower()]
            if cols:
                oilseed_crops[crop] = cols[0]
        
        if not oilseed_crops:
            print("⚠️  No oilseed columns found. Skipping...")
            return None
        
        state_oil = self.df.groupby('state_name')[list(oilseed_crops.values())].sum()
        top5_states = state_oil.sum(axis=1).nlargest(5).index
        plot_data = state_oil.loc[top5_states]
        
        fig, ax = plt.subplots(figsize=(14, 7))
        plot_data.plot(kind='bar', stacked=True, ax=ax, edgecolor='black')
        ax.set_title('Oilseed Composition in Major States', fontsize=16, fontweight='bold')
        ax.set_xlabel('State', fontsize=12)
        ax.set_ylabel('Production (1000 tons)', fontsize=12)
        ax.legend(title='Crop', labels=list(oilseed_crops.keys()), bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(f'{OUTPUT_DIR}/13_oilseed_major_states.png', dpi=300)
        plt.close()
        
        print(plot_data)
        return plot_data
    
    def eda_14_area_vs_production(self):
        """EDA 14: Impact of Area Cultivated on Production (Rice, Wheat, Maize)"""
        print("\n" + "="*70)
        print("EDA 14: Area vs Production Correlation")
        print("="*70)
        
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))
        
        crops = [
            ('rice_area_1000_ha', 'rice_production_1000_tons', 'Rice', '#27ae60'),
            ('wheat_area_1000_ha', 'wheat_production_1000_tons', 'Wheat', '#e67e22'),
            ('maize_area_1000_ha', 'maize_production_1000_tons', 'Maize', '#f39c12')
        ]
        
        for idx, (area_col, prod_col, crop_name, color) in enumerate(crops):
            data = self.df[[area_col, prod_col]].dropna()
            data = data[(data[area_col] > 0) & (data[prod_col] > 0)]
            
            axes[idx].scatter(data[area_col], data[prod_col], alpha=0.5, color=color)
            axes[idx].set_title(f'{crop_name}: Area vs Production', fontsize=14, fontweight='bold')
            axes[idx].set_xlabel('Area (1000 ha)', fontsize=11)
            axes[idx].set_ylabel('Production (1000 tons)', fontsize=11)
            axes[idx].grid(True, alpha=0.3)
            
            # Add correlation
            corr = data[area_col].corr(data[prod_col])
            axes[idx].text(0.05, 0.95, f'Corr: {corr:.3f}', 
                          transform=axes[idx].transAxes, fontsize=12,
                          verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        plt.tight_layout()
        plt.savefig(f'{OUTPUT_DIR}/14_area_vs_production.png', dpi=300)
        plt.close()
        
        return None
    
    def eda_15_rice_wheat_yield_states(self):
        """EDA 15: Rice vs Wheat Yield Across States"""
        print("\n" + "="*70)
        print("EDA 15: Rice vs Wheat Yield Across States")
        print("="*70)
        
        state_yields = self.df.groupby('state_name').agg({
            'rice_yield_kg_per_ha': 'mean',
            'wheat_yield_kg_per_ha': 'mean'
        }).dropna()
        
        # Filter top states
        state_yields['total_yield'] = state_yields.sum(axis=1)
        top10 = state_yields.nlargest(10, 'total_yield')
        
        fig, ax = plt.subplots(figsize=(14, 7))
        x = np.arange(len(top10))
        width = 0.35
        
        ax.bar(x - width/2, top10['rice_yield_kg_per_ha'], width, 
              label='Rice', color='#27ae60', edgecolor='black')
        ax.bar(x + width/2, top10['wheat_yield_kg_per_ha'], width, 
              label='Wheat', color='#e67e22', edgecolor='black')
        
        ax.set_title('Rice vs Wheat Yield: Top 10 States', fontsize=16, fontweight='bold')
        ax.set_xlabel('State', fontsize=12)
        ax.set_ylabel('Yield (kg/ha)', fontsize=12)
        ax.set_xticks(x)
        ax.set_xticklabels(top10.index, rotation=45, ha='right')
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{OUTPUT_DIR}/15_rice_wheat_yield_states.png', dpi=300)
        plt.close()
        
        print(top10)
        return top10
    
    def generate_all_visualizations(self):
        """Generate all 15 required visualizations"""
        print("\n" + "🌾"*35)
        print("AGRIDATA EXPLORER - COMPREHENSIVE EDA")
        print("🌾"*35)
        
        self.eda_1_top7_rice_states()
        self.eda_2_top5_wheat_states()
        self.eda_3_oilseed_top5_states()
        self.eda_4_top7_sunflower_states()
        self.eda_5_sugarcane_50years()
        self.eda_6_rice_vs_wheat_50years()
        self.eda_7_wb_districts_rice()
        self.eda_8_up_wheat_top10_years()
        self.eda_9_millet_50years()
        self.eda_10_sorghum_by_region()
        self.eda_11_groundnut_top7()
        self.eda_12_soybean_top5_yield()
        self.eda_13_oilseed_major_states()
        self.eda_14_area_vs_production()
        self.eda_15_rice_wheat_yield_states()
        
        print("\n" + "="*70)
        print("✓ ALL 15 VISUALIZATIONS GENERATED SUCCESSFULLY!")
        print(f"✓ Saved to: {OUTPUT_DIR}/")
        print("="*70)

# Main execution
if __name__ == "__main__":
    # Path to cleaned data
    DATA_PATH = '../data/processed/agri_data_cleaned.csv'
    
    # Create visualizer and generate all plots
    visualizer = AgriEDAVisualizer(DATA_PATH)
    visualizer.generate_all_visualizations()
    
    print("\n🎉 Project EDA Complete! Ready for Power BI integration.")