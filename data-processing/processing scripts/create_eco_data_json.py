"""
Create eco_data.json with per-capita emissions and carbon intensity data.

Reads:
- raw-data/energy_consumption/owid-energy-data.xlsx (carbon_intensity_elec + population)
- raw-data/end_uses_efficiency/*_carbon_indicators.csv (tCO2/capita by sector)
- raw-data/end_uses_efficiency/*_emissions.csv (total kt CO2 by sector)
- country_code_mastersheet.json (ISO mapping)

Outputs:
- prepared-sets/eco_data.json
- Also copies to public/data/eco_data.json
"""

import pandas as pd
import numpy as np
import json
import time
import shutil
from pathlib import Path
from datetime import datetime

# ============================================================================
# Configuration
# ============================================================================

BASE_DIR = Path(__file__).parent.parent
OWID_FILE = BASE_DIR / 'raw-data' / 'energy_consumption' / 'owid-energy-data.xlsx'
MASTERSHEET = BASE_DIR / 'country_code_mastersheet.json'
OUTPUT_JSON = BASE_DIR / 'prepared-sets' / 'eco_data.json'
PUBLIC_JSON = BASE_DIR.parent / 'public' / 'data' / 'eco_data.json'

IEA_DIR = BASE_DIR / 'raw-data' / 'end_uses_efficiency'

# IEA CSVs use country names; map them to project ISO2 codes
# (inverted from create_consumptions_by_sector_json.py COUNTRY_NAMES)
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

# Build reverse: country name -> ISO2 code
NAME_TO_CODE = {name: code for code, name in COUNTRY_NAMES.items()}

# Year columns in IEA CSVs
YEAR_COLS = ['2000.0', '2005.0', '2010.0', '2015.0', '2016.0', '2017.0',
             '2018.0', '2019.0', '2020.0', '2021.0', '2022.0', '2023.0']


def read_iea_csv(filepath):
    """Read an IEA CSV, skipping the 'Source:' header line."""
    return pd.read_csv(filepath, skiprows=1)


def get_last_available(row, year_cols=YEAR_COLS):
    """Scan year columns from right to left, return (year, value) for last non-null, non-'..' value."""
    for col in reversed(year_cols):
        val = row.get(col)
        if val is not None and val != '..' and pd.notna(val):
            try:
                return int(float(col)), round(float(val), 4)
            except (ValueError, TypeError):
                continue
    return None, None


