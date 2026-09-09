import os
import pandas as pd
import numpy as np

# Automatically find raw procurement file in root or data/raw directory
file_path = 'government-procurement-via-gebiz.csv'
if not os.path.exists(file_path) and os.path.exists('data/raw/government-procurement-via-gebiz.csv'):
    file_path = 'data/raw/government-procurement-via-gebiz.csv'

print(f"Loading raw spend dataset from: {file_path}")
gebiz = pd.read_csv(file_path)

print("Aggregating total spend and order counts per supplier...")
suppliers_df = gebiz.groupby('supplier_name').agg(
    total_spend=('awarded_amt', 'sum'),
    tender_count=('tender_no.', 'count'),
    agencies_count=('agency', 'nunique')
).reset_index()

# Remove unknown vendor rows
suppliers_df = suppliers_df[suppliers_df['supplier_name'] != 'Unknown']

print("Synthesizing realistic performance metrics...")
np.random.seed(42)

# Generate realistic performance scores
suppliers_df['on_time_delivery_pct'] = np.round(
    np.random.normal(loc=88, scale=8, size=len(suppliers_df)), 2
).clip(50.0, 100.0)

suppliers_df['quality_rating'] = np.round(
    np.random.normal(loc=4.1, scale=0.6, size=len(suppliers_df)), 2
).clip(1.0, 5.0)

suppliers_df['cost_competitiveness_score'] = np.round(
    np.random.normal(loc=78, scale=10, size=len(suppliers_df)), 2
).clip(40.0, 100.0)

# Save Master Dataset
output_file = 'Master_Supplier_Performance_Dataset.csv'
suppliers_df.to_csv(output_file, index=False)

print("\n--------------------------------------------------")
print(f"SUCCESS! Master file generated: '{output_file}'")
print(f"Total Unique Suppliers Analyzed: {len(suppliers_df)}")
print("--------------------------------------------------")