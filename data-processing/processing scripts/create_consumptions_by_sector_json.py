"""
Create JSON dataset for D3 visualizations of energy imports/exports and dependency metrics.

Input files:
- transport_energy.csv (1283 rows)
- residential_energy.csv (856 rows)
- industrial_energy.csv (917 rows)
- service_energy.csv (673 rows)
1283 + 856 + 917 - 6 = 3050 rows total

Output:
- energy_consumptions_by_sector.json
"""

import pandas as pd
import numpy as np
import json
import time
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# ============================================================================
# Configuration
# ============================================================================

BASE_PATH = Path(__file__).parent.parent / 'raw-data' / 'end_uses_efficiency'

# Estimated row counts for progress calculation (update if data changes)
ESTIMATED_TRADE_ROWS = 4_461
OUTPUT_PATH = Path(__file__).parent.parent / 'prepared-sets'

ENERGY_FILE = BASE_PATH / 'industry_energy.csv'
RESIDENTIAL_FILE = BASE_PATH / 'residential_energy.csv'
TRANSPORT_FILE = BASE_PATH / 'transport_energy.csv'
SERVICE_FILE = BASE_PATH / 'services_energy.csv'

# Country name lookup (ISO 2-letter to full name)
COUNTRY_NAMES = {
    'AD': 'Andorra', 'AE': 'United Arab Emirates', 'AF': 'Afghanistan', 'AL': 'Albania',
    'AM': 'Armenia', 'AO': 'Angola', 'AR': 'Argentina', 'AT': 'Austria', 'AU': 'Australia',
    'AZ': 'Azerbaijan', 'BA': 'Bosnia and Herzegovina', 'BD': 'Bangladesh', 'BE': 'Belgium',
    'BG': 'Bulgaria', 'BH': 'Bahrain', 'BR': 'Brazil', 'BY': 'Belarus', 'CA': 'Canada',
    'CH': 'Switzerland', 'CL': 'Chile', 'CM': 'Cameroon', 'CN': 'Hong Kong (China)', 'CO': 'Colombia',
    'CY': 'Cyprus', 'CZ': 'Czech Republic', 'DE': 'Germany', 'DK': 'Denmark', 'DZ': 'Algeria',
    'EC': 'Ecuador', 'EE': 'Estonia', 'EG': 'Egypt', 'ES': 'Spain',
    'FI': 'Finland', 'FR': 'France', 'GA': 'Gabon', 'GE': 'Georgia',
    'GH': 'Ghana', 'GQ': 'Equatorial Guinea', 'GR': 'Greece', 'HR': 'Croatia', 'HU': 'Hungary',
    'ID': 'Indonesia', 'IE': 'Ireland', 'IL': 'Israel', 'IN': 'India', 'IQ': 'Iraq',
    'IR': 'Iran', 'IS': 'Iceland', 'IT': 'Italy', 'JO': 'Jordan', 'JP': 'Japan',
    'KW': 'Kuwait', 'KZ': 'Kazakhstan', 'LB': 'Lebanon', 'LI': 'Liechtenstein',
    'LT': 'Lithuania', 'LU': 'Luxembourg', 'LV': 'Latvia', 'LY': 'Libya', 'MA': 'Morocco',
    'MD': 'Republic of Moldova', 'ME': 'Montenegro', 'MK': 'Republic of North Macedonia', 'MN': 'Mongolia',
    'MT': 'Malta', 'MX': 'Mexico', 'MY': 'Malaysia', 'MZ': 'Mozambique', 'NG': 'Nigeria',
    'NL': 'Netherlands', 'NO': 'Norway', 'NZ': 'New Zealand', 'OM': 'Oman', 'PE': 'Peru',
    'PH': 'Philippines', 'PK': 'Pakistan', 'PL': 'Poland', 'PT': 'Portugal', 'QA': 'Qatar',
    'RO': 'Romania', 'RS': 'Serbia', 'RU': 'Russia', 'SA': 'Saudi Arabia', 'SD': 'Sudan',
    'SE': 'Sweden', 'SG': 'Singapore', 'SI': 'Slovenia', 'SK': 'Slovak Republic', 'SY': 'Syria',
    'TD': 'Chad', 'TH': 'Thailand', 'TM': 'Turkmenistan', 'TN': 'Tunisia', 'TR': 'Republic of Turkiye',
    'TT': 'Trinidad and Tobago', 'TW': 'Chinese Taipei', 'UA': 'Ukraine', 'UK': 'United Kingdom',
    'US': 'United States', 'UZ': 'Uzbekistan', 'VE': 'Venezuela', 'VN': 'Vietnam',
    'XK': 'Kosovo', 'YE': 'Yemen', 'ZA': 'South Africa', 'KG': 'Kyrgyzstan', 'UY': 'Uruguay', 'KR': 'Korea',
}

ROWS = [
    'Country', 
    'End use', 
    'Product',
    '2000', 
    '2005', 
    '2010', 
    '2015', 
    '2016', 
    '2017', 
    '2018', 
    '2019', 
    '2020', 
    '2021', 
    '2022', 
    '2023'
]

# ============================================================================
# Progress Tracking Utilities
# ============================================================================

def format_time(seconds):
    """Format seconds into human-readable string."""
    if seconds < 60:
        return f'{seconds:.0f}s'
    elif seconds < 3600:
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f'{mins}m {secs}s'
    else:
        hours = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        return f'{hours}h {mins}m'


