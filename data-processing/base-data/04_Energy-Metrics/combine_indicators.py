import pandas as pd
import numpy as np

def parse_eurostat_tsv(filepath, indicator_name):
    """Parse Eurostat TSV format and add indicator column"""
    try:
        df = pd.read_csv(filepath, sep='\t')
    except FileNotFoundError:
        df = pd.read_csv('../../raw-data/electricity_indicators_eurostat/' + filepath, sep='\t')
    first_col = df.columns[0]
    dim_names = first_col.replace('\\TIME_PERIOD', '').split(',')
    split_dims = df[first_col].str.split(',', expand=True)
    split_dims.columns = dim_names
    year_cols = [c for c in df.columns if c != first_col]
    result = pd.concat([split_dims, df[year_cols]], axis=1)
    result['indicator'] = indicator_name
    # Clean column names (strip whitespace)
    result.columns = [c.strip() if isinstance(c, str) else c for c in result.columns]
    return result

print('Loading and parsing all datasets...')
re = parse_eurostat_tsv('estat_nrg_ind_re.tsv', 'RE')      # Rate of electrification
eff = parse_eurostat_tsv('estat_nrg_ind_eff.tsv', 'EFF')   # Energy efficiency
ei = parse_eurostat_tsv('estat_nrg_ind_ei.tsv', 'EI')      # Energy intensity
esc = parse_eurostat_tsv('estat_nrg_ind_esc.tsv', 'ESC')   # Energy supply per capita

print(f'RE: {re.shape}, columns: {list(re.columns[:6])}...')
print(f'EFF: {eff.shape}, columns: {list(eff.columns[:6])}...')
print(f'EI: {ei.shape}, columns: {list(ei.columns[:6])}...')
print(f'ESC: {esc.shape}, columns: {list(esc.columns[:6])}...')

# Add 'siec' column to datasets that don't have it (set to 'TOTAL' or NA)
re['siec'] = 'TOTAL'
eff['siec'] = 'TOTAL'
ei['siec'] = 'TOTAL'
# esc already has siec

# Get all unique years across all datasets
all_years = set()
for df in [re, eff, ei, esc]:
    year_cols = [c for c in df.columns if c.isdigit()]
    all_years.update(year_cols)
all_years = sorted(all_years)
print(f'All years: {all_years[0]} to {all_years[-1]} ({len(all_years)} years)')

# Add missing year columns to each dataset
for df in [re, eff, ei, esc]:
    for year in all_years:
        if year not in df.columns:
            df[year] = np.nan

# Define common columns for final output
common_cols = ['indicator', 'freq', 'siec', 'nrg_bal', 'unit', 'geo']

# Select and reorder columns
def prepare_df(df):
    cols = common_cols + all_years
    return df[cols]

re_prep = prepare_df(re)
eff_prep = prepare_df(eff)
ei_prep = prepare_df(ei)
esc_prep = prepare_df(esc)

print(f'RE prepared: {re_prep.shape}')
print(f'EFF prepared: {eff_prep.shape}')
print(f'EI prepared: {ei_prep.shape}')
print(f'ESC prepared: {esc_prep.shape}')

# Combine all
combined = pd.concat([re_prep, eff_prep, ei_prep, esc_prep], ignore_index=True)
print(f'Combined wide format: {combined.shape}')

# Melt to long format
id_cols = ['indicator', 'freq', 'siec', 'nrg_bal', 'unit', 'geo']
combined_long = combined.melt(id_vars=id_cols, value_vars=all_years, var_name='year', value_name='value')
print(f'Combined long format: {combined_long.shape}')

# Clean up value column - remove flags and convert to numeric
combined_long['value'] = combined_long['value'].astype(str).str.replace(r'[a-z]', '', regex=True).str.strip()
combined_long['value'] = combined_long['value'].replace([':', ''], np.nan)
combined_long['value'] = pd.to_numeric(combined_long['value'], errors='coerce')

# Convert year to integer
combined_long['year'] = combined_long['year'].astype(int)

# Save to CSV
output_path = '../output/combined_electricity_indicators.csv'
combined_long.to_csv(output_path, index=False)
print(f'Saved to: {output_path}')
print(f'Final shape: {combined_long.shape}')
print()
print('Sample rows:')
print(combined_long.head(10).to_string())
print()
print('Indicators breakdown:')
print(combined_long.groupby('indicator').size())
print()
print('Non-null values by indicator:')
print(combined_long.groupby('indicator')['value'].apply(lambda x: x.notna().sum()))
