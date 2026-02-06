"""
Augment existing energy imports/exports/dependency JSON with OWID production/consumption data.

Reads:
- prepared-sets/energy_imports_exports_dependency.json (existing 30MB dataset)
- raw-data/energy_consumption/owid-energy-data.xlsx (OWID energy dataset)
- country_code_mastersheet.json (ISO2 ↔ ISO3 mapping)

Outputs:
- prepared-sets/energy_mix.json (augmented dataset)
- Also copies to public/data/energy_mix.json
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
INPUT_JSON = BASE_DIR / 'prepared-sets' / 'energy_imports_exports_dependency.json'
OWID_FILE = BASE_DIR / 'raw-data' / 'energy_consumption' / 'owid-energy-data.xlsx'
MASTERSHEET = BASE_DIR / 'country_code_mastersheet.json'
OUTPUT_JSON = BASE_DIR / 'prepared-sets' / 'energy_mix.json'
PUBLIC_JSON = BASE_DIR.parent / 'public' / 'data' / 'energy_mix.json'

# OWID columns → internal energy type codes
OWID_PRODUCTION_COLS = {
    'coal_production': 'SFF',
    'oil_production': 'OIL',
    'gas_production': 'GAS',
    'electricity_generation': 'EH',
}

OWID_CONSUMPTION_COLS = {
    'coal_consumption': 'SFF',
    'oil_consumption': 'OIL',
    'gas_consumption': 'GAS',
    'biofuel_consumption': 'BIO',
    'electricity_demand': 'EH',
}


def main():
    overall_start = time.time()

    print('=' * 60)
    print('Augment Energy Dataset with OWID Production/Consumption')
    print('=' * 60)
    print()

    # ---- Step 1: Load existing JSON ----
    print('Step 1: Loading existing JSON dataset...')
    with open(INPUT_JSON, 'r', encoding='utf-8') as f:
        text = f.read()
    # Handle NaN values
    text = text.replace(': NaN', ': null')
    data = json.loads(text)
    n_countries = len(data['countries'])
    print(f'  Loaded {n_countries} countries')
    print()

    # ---- Step 2: Load country code mastersheet ----
    print('Step 2: Loading country code mastersheet...')
    with open(MASTERSHEET, 'r', encoding='utf-8') as f:
        mastersheet = json.load(f)
    owid_to_eurostat = mastersheet['owid_to_eurostat']
    eurostat_to_owid = mastersheet['eurostat_to_owid']
    print(f'  {len(owid_to_eurostat)} OWID→Eurostat mappings')
    print()

    # ---- Step 3: Load OWID data ----
    print('Step 3: Loading OWID energy dataset...')
    t0 = time.time()
    df = pd.read_excel(OWID_FILE)
    print(f'  Loaded {len(df):,} rows, {len(df.columns)} columns in {time.time()-t0:.1f}s')

    # Filter to countries in mastersheet
    df_filtered = df[df['iso_code'].isin(owid_to_eurostat.keys())].copy()
    df_filtered['geo'] = df_filtered['iso_code'].map(owid_to_eurostat)
    n_matched = df_filtered['geo'].nunique()
    print(f'  Matched {n_matched} countries from mastersheet')

    # Check for missing countries
    matched_geos = set(df_filtered['geo'].unique())
    all_eurostat_geos = set(owid_to_eurostat.values())
    missing = all_eurostat_geos - matched_geos
    if missing:
        print(f'  WARNING: {len(missing)} project countries not in OWID: {sorted(missing)}')
    print()

    # ---- Step 4: Build OWID lookup ----
    print('Step 4: Building production/consumption lookup...')
    t0 = time.time()

    all_owid_cols = list(OWID_PRODUCTION_COLS.keys()) + list(OWID_CONSUMPTION_COLS.keys())
    existing_cols = [c for c in all_owid_cols if c in df_filtered.columns]
    missing_cols = [c for c in all_owid_cols if c not in df_filtered.columns]
    if missing_cols:
        print(f'  WARNING: Missing OWID columns: {missing_cols}')

    # Build: {geo: {year_str: {production: {...}, consumption: {...}}}}
    owid_lookup = {}
    for _, row in df_filtered.iterrows():
        geo = row['geo']
        year_str = str(int(row['year']))

        if geo not in owid_lookup:
            owid_lookup[geo] = {}

        prod = {}
        cons = {}

        for owid_col, energy_type in OWID_PRODUCTION_COLS.items():
            if owid_col in df_filtered.columns:
                val = row[owid_col]
                if pd.notna(val):
                    prod[energy_type] = round(float(val), 3)

        for owid_col, energy_type in OWID_CONSUMPTION_COLS.items():
            if owid_col in df_filtered.columns:
                val = row[owid_col]
                if pd.notna(val):
                    cons[energy_type] = round(float(val), 3)

        entry = {}
        if prod:
            entry['production'] = prod
        if cons:
            entry['consumption'] = cons
        if entry:
            owid_lookup[geo][year_str] = entry

    print(f'  Built lookup for {len(owid_lookup)} countries in {time.time()-t0:.1f}s')

    # Stats
    total_year_entries = sum(len(years) for years in owid_lookup.values())
    print(f'  Total year entries: {total_year_entries:,}')
    print()

    # ---- Step 5: Merge into existing JSON ----
    print('Step 5: Merging OWID data into existing dataset...')
    merged_count = 0
    new_year_count = 0

    for geo, years_data in owid_lookup.items():
        if geo not in data['countries']:
            # Country exists in OWID but not in Eurostat dataset — skip
            continue

        country = data['countries'][geo]

        for year_str, owid_entry in years_data.items():
            if year_str in country['years']:
                # Merge into existing year
                if 'production' in owid_entry:
                    country['years'][year_str]['production'] = owid_entry['production']
                if 'consumption' in owid_entry:
                    country['years'][year_str]['consumption'] = owid_entry['consumption']
                merged_count += 1
            else:
                # Add new year entry with just OWID data
                country['years'][year_str] = owid_entry
                new_year_count += 1

    print(f'  Merged into {merged_count:,} existing year entries')
    print(f'  Added {new_year_count:,} new year entries (OWID-only)')
    print()

    # ---- Step 6: Update metadata ----
    print('Step 6: Updating metadata...')
    data['metadata']['generated'] = datetime.now().isoformat()
    data['metadata']['sources'] = [
        'Eurostat energy trade (estat_nrg_ti_*, estat_nrg_te_*)',
        'Eurostat import dependency (estat_nrg_ind_id, estat_nrg_ind_id3cf)',
        'Our World in Data - Energy Dataset (production, consumption)'
    ]
    data['metadata']['production_consumption_unit'] = 'TWh'
    data['metadata']['production_types'] = list(OWID_PRODUCTION_COLS.values())
    data['metadata']['consumption_types'] = list(OWID_CONSUMPTION_COLS.values())

    # Update time range
    all_years_set = set()
    for country in data['countries'].values():
        all_years_set.update(int(y) for y in country['years'].keys())
    if all_years_set:
        data['metadata']['time_range'] = [min(all_years_set), max(all_years_set)]
    print(f'  Time range: {data["metadata"]["time_range"]}')
    print()

    # ---- Step 7: Verification ----
    print('Step 7: Verification...')
    sample_countries = ['DE', 'FR', 'IT', 'PL', 'ES']
    sample_years = ['2000', '2015', '2023']

    for geo in sample_countries:
        if geo not in data['countries']:
            print(f'  {geo}: NOT IN DATASET')
            continue
        country = data['countries'][geo]
        for year in sample_years:
            if year not in country['years']:
                print(f'  {geo}/{year}: no data')
                continue
            yd = country['years'][year]
            prod = yd.get('production', {})
            cons = yd.get('consumption', {})
            dep = yd.get('dependency', {}).get('overall')
            print(f'  {geo}/{year}: dep={dep}%, prod={list(prod.keys())}, cons={list(cons.keys())}')

    print()

    # ---- Step 8: Save ----
    print('Step 8: Saving output...')
    t0 = time.time()

    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

    file_size = OUTPUT_JSON.stat().st_size / (1024 * 1024)
    print(f'  Saved to: {OUTPUT_JSON}')
    print(f'  File size: {file_size:.1f} MB')

    # Copy to public/data
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