def print_progress(current, total, start_time, prefix='Progress', bar_length=40):
    """Print a progress bar with ETA."""
    elapsed = time.time() - start_time
    percent = current / total if total > 0 else 0

    # Calculate ETA
    if percent > 0:
        total_estimated = elapsed / percent
        eta = total_estimated - elapsed
        eta_str = format_time(eta)
    else:
        eta_str = 'calculating...'

    # Build progress bar (ASCII compatible for Windows)
    filled = int(bar_length * percent)
    bar = '#' * filled + '-' * (bar_length - filled)

    # Print progress (use \r to overwrite line)
    print(f'\r  {prefix}: [{bar}] {percent*100:5.1f}% | {current:,}/{total:,} | Elapsed: {format_time(elapsed)} | ETA: {eta_str}    ', end='', flush=True)


def print_phase_header(phase_num, title, total_phases=3):
    """Print a phase header with overall progress."""
    print()
    print('=' * 60)
    print(f'PHASE {phase_num}/{total_phases}: {title}')
    print('=' * 60)
    print()

# ============================================================================
# Phase 1: Load Data
# ============================================================================

def load_data():
    print_phase_header(1, 'Loading data')

    def load_csv_clean(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        if lines and lines[0].strip().startswith('Source:'):
            lines = lines[1:]
        if lines and lines[0].strip().startswith('Country'):
            lines = lines[1:]
        import io
        return pd.read_csv(io.StringIO(''.join(lines)), names=ROWS, header=None)

    print('  Loading CSV files...')
    ef = load_csv_clean(ENERGY_FILE)
    rf = load_csv_clean(RESIDENTIAL_FILE)
    tf = load_csv_clean(TRANSPORT_FILE)
    sf = load_csv_clean(SERVICE_FILE)

    ef = ef.dropna(how='all')
    rf = rf.dropna(how='all')
    tf = tf.dropna(how='all')
    sf = sf.dropna(how='all')

    ef['type'] = 'Industry'
    rf['type'] = 'Residential'
    tf['type'] = 'Transport'
    sf['type'] = 'Service'

    data = pd.concat([ef, rf, tf, sf], ignore_index=True)

    print(f'  Loaded {len(data):,} rows from all files')
    return data

# ============================================================================
# Phase 2: Calc Meta Data
# ============================================================================

def get_meta_data(data):
    print_phase_header(2, 'Calculating meta data')

    # Example: Calculate unique end uses per sector
    industry_end_uses = set()
    residential_end_uses = set()
    transport_end_uses = set()
    services_end_uses = set()
    countries = set()

    for _, row in data.iterrows():
        type = row['type']
        enduse = row['End use']
        countries.add(row['Country'].lower())
        if 'Industry' == type:
            industry_end_uses.add(enduse)
        elif 'Residential' == type:
            residential_end_uses.add(enduse)
        elif 'Transport' == type:
            transport_end_uses.add(enduse)
        elif 'Service' == type:
            services_end_uses.add(enduse)

    country_codes = {
        code: country
        for code, country in COUNTRY_NAMES.items()
        if country.lower() in countries
    }

    print(f'  Industry end uses: {len(industry_end_uses)}')
    print(f'  Residential end uses: {len(residential_end_uses)}')
    print(f'  Transport end uses: {len(transport_end_uses)}')
    print(f'  Service end uses: {len(services_end_uses)}')
    print(f'  Countries: {len(countries)}')
    print(f'  Countries with Codes: {len(country_codes)}')
    if( len(countries) != len(country_codes)):
        print(f'  WARNING: Some countries are missing codes! {len(countries) - len(country_codes)} missing.')
        print(f'  Missing countries: {[c for c in countries if c not in [v.lower() for v in country_codes.values()]]}')

    return {
        'industry_end_uses': industry_end_uses,
        'residential_end_uses': residential_end_uses,
        'transport_end_uses': transport_end_uses,
        'service_end_uses': services_end_uses,
        'country_codes': country_codes,
    }

# ============================================================================
# Phase 3: Build JSON Structure
# ============================================================================

def build_json_output(data, meta_data):
    print_phase_header(3, 'Building JSON output')

    # Get all countries and years
    all_countries = sorted(set(data['Country'].values))
    all_years = ['2000', '2005', '2010', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023']
    print(f'  Countries: {len(all_countries)}, Years: {all_years[0]}-{all_years[-1]}')

    # Build country data 'AU' -> {residential: {'year': {'end_use': {'product': Total final use (PJ), 'value': 59.74}}}, industry: y, transport: z}
    countries = {}
    for country in all_countries:
        countries[country] = {}
        country_data = data[data['Country'] == country]
        for _, row in country_data.iterrows():
            type = row['type']
            end_use = row['End use']
            if type not in countries[country]:
                countries[country][type] = {}
            for year in all_years:
                if year not in countries[country][type]:
                    countries[country][type][year] = {}
                val = None if pd.isna(row[str(year)]) or str(row[str(year)]).strip() == '..' else float(row[str(year)])
                if end_use not in countries[country][type][year]:
                    countries[country][type][year][end_use] = {'products': {}}
                if val is not None:
                    countries[country][type][year][end_use]['products'][row['Product']] = val

    sorted_countries = sorted(all_countries)
    total_countries = len(sorted_countries)

    # Build final output
    output = {
        'metadata': {
            'generated': datetime.now().isoformat(),
            'sources': [
                'IEA Energy End-uses and Efficiency Indicators Database - Highlights'
            ],
            'time_range': str(all_years[0]) + " - " + str(all_years[-1]),
            'total_countries': total_countries,
            'industries_end_uses': list(meta_data['industry_end_uses']),
            'residential_end_uses': list(meta_data['residential_end_uses']),
            'transport_end_uses': list(meta_data['transport_end_uses']),
            'service_end_uses': list(meta_data['service_end_uses']),
        },
        'countries': countries,
        'country_lookup': {k: v for k, v in meta_data['country_codes'].items() if k in meta_data['country_codes']},
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
    output_file = OUTPUT_PATH / 'energy_consumptions_by_sector.json'
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
