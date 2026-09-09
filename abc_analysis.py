import pandas as pd

print("Reading master supplier dataset...")
df = pd.read_csv('Master_Supplier_Performance_Dataset.csv')

# 1. Sort by spend descending
df = df.sort_values(by='total_spend', ascending=False).reset_index(drop=True)

# 2. Calculate cumulative spend percentage
df['cum_spend'] = df['total_spend'].cumsum()
total_spend_sum = df['total_spend'].sum()
df['cum_pct'] = (df['cum_spend'] / total_spend_sum) * 100

# 3. Categorize into ABC
def assign_abc(pct):
    if pct <= 80.0:
        return 'A'
    elif pct <= 95.0:
        return 'B'
    else:
        return 'C'

df['abc_category'] = df['cum_pct'].apply(assign_abc)

# 4. Save classified file
output_file = 'ABC_Classified_Suppliers.csv'
df.to_csv(output_file, index=False)

print("\n--------------------------------------------------")
print(f"SUCCESS! Saved classified dataset as '{output_file}'")
print("\n--- ABC Distribution Summary ---")
print(df['abc_category'].value_counts())
print("--------------------------------------------------")