def main():
    overall_start = time.time()

    print('=' * 60)
    print('Create Eco Data JSON')
    print('=' * 60)
    print()

    # ---- Step 1: Load country code mastersheet ----
    print('Step 1: Loading country code mastersheet...')
    with open(MASTERSHEET, 'r', encoding='utf-8') as f:
        mastersheet = json.load(f)
    owid_to_eurostat = mastersheet['owid_to_eurostat']
    project_countries = {c['eurostat']: c['name'] for c in mastersheet['countries']}
    print(f'  {len(project_countries)} project countries')
    print()

    # ---- Step 2: Load OWID data (carbon_intensity_elec + population) ----
    print('Step 2: Loading OWID energy dataset...')
    t0 = time.time()
    df_owid = pd.read_excel(OWID_FILE)
    print(f'  Loaded {len(df_owid):,} rows in {time.time()-t0:.1f}s')

    # Filter to project countries
    df_owid = df_owid[df_owid['iso_code'].isin(owid_to_eurostat.keys())].copy()
    df_owid['geo'] = df_owid['iso_code'].map(owid_to_eurostat)

    # Build OWID lookup: {geo: {year: {carbon_intensity_elec, population}}}
    owid_lookup = {}
    for _, row in df_owid.iterrows():
        geo = row['geo']
        year = int(row['year'])
        ci = row.get('carbon_intensity_elec')
        pop = row.get('population')

        if geo not in owid_lookup:
            owid_lookup[geo] = {}

        entry = {}
        if pd.notna(ci):
            entry['carbon_intensity_elec'] = round(float(ci), 2)
        if pd.notna(pop):
            entry['population'] = float(pop)
        if entry:
            owid_lookup[geo][year] = entry

    print(f'  Built OWID lookup for {len(owid_lookup)} countries')
    print()

    # ---- Step 3: Load IEA per-capita carbon indicators ----
    print('Step 3: Loading IEA carbon indicators...')

    # Residential per-capita
    df_res_ci = read_iea_csv(IEA_DIR / 'residential_carbon_indicators.csv')
    df_res_ci = df_res_ci[
        (df_res_ci['End use'] == 'Total residential') &
        (df_res_ci['Indicator'] == 'Carbon intensity per capita (t CO2/capita)')
    ]

    # Services per-capita
    df_svc_ci = read_iea_csv(IEA_DIR / 'services_carbon_indicators.csv')
    df_svc_ci = df_svc_ci[
        (df_svc_ci['End use'] == 'Total services') &
        (df_svc_ci['Indicator'] == 'Carbon intensity per capita (t CO2/capita)')
    ]

    # Transport per-capita: Cars/light trucks + Freight trucks
    df_trn_ci = read_iea_csv(IEA_DIR / 'transport_carbon_indicators.csv')
    df_trn_cars = df_trn_ci[
        (df_trn_ci['End use'] == 'Cars/light trucks') &
        (df_trn_ci['Indicator'] == 'Carbon intensity per capita (t CO2/capita)')
    ]
    df_trn_freight = df_trn_ci[
        (df_trn_ci['End use'] == 'Freight trucks') &
        (df_trn_ci['Indicator'] == 'Carbon intensity per capita (t CO2/capita)')
    ]

    print(f'  Residential: {len(df_res_ci)} country rows')
    print(f'  Services: {len(df_svc_ci)} country rows')
    print(f'  Transport cars: {len(df_trn_cars)} rows, freight: {len(df_trn_freight)} rows')
    print()

    # ---- Step 4: Load IEA emissions totals ----
    print('Step 4: Loading IEA emissions totals...')

    # Industry: Manufacturing total
    df_ind_em = read_iea_csv(IEA_DIR / 'industry_emissions.csv')
    df_ind_em = df_ind_em[
        df_ind_em['End use'].str.contains('Manufacturing', na=False)
    ]

    # Residential total
    df_res_em = read_iea_csv(IEA_DIR / 'residential_emissions.csv')
    df_res_em = df_res_em[
        (df_res_em['End use'] == 'Total residential') &
        (df_res_em['Product'] == 'Total final use (kt CO2)')
    ]

    # Services total
    df_svc_em = read_iea_csv(IEA_DIR / 'services_emissions.csv')
    df_svc_em = df_svc_em[
        (df_svc_em['End use'] == 'Total services') &
        (df_svc_em['Product'] == 'Total final use (kt CO2)')
    ]

    # Transport: total passenger and freight
    df_trn_em = read_iea_csv(IEA_DIR / 'transport_emissions.csv')
    df_trn_total = df_trn_em[
        (df_trn_em['End use'] == 'Total passenger and freight transport') &
        (df_trn_em['Product'] == 'Total final use (kt CO2)')
    ]

    print(f'  Industry emissions: {len(df_ind_em)} rows')
    print(f'  Residential emissions: {len(df_res_em)} rows')
    print(f'  Services emissions: {len(df_svc_em)} rows')
    print(f'  Transport emissions: {len(df_trn_total)} rows')
    print()

    # ---- Step 5: Build per-country eco data ----
    print('Step 5: Building per-country eco data...')

    def get_iea_value(df, country_name):
        """Get last available value for a country from an IEA dataframe."""
        rows = df[df['Country'] == country_name]
        if rows.empty:
            return None, None
        row = rows.iloc[0]
        return get_last_available(row)

    def get_iea_transport_percapita(country_name):
        """Sum Cars/light trucks + Freight trucks per-capita for the latest common year."""
        cars_rows = df_trn_cars[df_trn_cars['Country'] == country_name]
        freight_rows = df_trn_freight[df_trn_freight['Country'] == country_name]
        if cars_rows.empty and freight_rows.empty:
            return None, None

        # Find last year where at least one has data
        best_year = None
        best_sum = 0
        for col in reversed(YEAR_COLS):
            cars_val = None
            freight_val = None
            if not cars_rows.empty:
                v = cars_rows.iloc[0].get(col)
                if v is not None and v != '..' and pd.notna(v):
                    try:
                        cars_val = float(v)
                    except (ValueError, TypeError):
                        pass
            if not freight_rows.empty:
                v = freight_rows.iloc[0].get(col)
                if v is not None and v != '..' and pd.notna(v):
                    try:
                        freight_val = float(v)
                    except (ValueError, TypeError):
                        pass
            if cars_val is not None or freight_val is not None:
                best_year = int(float(col))
                best_sum = (cars_val or 0) + (freight_val or 0)
                break

        if best_year is None:
            return None, None
        return best_year, round(best_sum, 4)

    countries_data = {}
    carbon_intensity_ranking = []

    for geo, country_name in project_countries.items():
        # Map project country name to IEA country name
        iea_name = COUNTRY_NAMES.get(geo)

        entry = {'name': country_name}

        # Carbon intensity from OWID
        owid_years = owid_lookup.get(geo, {})
        ci_year = None
        ci_value = None
        population = None

        # Find latest year with carbon_intensity_elec
        for y in sorted(owid_years.keys(), reverse=True):
            yd = owid_years[y]
            if 'carbon_intensity_elec' in yd:
                ci_year = y
                ci_value = yd['carbon_intensity_elec']
                break

        # Find latest year with population
        for y in sorted(owid_years.keys(), reverse=True):
            yd = owid_years[y]
            if 'population' in yd:
                population = yd['population']
                break

        if ci_value is not None:
            entry['carbon_intensity'] = {
                'latest_year': ci_year,
                'latest_value': ci_value
            }
            carbon_intensity_ranking.append({
                'code': geo,
                'name': country_name,
                'value': ci_value,
                'year': ci_year
            })

        # Per-capita emissions from IEA
        if iea_name:
            res_year, res_val = get_iea_value(df_res_ci, iea_name)
            svc_year, svc_val = get_iea_value(df_svc_ci, iea_name)
            trn_year, trn_val = get_iea_transport_percapita(iea_name)

            # Industry: compute from total emissions / population
            ind_em_year, ind_em_val = get_iea_value(df_ind_em, iea_name)
            ind_percapita = None
            ind_year = None
            if ind_em_val is not None and population is not None and population > 0:
                # ind_em_val is in kt CO2, population is persons
                # tCO2/capita = (kt CO2 * 1000) / population
                ind_percapita = round((ind_em_val * 1000) / population, 4)
                ind_year = ind_em_year

            # Find the most common year among available sectors
            years_available = [y for y in [res_year, svc_year, trn_year, ind_year] if y is not None]
            if years_available:
                emissions_year = max(years_available)  # Use latest available
                epc = {'year': emissions_year}
                if res_val is not None:
                    epc['residential'] = res_val
                if svc_val is not None:
                    epc['services'] = svc_val
                if trn_val is not None:
                    epc['transport'] = trn_val
                if ind_percapita is not None:
                    epc['industry'] = ind_percapita
                if len(epc) > 1:  # More than just 'year'
                    entry['emissions_per_capita'] = epc

            # Total emissions (kt CO2) from IEA
            res_em_year, res_em_val = get_iea_value(df_res_em, iea_name)
            svc_em_year, svc_em_val = get_iea_value(df_svc_em, iea_name)
            trn_em_year, trn_em_val = get_iea_value(df_trn_total, iea_name)
            ind_em_year2, ind_em_val2 = get_iea_value(df_ind_em, iea_name)

            em_years = [y for y in [res_em_year, svc_em_year, trn_em_year, ind_em_year2] if y is not None]
            if em_years:
                em_year = max(em_years)
                etk = {'year': em_year}
                if res_em_val is not None:
                    etk['residential'] = round(res_em_val, 1)
                if svc_em_val is not None:
                    etk['services'] = round(svc_em_val, 1)
                if trn_em_val is not None:
                    etk['transport'] = round(trn_em_val, 1)
                if ind_em_val2 is not None:
                    etk['industry'] = round(ind_em_val2, 1)
                if len(etk) > 1:
                    entry['emissions_total_kt'] = etk

        # Only include countries with at least some data
        if len(entry) > 1:
            countries_data[geo] = entry

    # Sort ranking by value ascending (cleanest first)
    carbon_intensity_ranking.sort(key=lambda x: x['value'])

    print(f'  Countries with eco data: {len(countries_data)}')
    print(f'  Countries in carbon intensity ranking: {len(carbon_intensity_ranking)}')
    print()

    # ---- Step 6: Build output ----
    print('Step 6: Building output...')

    output = {
        'metadata': {
            'generated': datetime.now().isoformat(),
            'sources': ['OWID Energy Data', 'IEA End-Uses & Efficiency Indicators']
        },
        'countries': countries_data,
        'carbon_intensity_ranking': carbon_intensity_ranking
    }

    # ---- Step 7: Verification ----
    print('Step 7: Verification...')
    sample_countries = ['DE', 'FR', 'IT', 'PL', 'SE']
    for geo in sample_countries:
        if geo not in countries_data:
            print(f'  {geo}: NO DATA')
            continue
        c = countries_data[geo]
        ci = c.get('carbon_intensity', {})
        epc = c.get('emissions_per_capita', {})
        print(f'  {geo} ({c["name"]}):')
        print(f'    Carbon intensity: {ci.get("latest_value")} gCO2/kWh ({ci.get("latest_year")})')
        print(f'    Per-capita: res={epc.get("residential")}, svc={epc.get("services")}, '
              f'trn={epc.get("transport")}, ind={epc.get("industry")} ({epc.get("year")})')
    print()

    # ---- Step 8: Save ----
    print('Step 8: Saving output...')
    t0 = time.time()

    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    file_size = OUTPUT_JSON.stat().st_size / 1024
    print(f'  Saved to: {OUTPUT_JSON}')
    print(f'  File size: {file_size:.1f} KB')

    # Copy to public/data
    PUBLIC_JSON.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUTPUT_JSON, PUBLIC_JSON)
    print(f'  Copied to: {PUBLIC_JSON}')
    print(f'  Write time: {time.time()-t0:.1f}s')
    print()

    # ---- Done ----
    total_time = time.time() - overall_start
    print('=' * 60)
    print(f'COMPLETE in {total_time:.1f}s')
    print('=' * 60)


if __name__ == '__main__':
    main()
