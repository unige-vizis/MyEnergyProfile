"""
Create JSON dataset for D3 visualizations of energy prices.
https://github.com/MilesIParker/EnergyCPI?tab=readme-ov-file
https://www.sciencedirect.com/science/article/pii/S0140988324003530

https://databank.worldbank.org/embed/Electric-Prices-by-Country/id/7b12e700?utm_source=chatgpt.com

Input files:
- energycpiq.csv (9825 rows)
- Electric-Prices-by-Country.csv (3057 rows)

Output:
- energy_prices.json
"""

import pandas as pd
import json
import pycountry
from pathlib import Path
from datetime import datetime

# ============================================================================
# Configuration
# ============================================================================

BASE_PATH = Path(__file__).parent.parent / 'raw-data' / 'energy_prices'

# Estimated row counts for progress calculation (update if data changes)
ESTIMATED_TRADE_ROWS = 4_461
OUTPUT_PATH = Path(__file__).parent.parent / 'prepared-sets'

ENERGYCLPQ = BASE_PATH / 'energycpiq.csv'
ELECTRICITYPRICESBYCOUNTRY = BASE_PATH / 'Electric-Prices-by-Country.csv'

# Country name lookup (ISO 2-letter to full name)
COUNTRY_NAMES = { 'BA': 'Bosnia-Herzegovina', 'KR': ['Korea Rep', 'Korea, Rep.'], 'GM': 'Gambia, The', 'MK': 'N Macedonia', 
                 'EX': 'ECCU', 'EU': 'Euro Area', 'TR': 'Turkey', 'BS': 'Bahamas, The', 'CD': 'Congo, Dem. Rep.',
                 'CG': 'Congo, Rep.', 'CI': "C�te d'Ivoire", 'EG': 'Egypt, Arab Rep.', 'GM': 'Gambia, The',
                 'HK': 'Hong Kong, China', 'IR': 'Iran, Islamic Rep.', 'LA': 'Lao PDR', 'FM': 'Micronesia, Fed. Sts.',
                 'ST': 'S�o Tom� and Principe', 'KN': 'St. Kitts and Nevis', 'LC': 'St. Lucia', 'VC': 'St. Vincent and the Grenadines',
                 'TW': 'Taiwan, China', 'VE': 'Venezuela, RB', 'YE': 'Yemen, Rep.'
}

ROWS = [
    'Country', 'Year', 
    '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2010', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024'
]

QUATERS = range(1, 5) # four quarters per year in energycpiq.csv

# Variable name	    COICOP code	    Series name
# CPI0450	        04.5.0	        Electricity, gas and other fuels
# CPI0451	        04.5.1	        Electricity
# CPI0452	        04.5.2	        Gas (including piped and bottled)
# CPI0453	        05.5.3	        Liquid fuels (e.g. kerosene)
# CPI0454	        04.5.4	        Solid fuels (e.g. coal, coke, wood)
# CPI0455	        04.5.5	        Other energy for heating and cooling (e.g. district heating)
# CPI0722	        07.2.2	        Fuels and lubricants for personal transport equipment
# CPIENRG	        n.a.	        Energy — combining 04.5.0 and 07.2.2
# CPIFUELIGHT	    n.a.	        Fuel and light, a non-COICOP grouping that is close to 04.5.0
ENERGY_SERIES = [ 'CPI0450', 'CPI0451', 'CPI0452', 'CPI0453', 'CPI0454', 'CPI0455', 'CPI0722', 'CPIENRG', 'CPIFUELIGHT' ]

# ============================================================================
# Phase 1: Load Data
# ============================================================================

def load_data():
    print('  Loading CSV files...')
    energyPrices = pd.read_csv(ENERGYCLPQ)
    electricityPrices = pd.read_csv(ELECTRICITYPRICESBYCOUNTRY)
    energyPrices = energyPrices.dropna(how='all')
    
    # Get the electricity price column (handle line breaks in column name)
    price_col = [col for col in electricityPrices.columns if 'Getting electricity' in col][0]
    electricityPrices = electricityPrices.dropna(subset=[price_col], how='any')

    # Rename country column for consistency
    electricityPrices = electricityPrices.rename(columns={'Country Name': 'country'})

    # Replace the country names with the county codes
    energyPrices = normalize_country_name(energyPrices)
    electricityPrices = normalize_country_name(electricityPrices)

    print(f'  Loaded {len(energyPrices):,} rows from ENERGYCLPQ files')
    print(f'  Loaded {len(electricityPrices):,} rows from ELECTRICITYPRICESBYCOUNTRY files')
    return {'energyPrices': energyPrices, 'electricityPrices': electricityPrices, 'price_col': price_col}

