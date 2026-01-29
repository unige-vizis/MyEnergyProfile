import pandas as pd
import numpy as np

def parse_eurostat_tsv(filepath, indicator_name):
    """Parse Eurostat TSV format and add indicator column"""
    try:
        df = pd.read_csv(filepath, sep='\t')
    except FileNotFoundError:
        df = pd.read_csv('../../raw-data/import_dependency_eurostat/' + filepath, sep='\t')
    first_col = df.columns[0]
    dim_names = first_col.replace('\\TIME_PERIOD', '').split(',')
    split_dims = df[first_col].str.split(',', expand=True)
    split_dims.columns = dim_names
    year_cols = [c for c in df.columns if c != first_col]
    result = pd.concat([split_dims, df[year_cols]], axis=1)
    result['indicator'] = indicator_name
    result.columns = [c.strip() if isinstance(c, str) else c for c in result.columns]
    return result

print('Loading and parsing all datasets...')
id_df = parse_eurostat_tsv('estat_nrg_ind_id.tsv', 'ID')           # General import dependency
id3cf = parse_eurostat_tsv('estat_nrg_ind_id3cf.tsv', 'ID3CF')     # 3rd countries by fuel
idogas = parse_eurostat_tsv('estat_nrg_ind_idogas.tsv', 'IDOGAS')  # Gas by origin
idooil = parse_eurostat_tsv('estat_nrg_ind_idooil.tsv', 'IDOOIL')  # Oil by origin

print(f'ID: {id_df.shape}, columns: {list(id_df.columns[:6])}')
print(f'ID3CF: {id3cf.shape}, columns: {list(id3cf.columns[:6])}')
print(f'IDOGAS: {idogas.shape}, columns: {list(idogas.columns[:6])}')
print(f'IDOOIL: {idooil.shape}, columns: {list(idooil.columns[:6])}')

# Add 'partner' column to ID which doesn't have it
id_df['partner'] = 'TOTAL'

# Get all unique years across all datasets
all_years = set()
for df in [id_df, id3cf, idogas, idooil]:
    year_cols = [c for c in df.columns if c.isdigit()]
    all_years.update(year_cols)
all_years = sorted(all_years)
print(f'All years: {all_years[0]} to {all_years[-1]} ({len(all_years)} years)')

# Add missing year columns to each dataset
for df in [id_df, id3cf, idogas, idooil]:
    for year in all_years:
        if year not in df.columns:
            df[year] = np.nan

# Define common columns for final output
common_cols = ['indicator', 'freq', 'siec', 'partner', 'unit', 'geo']

# Select and reorder columns
def prepare_df(df):
    cols = common_cols + all_years
    return df[cols]

id_prep = prepare_df(id_df)
id3cf_prep = prepare_df(id3cf)
idogas_prep = prepare_df(idogas)
idooil_prep = prepare_df(idooil)

# Combine all
combined = pd.concat([id_prep, id3cf_prep, idogas_prep, idooil_prep], ignore_index=True)
print(f'Combined wide format: {combined.shape}')

# Melt to long format
id_cols = ['indicator', 'freq', 'siec', 'partner', 'unit', 'geo']
combined_long = combined.melt(id_vars=id_cols, value_vars=all_years, var_name='year', value_name='value')
print(f'Combined long format: {combined_long.shape}')

# Clean up value column - remove flags and convert to numeric
combined_long['value'] = combined_long['value'].astype(str).str.replace(r'[a-z]', '', regex=True).str.strip()
combined_long['value'] = combined_long['value'].replace([':', ''], np.nan)
combined_long['value'] = pd.to_numeric(combined_long['value'], errors='coerce')

# Convert year to integer
combined_long['year'] = combined_long['year'].astype(int)

# Save to CSV
output_path = 'output/combined_import_dependency.csv'
combined_long.to_csv(output_path, index=False)
print(f'Saved to: {output_path}')
print(f'Final shape: {combined_long.shape}')
print()
print('Sample rows:')
print(combined_long[combined_long['value'].notna()].head(10).to_string())
print()
print('Indicators breakdown:')
print(combined_long.groupby('indicator').size())
print()
print('Non-null values by indicator:')
print(combined_long.groupby('indicator')['value'].apply(lambda x: x.notna().sum()))
