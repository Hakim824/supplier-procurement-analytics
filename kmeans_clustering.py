import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

print("Loading ABC classified dataset...")
df = pd.read_csv('ABC_Classified_Suppliers.csv')

print("Calculating Composite Performance Score (0-100 scale)...")
# Performance Weights: Delivery (40%), Quality (40%), Cost (20%)
w1, w2, w3 = 0.40, 0.40, 0.20

df['composite_score'] = np.round(
    (w1 * (df['on_time_delivery_pct'] / 100.0) +
     w2 * (df['quality_rating'] / 5.0) +
     w3 * (df['cost_competitiveness_score'] / 100.0)) * 100, 2
)

print("Standardizing features and fitting K-Means Clustering...")
feature_cols = [
    'total_spend', 
    'on_time_delivery_pct', 
    'quality_rating', 
    'cost_competitiveness_score', 
    'composite_score'
]

# Standardize numerical features for distance calculation
scaler = StandardScaler()
scaled_features = scaler.fit_transform(df[feature_cols])

# Run K-Means algorithm with k=4 clusters
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df['cluster_id'] = kmeans.fit_predict(scaled_features)

# Save final analytics dataset
output_file = 'Final_Supplier_Analytics_Master.csv'
df.to_csv(output_file, index=False)

print("\n--------------------------------------------------")
print(f"SUCCESS! Master file saved as '{output_file}'")
print("\n--- Cluster Count Summary ---")
print(df['cluster_id'].value_counts())
print("\n--- Preview ---")
print(df[['supplier_name', 'total_spend', 'abc_category', 'composite_score', 'cluster_id']].head())
print("--------------------------------------------------")