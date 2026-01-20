import pandas as pd
import numpy as np

def parse_eurostat_tsv(filepath, sector_name):
    try:
        df = pd.read_csv(filepath, sep='\t')
    except FileNotFoundError:
        df = pd.read_csv('../../raw-data/consumption_eurostat_sectors/' + filepath, sep='\t')
    first_col = df.columns[0]
    dim_names = first_col.replace('\\TIME_PERIOD', '').split(',')
    split_dims = df[first_col].str.split(',', expand=True)
    split_dims.columns = dim_names
    year_cols = [c for c in df.columns if c != first_col]
    result = pd.concat([split_dims, df[year_cols]], axis=1)
    result['sector'] = sector_name
    return result, [c.strip() for c in year_cols]

print('Loading and parsing all datasets...')
hh, hh_years = parse_eurostat_tsv('eurostat_household_consumption_2010-2023.tsv', 'HH')
ind, ind_years = parse_eurostat_tsv('eurostat_industry_consumption_2017-2023.tsv', 'IND')
ser, ser_years = parse_eurostat_tsv('eurostat_services_consumption_2020-2023.tsv', 'SER')
tra, tra_years = parse_eurostat_tsv('eurostat_transport_consumption_2020-2023.tsv', 'TRA')

# Rename year columns to remove trailing spaces
for df in [hh, ind, ser, tra]:
    df.columns = [c.strip() if isinstance(c, str) else c for c in df.columns]

# Create unified category column for each
hh['category'] = hh['nrg_bal']
ind['category'] = ind['nace_r2']
ser['category'] = ser['nace_r2']
tra['category'] = tra['tra_mode'] + '|' + tra['nrg_bal']  # Combine both for transport

# Define all possible years
all_years = ['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023']

# Add missing year columns to each dataset
for df in [hh, ind, ser, tra]:
    for year in all_years:
        if year not in df.columns:
            df[year] = np.nan

# Define common columns for final output
common_cols = ['sector', 'freq', 'siec', 'unit', 'geo', 'category']

# Select and reorder columns
def prepare_df(df):
    cols = common_cols + all_years
    return df[cols]

hh_prep = prepare_df(hh)
ind_prep = prepare_df(ind)
ser_prep = prepare_df(ser)
tra_prep = prepare_df(tra)

print(f'HH prepared: {hh_prep.shape}')
print(f'IND prepared: {ind_prep.shape}')
print(f'SER prepared: {ser_prep.shape}')
print(f'TRA prepared: {tra_prep.shape}')

# Combine all
combined = pd.concat([hh_prep, ind_prep, ser_prep, tra_prep], ignore_index=True)
print(f'Combined wide format: {combined.shape}')

# Melt to long format
id_cols = ['sector', 'freq', 'siec', 'unit', 'geo', 'category']
combined_long = combined.melt(id_vars=id_cols, value_vars=all_years, var_name='year', value_name='value')
print(f'Combined long format: {combined_long.shape}')

# Clean up value column - remove flags and convert to numeric
combined_long['value'] = combined_long['value'].astype(str).str.replace(r'[a-z]', '', regex=True).str.strip()
combined_long['value'] = combined_long['value'].replace([':', ''], np.nan)
combined_long['value'] = pd.to_numeric(combined_long['value'], errors='coerce')

# Convert year to integer
combined_long['year'] = combined_long['year'].astype(int)

# Save to CSV
output_path = '../output/eurostat_sector_consumption_combined_2010-2023.csv'
combined_long.to_csv(output_path, index=False)
print(f'Saved to: {output_path}')
print(f'Final shape: {combined_long.shape}')
print()
print('Sample rows:')
print(combined_long.head(10).to_string())
print()
print('Value statistics:')
print(combined_long['value'].describe())
print()
print('Sectors breakdown:')
print(combined_long.groupby('sector').size())