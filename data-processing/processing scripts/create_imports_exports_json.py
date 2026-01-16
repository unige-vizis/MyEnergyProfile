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
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# ============================================================================
# Configuration
# ============================================================================

BASE_PATH = Path(__file__).parent.parent / 'base-data' / '05_Energy-Imports-Exports'
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
    'SFF_OTH': 'other_solid_fossil_fuels',

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
    'CF_R': 'renewable_fuels',

    # Electricity and heat
    'E7000': 'electricity',
    'H8000': 'heat',

    # Nuclear
    'N900H': 'nuclear_heat',
    'S2000': 'nuclear_fuels',

    # Peat
    'P1100': 'peat',
    'P1200': 'peat_products',

    # Other
    'TOTAL': 'total'
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
# Phase 1: Load and Process Dependency Data
# ============================================================================

def load_dependency_data():
    """Load and process import dependency indicators."""
    print('=' * 60)
    print('PHASE 1: Loading dependency data')
    print('=' * 60)

    df = pd.read_csv(DEPENDENCY_FILE)
    print(f'Loaded {len(df):,} rows from dependency file')

    # Report indicators present
    print(f'Indicators: {df["indicator"].unique().tolist()}')

    # Build dependency lookup: {geo: {year: {metrics}}}
    dependency_data = defaultdict(lambda: defaultdict(dict))

    # Process overall dependency (ID with partner=TOTAL)
    overall = df[(df['indicator'] == 'ID') & (df['partner'] == 'TOTAL')]
    print(f'  Overall dependency (ID): {len(overall):,} rows')

    for _, row in overall.iterrows():
        geo = row['geo']
        year = int(row['year'])
        siec = row['siec']
        value = row['value'] if pd.notna(row['value']) else None

        fuel_name = SIEC_TO_FUEL.get(siec, siec)

        if fuel_name == 'total' or siec == 'TOTAL':
            dependency_data[geo][year]['overall'] = value
        else:
            if 'by_fuel' not in dependency_data[geo][year]:
                dependency_data[geo][year]['by_fuel'] = {}
            if fuel_name not in dependency_data[geo][year]['by_fuel']:
                dependency_data[geo][year]['by_fuel'][fuel_name] = {}
            dependency_data[geo][year]['by_fuel'][fuel_name]['overall'] = value

    # Process third country dependency (ID3CF with partner=THRD)
    third_country = df[(df['indicator'] == 'ID3CF') & (df['partner'] == 'THRD')]
    print(f'  Third country dependency (ID3CF): {len(third_country):,} rows')

    for _, row in third_country.iterrows():
        geo = row['geo']
        year = int(row['year'])
        siec = row['siec']
        value = row['value'] if pd.notna(row['value']) else None

        fuel_name = SIEC_TO_FUEL.get(siec, siec)

        if fuel_name == 'total' or siec == 'TOTAL':
            dependency_data[geo][year]['third_countries'] = value
        else:
            if 'by_fuel' not in dependency_data[geo][year]:
                dependency_data[geo][year]['by_fuel'] = {}
            if fuel_name not in dependency_data[geo][year]['by_fuel']:
                dependency_data[geo][year]['by_fuel'][fuel_name] = {}
            dependency_data[geo][year]['by_fuel'][fuel_name]['third_countries'] = value

    # Note: IDOGAS and IDOOIL (gas/oil origins) are skipped as they have limited data coverage

    print(f'Processed {len(dependency_data)} countries')
    return dict(dependency_data)


# ============================================================================
# Phase 2: Process Trade Data (Chunked)
# ============================================================================

def process_trade_data(chunk_size=1_000_000):
    """Process trade data in chunks to manage memory."""
    print()
    print('=' * 60)
    print('PHASE 2: Processing trade data (chunked)')
    print('=' * 60)

    # Accumulators for aggregated data
    # {geo: {year: {energy_type: {partner: value}}}}
    imports_by_partner = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(float))))
    exports_by_partner = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(float))))

    # Totals by energy type
    imports_totals = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    exports_totals = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))

    chunk_num = 0
    total_rows = 0

    for chunk in pd.read_csv(TRADE_FILE, chunksize=chunk_size):
        chunk_num += 1
        total_rows += len(chunk)

        # Filter out aggregates and invalid partners
        chunk = chunk[~chunk['geo'].isin(['EU27_2020', 'EA20'])]
        chunk = chunk[~chunk['partner'].isin(['TOTAL', 'THRD', 'NSP'])]
        chunk = chunk[chunk['value'].notna()]

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

        if chunk_num % 5 == 0:
            print(f'  Processed chunk {chunk_num}: {total_rows:,} rows so far')

    print(f'Finished processing {total_rows:,} rows in {chunk_num} chunks')

    return {
        'imports_by_partner': dict(imports_by_partner),
        'exports_by_partner': dict(exports_by_partner),
        'imports_totals': dict(imports_totals),
        'exports_totals': dict(exports_totals)
    }


def calculate_shares_and_rankings(trade_data):
    """Calculate partner shares and identify top partners."""
    print()
    print('=' * 60)
    print('PHASE 3: Calculating shares and rankings')
    print('=' * 60)

    results = defaultdict(lambda: defaultdict(dict))

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

    print(f'Calculated shares for {len(results)} countries')
    return dict(results)


# ============================================================================
# Phase 4: Build JSON Structure
# ============================================================================

def build_json_output(dependency_data, trade_results):
    """Combine all data into final JSON structure."""
    print()
    print('=' * 60)
    print('PHASE 4: Building JSON output')
    print('=' * 60)

    # Get all countries and years
    all_countries = set(dependency_data.keys()) | set(trade_results.keys())
    all_years = set()
    for geo_data in list(dependency_data.values()) + list(trade_results.values()):
        all_years.update(geo_data.keys())

    all_years = sorted([y for y in all_years if isinstance(y, int)])
    print(f'Countries: {len(all_countries)}, Years: {all_years[0]}-{all_years[-1]}')

    # Build country data
    countries = {}
    for geo in sorted(all_countries):
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

    print(f'Built output with {len(countries)} countries')
    return output


# ============================================================================
# Phase 5: Verification
# ============================================================================

def verify_output(output):
    """Run verification checks on the output."""
    print()
    print('=' * 60)
    print('PHASE 5: Verification')
    print('=' * 60)

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
    print('=' * 60)
    print('Energy Imports/Exports JSON Dataset Generator')
    print('=' * 60)
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

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    file_size = output_file.stat().st_size / (1024 * 1024)
    print(f'Saved to: {output_file}')
    print(f'File size: {file_size:.2f} MB')
    print()
    print('Done!')


if __name__ == '__main__':
    main()
