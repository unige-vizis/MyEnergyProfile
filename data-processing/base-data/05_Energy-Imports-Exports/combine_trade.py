import pandas as pd
import numpy as np

def parse_eurostat_tsv(filepath, flow_type, energy_type):
    """Parse Eurostat TSV format and add flow/energy columns"""
    try:
        df = pd.read_csv(filepath, sep='\t')
    except FileNotFoundError:
        df = pd.read_csv('../../raw-data/energy_trade_eurostat/' + filepath, sep='\t')
    first_col = df.columns[0]
    dim_names = first_col.replace('\\TIME_PERIOD', '').split(',')
    split_dims = df[first_col].str.split(',', expand=True)
    split_dims.columns = dim_names
    year_cols = [c for c in df.columns if c != first_col]
    result = pd.concat([split_dims, df[year_cols]], axis=1)
    result['flow'] = flow_type
    result['energy_type'] = energy_type
    result.columns = [c.strip() if isinstance(c, str) else c for c in result.columns]
    return result

# Define all files
files = [
    ('estat_nrg_ti_sff.tsv', 'IMPORT', 'SFF'),   # Solid fossil fuels
    ('estat_nrg_ti_oil.tsv', 'IMPORT', 'OIL'),   # Oil & petroleum
    ('estat_nrg_ti_gas.tsv', 'IMPORT', 'GAS'),   # Natural gas
    ('estat_nrg_ti_bio.tsv', 'IMPORT', 'BIO'),   # Biofuels
    ('estat_nrg_ti_eh.tsv', 'IMPORT', 'EH'),     # Electricity/heat
    ('estat_nrg_te_sff.tsv', 'EXPORT', 'SFF'),
    ('estat_nrg_te_oil.tsv', 'EXPORT', 'OIL'),
    ('estat_nrg_te_gas.tsv', 'EXPORT', 'GAS'),
    ('estat_nrg_te_bio.tsv', 'EXPORT', 'BIO'),
    ('estat_nrg_te_eh.tsv', 'EXPORT', 'EH'),
]

print('Loading and parsing all datasets...')
dfs = []
for filename, flow, energy in files:
    df = parse_eurostat_tsv(filename, flow, energy)
    print(f'  {flow} {energy}: {df.shape[0]:,} rows')
    dfs.append(df)

# Get all unique years
all_years = set()
for df in dfs:
    year_cols = [c for c in df.columns if c.isdigit()]
    all_years.update(year_cols)
all_years = sorted(all_years)
print(f'Year range: {all_years[0]} to {all_years[-1]}')

# Add missing year columns
for df in dfs:
    for year in all_years:
        if year not in df.columns:
            df[year] = np.nan

# Define common columns
common_cols = ['flow', 'energy_type', 'freq', 'siec', 'partner', 'unit', 'geo']

# Prepare and combine
def prepare_df(df):
    return df[common_cols + all_years]

combined = pd.concat([prepare_df(df) for df in dfs], ignore_index=True)
print(f'Combined wide format: {combined.shape[0]:,} rows')

# Melt to long format
combined_long = combined.melt(
    id_vars=common_cols,
    value_vars=all_years,
    var_name='year',
    value_name='value'
)
print(f'Combined long format: {combined_long.shape[0]:,} rows')

# Clean values
combined_long['value'] = combined_long['value'].astype(str).str.replace(r'[a-z]', '', regex=True).str.strip()
combined_long['value'] = combined_long['value'].replace([':', ''], np.nan)
combined_long['value'] = pd.to_numeric(combined_long['value'], errors='coerce')
combined_long['year'] = combined_long['year'].astype(int)

# Save
output_path = 'output/combined_energy_trade.csv'
combined_long.to_csv(output_path, index=False)
print(f'Saved to: {output_path}')
print(f'Final shape: {combined_long.shape[0]:,} rows x {combined_long.shape[1]} columns')
print()

print('Summary by flow & energy_type:')
print(combined_long.groupby(['flow', 'energy_type']).agg(
    rows=('value', 'size'),
    non_null=('value', lambda x: x.notna().sum())
))