def normalize_country_name(data):
    for row in data.itertuples():
        country_name = row.country
        try:
            for code, name in COUNTRY_NAMES.items():
                if isinstance(name, list):
                    for n in name:
                        if n.lower() == country_name.lower():
                            data.at[row.Index, 'country'] = code
                            break
                else:
                    if name.lower() == country_name.lower():
                        data.at[row.Index, 'country'] = code
                        break
            # Direct fuzzy match to ISO code
            if(isinstance(data.at[row.Index, 'country'], str) and len(data.at[row.Index, 'country']) > 2):
                country = pycountry.countries.search_fuzzy(country_name)[0]
                data.at[row.Index, 'country'] = country.alpha_2
        except LookupError:
            print(f"No match for: {country_name}")

    return data

# ============================================================================
# Phase 2: Calc Meta Data
# ============================================================================

def get_meta_data(data):
    country_codes = set()
    for _, row in data['energyPrices'].iterrows():
        country_codes.add(row['country'])
    for _, row in data['electricityPrices'].iterrows():
        country_codes.add(row['country'])

    country_codes_and_names = {
        code: country
        for code, country in COUNTRY_NAMES.items()
        if code in country_codes
    }

    return {
        'energy_series': ENERGY_SERIES,
        'country_codes': country_codes,
        'country_codes_and_names': country_codes_and_names,
    }

# ============================================================================
# Phase 3: Build JSON Structure
# ============================================================================

def build_json_output(data, meta_data):
    # Get all countries and years
    all_countries = meta_data['country_codes']
    all_years = range(1996, 2025) # 1996-2024 inclusive
    print(f'  Countries: {len(all_countries)}, Years: {all_years[0]}-{all_years[-1]}')

    # Get the electricity price column name
    price_col = data['price_col']

    # Origin columns: country,year,IFScode,wbcode,imfadv,euroarea,CPI0450,CPI0451,CPI0452,CPI0453,CPI0454,CPI0455,CPI0722,CPIENRG,CPIFUELIGHT,quarter
    # Build new structure: {name: 'Australia', 1996: {'Price of electricity (US cents per kWh)': '111', 1:{CPI0450: '234', CPI0451: '234', ...},2:{CPI0450: '65',...}}, 1997: {1: {}, 2: {},...}, ...}, {name: '', 1996: {...}...} -> quarters -> energy series
    countries = {}
    for country in all_countries:
        country_data = data['energyPrices'][data['energyPrices']['country'] == country]
        country_entry = {}

        country_elec_prices = data['electricityPrices'][
            data['electricityPrices']['country'] == country
        ]

        for year in all_years:
            year_entry = {}
            row = country_elec_prices[country_elec_prices['Time'] == year]
            if not row.empty:
                value = row[price_col].iloc[0]
                if pd.notna(value):
                    year_entry['Price of electricity (US cents per kWh)'] = round(float(value), 2)

            year_data = country_data[country_data['year'] == year]
            if not year_data.empty:
                for quarter in QUATERS:
                    quarter_data = year_data[year_data['quarter'] == quarter]
                    if quarter_data.empty:
                        continue

                    quarter_entry = {}
                    for series in meta_data['energy_series']:
                        value = quarter_data.iloc[0][series]
                        if pd.notna(value):
                            quarter_entry[series] = round(float(value), 2)

                    if quarter_entry:
                        year_entry[str(quarter)] = quarter_entry

            if year_entry:
                country_entry[str(year)] = year_entry
                
        if country_entry:
            countries[country.title().upper()] = country_entry

    sorted_countries = sorted(all_countries)
    total_countries = len(sorted_countries)

    # Build final output
    output = {
        'metadata': {
            'generated': datetime.now().isoformat(),
            'sources': [
                'EnergyCPI - Global database for energy consumer prices covering 102 countries and 2 currency unions.'
            ],
            'time_range': str(all_years[0]) + " - " + str(all_years[-1]),
            'total_countries': total_countries,
            'energy_series': list(meta_data['energy_series']),
        },
        'countries': countries,
        'country_lookup': {k: v for k, v in meta_data['country_codes_and_names'].items() if k in meta_data['country_codes_and_names']},
    }

    return output

# ============================================================================
# Main
# ============================================================================

def main():
    print('=' * 60)
    print('Consumption JSON Dataset Generator')
    print('=' * 60)
    # Ensure output directory exists
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

    # Phase 1: Load dependency data
    data = load_data()

    # Phase 2: Calc meta data
    meta_data = get_meta_data(data)

    # Phase 3: Build JSON output
    output = build_json_output(data, meta_data)

    # Save output
    output_file = OUTPUT_PATH / 'energy_prices.json'
    print()
    print('=' * 60)
    print('Saving output')
    print('=' * 60)
    print()

    print('  Writing JSON file...')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    file_size = output_file.stat().st_size / (1024 * 1024)
    print(f'  Saved to: {output_file}')
    print(f'  File size: {file_size:.2f} MB')

    # Final summary
    print()
    print('=' * 60)
    print('COMPLETE')
    print('=' * 60)
    print()

if __name__ == '__main__':
    main()
