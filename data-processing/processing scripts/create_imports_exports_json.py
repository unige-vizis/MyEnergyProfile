"""
Create JSON dataset for D3 visualizations of energy imports/exports and dependency metrics.

Input files:
- combined_import_dependency.csv (53K rows) - Dependency % metrics
- combined_energy_trade.csv (31.8M rows) - Import/export volumes by partner

Output:
- energy_imports_exports_dependency.json
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

BASE_PATH = Path(__file__).parent.parent / 'base-data' / '05_Energy-Imports-Exports'

# Estimated row counts for progress calculation (update if data changes)
ESTIMATED_TRADE_ROWS = 31_800_000  # ~31.8M rows in combined_energy_trade.csv
OUTPUT_PATH = Path(__file__).parent.parent / 'prepared-sets'

DEPENDENCY_FILE = BASE_PATH / 'import_dependency_eurostat' / 'output' / 'combined_import_dependency.csv'
TRADE_FILE = BASE_PATH / 'energy_trade_eurostat' / 'output' / 'combined_energy_trade.csv'

# Country name lookup (ISO 2-letter to full name)
COUNTRY_NAMES = {
    'AD': 'Andorra', 'AE': 'United Arab Emirates', 'AF': 'Afghanistan', 'AL': 'Albania',
    'AM': 'Armenia', 'AO': 'Angola', 'AR': 'Argentina', 'AT': 'Austria', 'AU': 'Australia',
    'AZ': 'Azerbaijan', 'BA': 'Bosnia and Herzegovina', 'BD': 'Bangladesh', 'BE': 'Belgium',
    'BG': 'Bulgaria', 'BH': 'Bahrain', 'BR': 'Brazil', 'BY': 'Belarus', 'CA': 'Canada',
    'CH': 'Switzerland', 'CL': 'Chile', 'CM': 'Cameroon', 'CN': 'China', 'CO': 'Colombia',
    'CY': 'Cyprus', 'CZ': 'Czechia', 'DE': 'Germany', 'DK': 'Denmark', 'DZ': 'Algeria',
    'EC': 'Ecuador', 'EE': 'Estonia', 'EG': 'Egypt', 'EL': 'Greece', 'ES': 'Spain',
    'FI': 'Finland', 'FR': 'France', 'GA': 'Gabon', 'GB': 'United Kingdom', 'GE': 'Georgia',
    'GH': 'Ghana', 'GQ': 'Equatorial Guinea', 'GR': 'Greece', 'HR': 'Croatia', 'HU': 'Hungary',
    'ID': 'Indonesia', 'IE': 'Ireland', 'IL': 'Israel', 'IN': 'India', 'IQ': 'Iraq',
    'IR': 'Iran', 'IS': 'Iceland', 'IT': 'Italy', 'JO': 'Jordan', 'JP': 'Japan',
    'KW': 'Kuwait', 'KZ': 'Kazakhstan', 'LB': 'Lebanon', 'LI': 'Liechtenstein',
    'LT': 'Lithuania', 'LU': 'Luxembourg', 'LV': 'Latvia', 'LY': 'Libya', 'MA': 'Morocco',
    'MD': 'Moldova', 'ME': 'Montenegro', 'MK': 'North Macedonia', 'MN': 'Mongolia',
    'MT': 'Malta', 'MX': 'Mexico', 'MY': 'Malaysia', 'MZ': 'Mozambique', 'NG': 'Nigeria',
    'NL': 'Netherlands', 'NO': 'Norway', 'NZ': 'New Zealand', 'OM': 'Oman', 'PE': 'Peru',
    'PH': 'Philippines', 'PK': 'Pakistan', 'PL': 'Poland', 'PT': 'Portugal', 'QA': 'Qatar',
    'RO': 'Romania', 'RS': 'Serbia', 'RU': 'Russia', 'SA': 'Saudi Arabia', 'SD': 'Sudan',
    'SE': 'Sweden', 'SG': 'Singapore', 'SI': 'Slovenia', 'SK': 'Slovakia', 'SY': 'Syria',
    'TD': 'Chad', 'TH': 'Thailand', 'TM': 'Turkmenistan', 'TN': 'Tunisia', 'TR': 'Turkey',
    'TT': 'Trinidad and Tobago', 'TW': 'Taiwan', 'UA': 'Ukraine', 'UK': 'United Kingdom',
    'US': 'United States', 'UZ': 'Uzbekistan', 'VE': 'Venezuela', 'VN': 'Vietnam',
    'XK': 'Kosovo', 'YE': 'Yemen', 'ZA': 'South Africa',
    # Aggregates
    'EU27_2020': 'EU27', 'EA20': 'Euro Area', 'TOTAL': 'Total', 'THRD': 'Third Countries'
}

# SIEC codes to fuel names (comprehensive mapping)
SIEC_TO_FUEL = {
    # Coal and solid fossil fuels
    'C0000X0350-0370': 'coal',
    'C0110': 'anthracite',
    'C0121': 'coking_coal',
    'C0129': 'other_bituminous_coal',
    'C0210': 'lignite',
    'C0220': 'sub_bituminous_coal',
    'C0311': 'patent_fuel',
    'C0320': 'coke',
    'C0330': 'coal_tar',
    'C0340': 'bkb_brown_coal_briquettes',
    'C0350': 'gas_coke',
    'C0360': 'coal_gas',
    'C0370': 'blast_furnace_gas',
    'C0390': 'other_coal_products',
    # Note: SFF_OTH (other_solid_fossil_fuels) excluded - only has third_countries data, no overall

    # Natural gas
    'G3000': 'natural_gas',
    'G3100': 'natural_gas_gaseous',
    'G3200': 'lng',

    # Oil and petroleum
    'O4000XBIO': 'oil',
    'O4100_TOT': 'crude_oil',
    'O4200': 'ngl',
    'O4300': 'refinery_feedstocks',
    'O4400': 'additives_oxygenates',
    'O4500': 'other_hydrocarbons',
    'O4610': 'refinery_gas',
    'O4620': 'ethane',
    'O4630': 'lpg',
    'O4640': 'naphtha',
    'O4651': 'motor_gasoline',
    'O4652': 'aviation_gasoline',
    'O4653': 'gasoline_jet_fuel',
    'O4661': 'kerosene_jet_fuel',
    'O4669': 'other_kerosene',
    'O4671': 'road_diesel',
    'O4672': 'heating_diesel',
    'O4680': 'fuel_oil',
    'O4691': 'white_spirit',
    'O4692': 'lubricants',
    'O4693': 'bitumen',
    'O4694': 'paraffin_waxes',
    'O4695': 'petroleum_coke',
    'O4699': 'other_oil_products',

    # Renewables and other
    'RA000': 'renewables_total',
    'RA100': 'hydro',
    'RA200': 'geothermal',
    'RA300': 'wind',
    'RA410': 'solar_thermal',
    'RA420': 'solar_pv',
    'RA500': 'tide_wave_ocean',
    'R5110-5150_W6000RI': 'biofuels_solid',
    'R5210': 'biogasoline',
    'R5220': 'biodiesel',
    'R5290': 'other_liquid_biofuels',
    'R5300': 'biogas',
    # Note: CF_R (renewable_fuels) excluded - only has third_countries data, no overall

    # Electricity and heat
    'E7000': 'electricity',
    'H8000': 'heat',

    # Note: Nuclear (N900H, S2000) excluded - limited relevance for import dependency analysis

    # Peat
    'P1100': 'peat',
    'P1200': 'peat_products',

    # Other
    'TOTAL': 'total'
}

# SIEC codes to explicitly exclude from output (no useful dependency data)
EXCLUDED_SIEC_CODES = {
    'SFF_OTH',   # other_solid_fossil_fuels - only has third_countries, no overall
    'CF_R',      # renewable_fuels - only has third_countries, no overall
    'S2000',     # nuclear_fuels - excluded per request
    'N900H',     # nuclear_heat - excluded per request
}

# Energy type codes to readable names
ENERGY_TYPE_NAMES = {
    'SFF': 'coal',
    'OIL': 'oil',
    'GAS': 'gas',
    'BIO': 'biofuels',
    'EH': 'electricity'
}

# Energy type units
ENERGY_TYPE_UNITS = {
    'SFF': 'THS_T',
    'OIL': 'THS_T',
    'GAS': 'TJ_GCV',
    'BIO': 'THS_T',
    'EH': 'GWH'
}


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


def print_phase_header(phase_num, title, total_phases=5):
    """Print a phase header with overall progress."""
    print()
    print('=' * 60)
    print(f'PHASE {phase_num}/{total_phases}: {title}')
    print('=' * 60)


# ============================================================================
# Phase 1: Load and Process Dependency Data
# ============================================================================

def load_dependency_data():
    """Load and process import dependency indicators."""
    print_phase_header(1, 'Loading dependency data')
    phase_start = time.time()

    print('  Loading CSV file...')
    df = pd.read_csv(DEPENDENCY_FILE)
    print(f'  Loaded {len(df):,} rows from dependency file')

    # Report indicators present
    print(f'  Indicators: {df["indicator"].unique().tolist()}')

    # Build dependency lookup: {geo: {year: {metrics}}}
    dependency_data = defaultdict(lambda: defaultdict(dict))

    # Process overall dependency (ID with partner=TOTAL)
    overall = df[(df['indicator'] == 'ID') & (df['partner'] == 'TOTAL')]
    total_overall = len(overall)
    print(f'  Processing overall dependency (ID): {total_overall:,} rows')

    start_time = time.time()
    for i, (_, row) in enumerate(overall.iterrows()):
        geo = row['geo']
        year = int(row['year'])
        siec = row['siec']
        value = row['value'] if pd.notna(row['value']) else None

        # Skip excluded SIEC codes
        if siec in EXCLUDED_SIEC_CODES:
            continue

        fuel_name = SIEC_TO_FUEL.get(siec, siec)

        if fuel_name == 'total' or siec == 'TOTAL':
            dependency_data[geo][year]['overall'] = value
        else:
            if 'by_fuel' not in dependency_data[geo][year]:
                dependency_data[geo][year]['by_fuel'] = {}
            if fuel_name not in dependency_data[geo][year]['by_fuel']:
                dependency_data[geo][year]['by_fuel'][fuel_name] = {}
            dependency_data[geo][year]['by_fuel'][fuel_name]['overall'] = value

        if (i + 1) % 5000 == 0 or i + 1 == total_overall:
            print_progress(i + 1, total_overall, start_time, 'Overall dep')
    print()  # New line after progress bar

    # Process third country dependency (ID3CF with partner=THRD)
    third_country = df[(df['indicator'] == 'ID3CF') & (df['partner'] == 'THRD')]
    total_third = len(third_country)
    print(f'  Processing third country dependency (ID3CF): {total_third:,} rows')

    start_time = time.time()
    for i, (_, row) in enumerate(third_country.iterrows()):
        geo = row['geo']
        year = int(row['year'])
        siec = row['siec']
        value = row['value'] if pd.notna(row['value']) else None

        # Skip excluded SIEC codes
        if siec in EXCLUDED_SIEC_CODES:
            continue

        fuel_name = SIEC_TO_FUEL.get(siec, siec)

        if fuel_name == 'total' or siec == 'TOTAL':
            dependency_data[geo][year]['third_countries'] = value
        else:
            if 'by_fuel' not in dependency_data[geo][year]:
                dependency_data[geo][year]['by_fuel'] = {}
            if fuel_name not in dependency_data[geo][year]['by_fuel']:
                dependency_data[geo][year]['by_fuel'][fuel_name] = {}
            dependency_data[geo][year]['by_fuel'][fuel_name]['third_countries'] = value

        if (i + 1) % 5000 == 0 or i + 1 == total_third:
            print_progress(i + 1, total_third, start_time, 'Third country')
    print()  # New line after progress bar

    # Note: IDOGAS and IDOOIL (gas/oil origins) are skipped as they have limited data coverage

    phase_elapsed = time.time() - phase_start
    print(f'  Processed {len(dependency_data)} countries in {format_time(phase_elapsed)}')
    return dict(dependency_data)


# ============================================================================
# Phase 2: Process Trade Data (Chunked)
# ============================================================================

def process_trade_data(chunk_size=1_000_000):
    """Process trade data in chunks to manage memory."""
    print_phase_header(2, 'Processing trade data (chunked)')
    phase_start = time.time()

    # Accumulators for aggregated data
    # {geo: {year: {energy_type: {partner: value}}}}
    imports_by_partner = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(float))))
    exports_by_partner = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(float))))

    # Totals by energy type
    imports_totals = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    exports_totals = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))

    chunk_num = 0
    total_rows = 0
    rows_processed_in_chunk = 0

    print(f'  Reading {TRADE_FILE.name} in chunks of {chunk_size:,} rows...')
    print(f'  Estimated total: ~{ESTIMATED_TRADE_ROWS:,} rows')
    print()

    for chunk in pd.read_csv(TRADE_FILE, chunksize=chunk_size):
        chunk_num += 1
        chunk_start = time.time()
        total_rows += len(chunk)

        # Filter out aggregates and invalid partners
        chunk = chunk[~chunk['geo'].isin(['EU27_2020', 'EA20'])]
        chunk = chunk[~chunk['partner'].isin(['TOTAL', 'THRD', 'NSP'])]
        chunk = chunk[chunk['value'].notna()]

        rows_processed_in_chunk = len(chunk)

        # Process imports
        imports_chunk = chunk[chunk['flow'] == 'IMPORT']
        for _, row in imports_chunk.iterrows():
            geo = row['geo']
            year = int(row['year'])
            energy_type = row['energy_type']
            partner = row['partner']
            value = float(row['value'])

            imports_by_partner[geo][year][energy_type][partner] += value
            imports_totals[geo][year][energy_type] += value

        # Process exports
        exports_chunk = chunk[chunk['flow'] == 'EXPORT']
        for _, row in exports_chunk.iterrows():
            geo = row['geo']
            year = int(row['year'])
            energy_type = row['energy_type']
            partner = row['partner']
            value = float(row['value'])

            exports_by_partner[geo][year][energy_type][partner] += value
            exports_totals[geo][year][energy_type] += value

        # Print progress with ETA
        print_progress(total_rows, ESTIMATED_TRADE_ROWS, phase_start, 'Trade data')

    print()  # New line after progress bar

    phase_elapsed = time.time() - phase_start
    print(f'  Finished processing {total_rows:,} rows in {chunk_num} chunks')
    print(f'  Phase completed in {format_time(phase_elapsed)}')

    return {
        'imports_by_partner': dict(imports_by_partner),
        'exports_by_partner': dict(exports_by_partner),
        'imports_totals': dict(imports_totals),
        'exports_totals': dict(exports_totals)
    }


def calculate_shares_and_rankings(trade_data):
    """Calculate partner shares and identify top partners."""
    print_phase_header(3, 'Calculating shares and rankings')
    phase_start = time.time()

    results = defaultdict(lambda: defaultdict(dict))

    # Count total geo-year combinations for progress
    total_combinations = sum(len(years) for years in trade_data['imports_by_partner'].values())
    processed = 0
    start_time = time.time()

    for geo, years_data in trade_data['imports_by_partner'].items():
        for year, energy_types in years_data.items():
            year_data = {'imports': {}, 'exports': {}}

            # Process imports
            total_by_type = {}
            all_partners = defaultdict(float)

            for energy_type, partners in energy_types.items():
                type_total = trade_data['imports_totals'].get(geo, {}).get(year, {}).get(energy_type, 0)
                total_by_type[energy_type] = {
                    'value': round(type_total, 2),
                    'unit': ENERGY_TYPE_UNITS.get(energy_type, 'UNKNOWN')
                }

                # Accumulate partner totals across energy types
                for partner, value in partners.items():
                    all_partners[partner] += value

            year_data['imports']['total_by_type'] = total_by_type

            # Calculate partner shares
            grand_total = sum(all_partners.values())
            if grand_total > 0:
                partner_shares = []

                for partner, value in all_partners.items():
                    share = (value / grand_total) * 100

                    partner_shares.append({
                        'geo': partner,
                        'name': COUNTRY_NAMES.get(partner, partner),
                        'share_pct': round(share, 2)
                    })

                # Sort by share and filter out zero shares
                partner_shares.sort(key=lambda x: x['share_pct'], reverse=True)
                year_data['imports']['partners'] = [p for p in partner_shares if p['share_pct'] > 0]

            # Process exports similarly
            if geo in trade_data['exports_by_partner'] and year in trade_data['exports_by_partner'][geo]:
                exp_energy_types = trade_data['exports_by_partner'][geo][year]

                total_by_type_exp = {}
                all_partners_exp = defaultdict(float)

                for energy_type, partners in exp_energy_types.items():
                    type_total = trade_data['exports_totals'].get(geo, {}).get(year, {}).get(energy_type, 0)
                    total_by_type_exp[energy_type] = {
                        'value': round(type_total, 2),
                        'unit': ENERGY_TYPE_UNITS.get(energy_type, 'UNKNOWN')
                    }

                    for partner, value in partners.items():
                        all_partners_exp[partner] += value

                year_data['exports']['total_by_type'] = total_by_type_exp

                grand_total_exp = sum(all_partners_exp.values())
                if grand_total_exp > 0:
                    partner_shares_exp = []

                    for partner, value in all_partners_exp.items():
                        share = (value / grand_total_exp) * 100

                        partner_shares_exp.append({
                            'geo': partner,
                            'name': COUNTRY_NAMES.get(partner, partner),
                            'share_pct': round(share, 2)
                        })

                    # Sort by share and filter out zero shares
                    partner_shares_exp.sort(key=lambda x: x['share_pct'], reverse=True)
                    year_data['exports']['partners'] = [p for p in partner_shares_exp if p['share_pct'] > 0]

            results[geo][year] = year_data

            processed += 1
            if processed % 100 == 0 or processed == total_combinations:
                print_progress(processed, total_combinations, start_time, 'Shares')

    print()  # New line after progress bar

    phase_elapsed = time.time() - phase_start
    print(f'  Calculated shares for {len(results)} countries in {format_time(phase_elapsed)}')
    return dict(results)


# ============================================================================
# Phase 4: Build JSON Structure
# ============================================================================

def build_json_output(dependency_data, trade_results):
    """Combine all data into final JSON structure."""
    print_phase_header(4, 'Building JSON output')
    phase_start = time.time()

    # Get all countries and years
    all_countries = set(dependency_data.keys()) | set(trade_results.keys())
    all_years = set()
    for geo_data in list(dependency_data.values()) + list(trade_results.values()):
        all_years.update(geo_data.keys())

    all_years = sorted([y for y in all_years if isinstance(y, int)])
    print(f'  Countries: {len(all_countries)}, Years: {all_years[0]}-{all_years[-1]}')

    # Build country data
    countries = {}
    sorted_countries = sorted(all_countries)
    total_countries = len(sorted_countries)
    start_time = time.time()

    for i, geo in enumerate(sorted_countries):
        # Skip aggregates
        if geo in ['EU27_2020', 'EA20']:
            continue

        country_entry = {
            'name': COUNTRY_NAMES.get(geo, geo),
            'years': {}
        }

        for year in all_years:
            year_entry = {}

            # Add dependency data
            if geo in dependency_data and year in dependency_data[geo]:
                dep_data = dependency_data[geo][year]
                year_entry['dependency'] = {
                    'overall': dep_data.get('overall'),
                    'third_countries': dep_data.get('third_countries'),
                }
                if 'by_fuel' in dep_data:
                    year_entry['dependency']['by_fuel'] = dep_data['by_fuel']

            # Add trade data
            if geo in trade_results and year in trade_results[geo]:
                trade = trade_results[geo][year]
                if trade.get('imports'):
                    year_entry['imports'] = trade['imports']
                if trade.get('exports'):
                    year_entry['exports'] = trade['exports']

            # Only add year if it has data
            if year_entry:
                country_entry['years'][str(year)] = year_entry

        # Only add country if it has data
        if country_entry['years']:
            countries[geo] = country_entry

        if (i + 1) % 10 == 0 or i + 1 == total_countries:
            print_progress(i + 1, total_countries, start_time, 'Building')

    print()  # New line after progress bar

    # Build final output
    output = {
        'metadata': {
            'generated': datetime.now().isoformat(),
            'sources': [
                'Eurostat energy trade (estat_nrg_ti_*, estat_nrg_te_*)',
                'Eurostat import dependency (estat_nrg_ind_id, estat_nrg_ind_id3cf)'
            ],
            'time_range': [all_years[0], all_years[-1]],
            'energy_types': list(ENERGY_TYPE_NAMES.keys()),
            'energy_type_names': ENERGY_TYPE_NAMES,
            'energy_type_units': ENERGY_TYPE_UNITS
        },
        'countries': countries,
        'country_lookup': {k: v for k, v in COUNTRY_NAMES.items() if k in all_countries}
    }

    phase_elapsed = time.time() - phase_start
    print(f'  Built output with {len(countries)} countries in {format_time(phase_elapsed)}')
    return output


# ============================================================================
# Phase 5: Verification
# ============================================================================

def verify_output(output):
    """Run verification checks on the output."""
    print_phase_header(5, 'Verification')

    issues = []

    # Check 1: Country count
    country_count = len(output['countries'])
    print(f'1. Country count: {country_count}')
    if country_count < 30:
        issues.append(f'Low country count: {country_count}')

    # Check 2: Year range
    time_range = output['metadata']['time_range']
    print(f'2. Year range: {time_range[0]}-{time_range[1]}')

    # Check 3: Sample countries have data
    sample_countries = ['DE', 'FR', 'PL', 'IT', 'ES']
    sample_years = [2000, 2015, 2023]

    print('3. Sample data spot-check:')
    for geo in sample_countries:
        if geo not in output['countries']:
            issues.append(f'Missing country: {geo}')
            continue

        country = output['countries'][geo]
        for year in sample_years:
            year_str = str(year)
            if year_str not in country['years']:
                print(f'   {geo}/{year}: NO DATA')
                continue

            year_data = country['years'][year_str]
            dep = year_data.get('dependency', {}).get('overall')
            third = year_data.get('dependency', {}).get('third_countries')
            top_partner = None
            if 'imports' in year_data and 'partners' in year_data['imports']:
                partners = year_data['imports']['partners']
                if partners:
                    top_partner = f"{partners[0]['name']} ({partners[0]['share_pct']}%)"

            print(f'   {geo}/{year}: dep={dep}%, third={third}%, top={top_partner}')

    # Check 4: Dependency values in valid range
    print('4. Dependency value range check:')
    dep_values = []
    for geo, country in output['countries'].items():
        for year, year_data in country['years'].items():
            if 'dependency' in year_data:
                overall = year_data['dependency'].get('overall')
                if overall is not None:
                    dep_values.append(overall)

    if dep_values:
        print(f'   Min: {min(dep_values):.1f}%, Max: {max(dep_values):.1f}%')
        print(f'   (Negative values indicate net exporters)')

    # Check 5: Partners list check
    print('5. Partners check (sample):')
    for geo in ['DE', 'FR']:
        if geo in output['countries']:
            for year in ['2020', '2023']:
                if year in output['countries'][geo]['years']:
                    year_data = output['countries'][geo]['years'][year]
                    if 'imports' in year_data and 'partners' in year_data['imports']:
                        partners = year_data['imports']['partners']
                        print(f'   {geo}/{year}: {len(partners)} partners, top 3 = {sum(p["share_pct"] for p in partners[:3]):.1f}%')

    if issues:
        print()
        print('ISSUES FOUND:')
        for issue in issues:
            print(f'  - {issue}')
    else:
        print()
        print('All verification checks passed!')

    return len(issues) == 0


# ============================================================================
# Main
# ============================================================================

def main():
    overall_start = time.time()

    print('=' * 60)
    print('Energy Imports/Exports JSON Dataset Generator')
    print('=' * 60)
    print()
    print(f'Started at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print()

    # Ensure output directory exists
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

    # Phase 1: Load dependency data
    dependency_data = load_dependency_data()

    # Phase 2: Process trade data
    trade_data = process_trade_data(chunk_size=500_000)

    # Phase 3: Calculate shares and rankings
    trade_results = calculate_shares_and_rankings(trade_data)

    # Phase 4: Build JSON output
    output = build_json_output(dependency_data, trade_results)

    # Phase 5: Verify
    verify_output(output)

    # Save output
    output_file = OUTPUT_PATH / 'energy_imports_exports_dependency.json'
    print()
    print('=' * 60)
    print('Saving output')
    print('=' * 60)

    print('  Writing JSON file...')
    save_start = time.time()
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    save_elapsed = time.time() - save_start

    file_size = output_file.stat().st_size / (1024 * 1024)
    print(f'  Saved to: {output_file}')
    print(f'  File size: {file_size:.2f} MB')
    print(f'  Write time: {format_time(save_elapsed)}')

    # Final summary
    overall_elapsed = time.time() - overall_start
    print()
    print('=' * 60)
    print('COMPLETE')
    print('=' * 60)
    print(f'  Total execution time: {format_time(overall_elapsed)}')
    print(f'  Finished at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print()


if __name__ == '__main__':
    main()
