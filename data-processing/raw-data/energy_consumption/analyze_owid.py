#!/usr/bin/env python3
"""Analyze the OWID energy dataset for column structure, coverage, and overlap with EU project countries."""

import pandas as pd
import pycountry

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)
pd.set_option("display.max_rows", 200)

FILE = "/home/mattik01/Desktop/githubs/MyEnergyProfile/data-processing/raw-data/energy_consumption/owid-energy-data.xlsx"

print("Loading OWID energy dataset...")
df = pd.read_excel(FILE)
print(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns\n")

# 1. Column list
print("=" * 80)
print("1. ALL COLUMNS")
print("=" * 80)
for i, col in enumerate(df.columns, 1):
    print(f"  {i:>3}. {col}")
print(f"\nTotal columns: {len(df.columns)}\n")

# 2. Country coverage
print("=" * 80)
print("2. COUNTRY COVERAGE (unique country + iso_code pairs)")
print("=" * 80)
countries = df[["country", "iso_code"]].drop_duplicates().sort_values("country").reset_index(drop=True)
for _, row in countries.iterrows():
    print(f"  {str(row['iso_code']):>6}  {row['country']}")
print(f"\nTotal unique countries/entities: {len(countries)}")
print(f"  - With ISO code:    {countries['iso_code'].notna().sum()}")
print(f"  - Without ISO code: {countries['iso_code'].isna().sum()}\n")

# 3. Year range
print("=" * 80)
print("3. YEAR RANGE")
print("=" * 80)
print(f"  Min year: {df['year'].min()}")
print(f"  Max year: {df['year'].max()}")
print(f"  Unique years: {df['year'].nunique()}\n")

# 4. Production columns
print("=" * 80)
print("4. PRODUCTION COLUMNS (*_production)")
print("=" * 80)
prod_cols = [c for c in df.columns if "_production" in c.lower()]
if prod_cols:
    for col in sorted(prod_cols):
        non_null = df[col].notna().sum()
        print(f"  {col:<45} non-null: {non_null:>6} / {len(df)}  ({100*non_null/len(df):.1f}%)")
else:
    print("  (none found)")
print(f"\nTotal production columns: {len(prod_cols)}\n")

# 5. Consumption columns
print("=" * 80)
print("5. CONSUMPTION COLUMNS (*_consumption)")
print("=" * 80)
cons_cols = [c for c in df.columns if "_consumption" in c.lower()]
if cons_cols:
    for col in sorted(cons_cols):
        non_null = df[col].notna().sum()
        print(f"  {col:<45} non-null: {non_null:>6} / {len(df)}  ({100*non_null/len(df):.1f}%)")
else:
    print("  (none found)")
print(f"\nTotal consumption columns: {len(cons_cols)}\n")

# 6. Electricity columns
print("=" * 80)
print("6. ELECTRICITY COLUMNS (electricity_generation, electricity_demand, and related)")
print("=" * 80)
elec_cols = [c for c in df.columns if "electric" in c.lower()]
if elec_cols:
    for col in sorted(elec_cols):
        non_null = df[col].notna().sum()
        print(f"  {col:<45} non-null: {non_null:>6} / {len(df)}  ({100*non_null/len(df):.1f}%)")
else:
    print("  (none found)")
print()

# 7. EU country overlap
print("=" * 80)
print("7. EU / PROJECT COUNTRY OVERLAP")
print("=" * 80)

project_iso2 = [
    "AL", "AT", "BA", "BE", "BG", "CH", "CY", "CZ", "DE", "DK",
    "EE", "EL", "ES", "FI", "FR", "GE", "HR", "HU", "IE", "IS",
    "IT", "LI", "LT", "LU", "LV", "MD", "ME", "MK", "MT", "NL",
    "NO", "PL", "PT", "RO", "RS", "SE", "SI", "SK", "TR", "UA",
    "UK", "XK",
]

manual_map = {
    "XK": "OWID_KOS",
    "EL": "GRC",
    "UK": "GBR",
}

iso2_to_iso3 = {}
for code in project_iso2:
    if code in manual_map:
        iso2_to_iso3[code] = manual_map[code]
    else:
        try:
            c = pycountry.countries.get(alpha_2=code)
            if c:
                iso2_to_iso3[code] = c.alpha_3
            else:
                iso2_to_iso3[code] = f"??({code})"
        except Exception:
            iso2_to_iso3[code] = f"??({code})"

owid_iso3 = set(df["iso_code"].dropna().unique())

found = []
missing = []
for iso2 in sorted(project_iso2):
    iso3 = iso2_to_iso3[iso2]
    in_owid = iso3 in owid_iso3
    country_name = ""
    if in_owid:
        country_name = df.loc[df["iso_code"] == iso3, "country"].iloc[0]
        found.append((iso2, iso3, country_name))
    else:
        try:
            country_name = pycountry.countries.get(alpha_2=iso2).name
        except Exception:
            country_name = iso2
        missing.append((iso2, iso3, country_name))

print(f"\n  Project countries: {len(project_iso2)}")
print(f"  Found in OWID:    {len(found)}")
print(f"  Missing in OWID:  {len(missing)}")

print(f"\n  FOUND ({len(found)}):")
for iso2, iso3, name in found:
    print(f"    {iso2} -> {iso3:<12} {name}")

print(f"\n  MISSING ({len(missing)}):")
for iso2, iso3, name in missing:
    print(f"    {iso2} -> {iso3:<12} {name}")

# For XK / Kosovo, also search by country name
if any(iso2 == "XK" for iso2, _, _ in missing):
    kosovo_rows = df[df["country"].str.contains("Kosovo", case=False, na=False)]
    if not kosovo_rows.empty:
        k_iso = kosovo_rows["iso_code"].iloc[0]
        print(f"\n  NOTE: Kosovo found by name search! OWID uses iso_code='{k_iso}' and country='{kosovo_rows['country'].iloc[0]}'")
print()

# 8. Sample data for Germany (DEU)
print("=" * 80)
print("8. SAMPLE DATA FOR GERMANY (DEU) - years 2000, 2010, 2020, 2023")
print("=" * 80)
deu = df[df["iso_code"] == "DEU"]
target_years = [2000, 2010, 2020, 2023]
deu_sample = deu[deu["year"].isin(target_years)]

relevant_cols = ["year"] + sorted(prod_cols) + sorted(cons_cols)
relevant_cols = [c for c in relevant_cols if c in deu_sample.columns]

if not deu_sample.empty:
    print(f"\n  Available years for DEU in dataset (last 10): {sorted(deu['year'].unique().tolist())[-10:]}")
    print(f"  Rows matching target years: {len(deu_sample)}\n")
    for _, row in deu_sample.iterrows():
        print(f"  --- Year {int(row['year'])} ---")
        for col in relevant_cols:
            if col == "year":
                continue
            val = row[col]
            status = "NULL" if pd.isna(val) else f"{val}"
            print(f"    {col:<45} {status}")
        print()
else:
    print("  No data found for DEU in target years.")
    print(f"  Available years: {sorted(deu['year'].unique().tolist())[:20]}...")
print()

# 9. Check for biofuel_production
print("=" * 80)
print("9. CHECK: biofuel_production")
print("=" * 80)
if "biofuel_production" in df.columns:
    non_null = df["biofuel_production"].notna().sum()
    print(f"  EXISTS - non-null: {non_null} / {len(df)}  ({100*non_null/len(df):.1f}%)")
else:
    biofuel_cols = [c for c in df.columns if "biofuel" in c.lower()]
    print(f"  NOT FOUND as exact column name.")
    if biofuel_cols:
        print(f"  Related biofuel columns: {biofuel_cols}")
    else:
        print(f"  No biofuel-related columns found at all.")
print()

# 10. Check nuclear/hydro/solar/wind consumption
print("=" * 80)
print("10. CHECK: nuclear_consumption, hydro_consumption, solar_consumption, wind_consumption")
print("=" * 80)
check_cols = ["nuclear_consumption", "hydro_consumption", "solar_consumption", "wind_consumption"]
for col in check_cols:
    if col in df.columns:
        non_null = df[col].notna().sum()
        print(f"  {col:<35} EXISTS    - non-null: {non_null:>6} / {len(df)}  ({100*non_null/len(df):.1f}%)")
    else:
        prefix = col.split("_")[0]
        similar = [c for c in df.columns if prefix in c.lower()]
        print(f"  {col:<35} NOT FOUND")
        if similar:
            print(f"    Related '{prefix}' columns: {similar}")
print()

print("=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
