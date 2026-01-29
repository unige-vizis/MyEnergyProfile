# JSON Schema Documentation

## Required Header Format

All JSON files in `prepared-sets/` must include a `metadata` object with a `sources` array that references:
1. Our combined/intermediate datasets
2. The original Eurostat dataset codes

**Example metadata:**
```json
{
  "metadata": {
    "generated": "2026-01-16T18:22:25.838001",
    "sources": [
      "Eurostat energy trade (estat_nrg_ti_*, estat_nrg_te_*)",
      "Eurostat import dependency (estat_nrg_ind_id, estat_nrg_ind_id3cf)"
    ],
    "time_range": [1990, 2024],
    "energy_types": ["SFF", "OIL", "GAS", "BIO", "EH"],
    "energy_type_names": { ... },
    "energy_type_units": { ... }
  },
  "countries": { ... },
  "country_lookup": { ... }
}
```

This ensures traceability back to original data sources for transparency and reproducibility.

---

## Example: Germany (DE) - 2023

This document explains every field in the JSON output using Germany 2023 as an example.
Each field includes an annotation describing its meaning and data source.

---

## Full JSON Structure (Annotated)

### Root Structure

```jsonc
{
  "metadata": {
    "generated": "2026-01-16T18:22:25.838001",
    // ISO timestamp when this file was generated

    "sources": [
      "Eurostat energy trade (estat_nrg_ti_*, estat_nrg_te_*)",
      "Eurostat import dependency (estat_nrg_ind_id, estat_nrg_ind_id3cf)"
    ],
    // Original Eurostat dataset codes used

    "time_range": [1990, 2024],
    // [start_year, end_year] - full range of available data

    "energy_types": ["SFF", "OIL", "GAS", "BIO", "EH"],
    // Energy type codes used in the data

    "energy_type_names": {
      "SFF": "coal",
      "OIL": "oil",
      "GAS": "gas",
      "BIO": "biofuels",
      "EH": "electricity"
    },
    // Human-readable names for energy type codes

    "energy_type_units": {
      "SFF": "THS_T",
      "OIL": "THS_T",
      "GAS": "TJ_GCV",
      "BIO": "THS_T",
      "EH": "GWH"
    }
    // Units for each energy type
  },

  "countries": {
    "DE": { ... },  // See country structure below
    "FR": { ... },
    // ... all countries
  },

  "country_lookup": {
    "DE": "Germany",
    "FR": "France",
    // ISO code to full name mapping
  }
}
```

### Country Structure

```jsonc
{
  "DE": {
    "name": "Germany",
    // Full country name

    "years": {
      "2023": {
        // See year structure below
      },
      "2022": { ... },
      // ... all years with data
    }
  }
}
```

### Year Structure (Germany 2023 Example)

```jsonc
{
  "dependency": {
    // ═══════════════════════════════════════════════════════════════════════
    // DEPENDENCY METRICS
    // Source: combined_import_dependency.csv
    // Original Eurostat datasets: estat_nrg_ind_id, estat_nrg_ind_id3cf
    // ═══════════════════════════════════════════════════════════════════════

    "overall": 66.831,
    // ┌─────────────────────────────────────────────────────────────────────┐
    // │ OVERALL IMPORT DEPENDENCY (%)                                       │
    // │ Source: indicator='ID', partner='TOTAL', siec='TOTAL'              │
    // │ Formula: (Imports - Exports) / (Gross Inland Consumption + Bunkers)│
    // │ Meaning: 66.8% of Germany's energy needs are met by imports        │
    // │ Range: Can be negative (net exporter) or >100% (stock changes)     │
    // └─────────────────────────────────────────────────────────────────────┘

    "third_countries": 48.22,
    // ┌─────────────────────────────────────────────────────────────────────┐
    // │ THIRD COUNTRY DEPENDENCY (%)                                        │
    // │ Source: indicator='ID3CF', partner='THRD', siec='TOTAL'            │
    // │ Meaning: 48.2% of energy imports come from non-EU countries        │
    // │ "Third countries" = countries outside the EU                        │
    // └─────────────────────────────────────────────────────────────────────┘

    "by_fuel": {
      // ═════════════════════════════════════════════════════════════════════
      // DEPENDENCY BREAKDOWN BY FUEL TYPE
      // Source: Same indicators, filtered by siec (fuel) codes
      // ═════════════════════════════════════════════════════════════════════

      "coal": {
        "overall": 48.747,
        // Source: indicator='ID', siec='C0000X0350-0370' (hard coal aggregate)
        // Meaning: 48.7% of coal consumption depends on imports

        "third_countries": 44.85
        // Source: indicator='ID3CF', siec='C0000X0350-0370'
        // Meaning: 44.9% of coal imports come from non-EU
      },

      "natural_gas": {
        "overall": 93.66,
        // Source: indicator='ID', siec='G3000' (natural gas)
        // Meaning: Germany imports 93.7% of its natural gas

        "third_countries": 49.94
        // Source: indicator='ID3CF', siec='G3000'
      },

      "oil": {
        "overall": 95.396,
        // Source: indicator='ID', siec='O4000XBIO' (oil excl. biofuels)

        "third_countries": 70.47
        // Source: indicator='ID3CF', siec='O4000XBIO'
      },

      "lignite": {
        "overall": 0.0
        // Source: indicator='ID', siec='C0210'
        // Meaning: Germany produces all its lignite domestically
      },

      "electricity": {
        "overall": null,
        // ┌─────────────────────────────────────────────────────────────────────┐
        // │ ALWAYS NULL - Eurostat does not publish overall import dependency  │
        // │ for electricity (E7000). See "Why No Electricity Dependency" below.│
        // └─────────────────────────────────────────────────────────────────────┘

        "third_countries": 8.14
        // Source: indicator='ID3CF', siec='E7000' (from Eurostat directly)
        // This IS available - shows % of electricity imports from non-EU countries
      }

      // Additional fuel types may include:
      // anthracite, coking_coal, other_bituminous_coal, sub_bituminous_coal,
      // crude_oil, ngl, peat, nuclear_fuels, etc.
      //
      // Note: renewable_fuels (CF_R) and other_solid_fossil_fuels (SFF_OTH) are
      // excluded as they only have third_countries data with no overall dependency.
    }
  },

  "imports": {
    // ═══════════════════════════════════════════════════════════════════════
    // IMPORT DATA
    // Source: combined_energy_trade.csv (flow='IMPORT')
    // Original Eurostat datasets: estat_nrg_ti_sff, estat_nrg_ti_oil,
    //                             estat_nrg_ti_gas, estat_nrg_ti_bio, estat_nrg_ti_eh
    // ═══════════════════════════════════════════════════════════════════════

    "total_by_type": {
      // ═════════════════════════════════════════════════════════════════════
      // IMPORT VOLUMES BY ENERGY TYPE
      // Calculated: Sum of all partner imports per energy type
      // ═════════════════════════════════════════════════════════════════════

      "SFF": {
        "value": 96128.47,
        "unit": "THS_T"
        // SOLID FOSSIL FUELS (Coal)
        // Unit: Thousand tonnes
      },

      "OIL": {
        "value": 609290.0,
        "unit": "THS_T"
        // OIL & PETROLEUM PRODUCTS
        // Unit: Thousand tonnes
      },

      "GAS": {
        "value": 2960810.36,
        "unit": "TJ_GCV"
        // NATURAL GAS
        // Unit: Terajoules (Gross Calorific Value)
        // Note: 1 TJ ≈ 27,778 cubic meters of natural gas
      },

      "BIO": {
        "value": 482.0,
        "unit": "THS_T"
        // BIOFUELS
        // Unit: Thousand tonnes
      },

      "EH": {
        "value": 40624.0,
        "unit": "GWH"
        // ELECTRICITY & HEAT
        // Unit: Gigawatt-hours
      }
    },

    "partners": [
      // ═════════════════════════════════════════════════════════════════════
      // ALL IMPORT PARTNERS
      // Sorted by share percentage (descending)
      // Calculated: Aggregated across all energy types
      // Note: Shares are calculated from value sums, so gas (TJ) may dominate
      //       due to larger numeric values compared to coal (THS_T)
      // ═════════════════════════════════════════════════════════════════════

      {
        "geo": "NO",
        // ISO 3166-1 alpha-2 country code (or regional aggregate code)
        // Source: 'partner' column in combined_energy_trade.csv

        "name": "Norway",
        // Full country/region name from COUNTRY_NAMES lookup

        "share_pct": 33.94
        // Percentage share of total imports
        // Calculated: (partner_value / grand_total) * 100
      },
      {
        "geo": "NL",
        "name": "Netherlands",
        "share_pct": 22.61
      },
      {
        "geo": "BE",
        "name": "Belgium",
        "share_pct": 17.2
      },
      {
        "geo": "US",
        "name": "United States",
        "share_pct": 14.77
      }
      // ... all partners with non-zero shares
    ]
  },

  "exports": {
    // ═══════════════════════════════════════════════════════════════════════
    // EXPORT DATA
    // Source: combined_energy_trade.csv (flow='EXPORT')
    // Original Eurostat datasets: estat_nrg_te_sff, estat_nrg_te_oil,
    //                             estat_nrg_te_gas, estat_nrg_te_bio, estat_nrg_te_eh
    // Structure: Identical to imports section
    // ═══════════════════════════════════════════════════════════════════════

    "total_by_type": {
      "SFF": {
        "value": 5452.48,
        "unit": "THS_T"
      },
      "OIL": {
        "value": 148945.0,
        "unit": "THS_T"
      },
      "GAS": {
        "value": 115642.0,
        "unit": "TJ_GCV"
      },
      "BIO": {
        "value": 771.0,
        "unit": "THS_T"
      },
      "EH": {
        "value": 37309.0,
        "unit": "GWH"
      }
    },

    "partners": [
      {
        "geo": "CH",
        "name": "Switzerland",
        "share_pct": 44.13
      },
      {
        "geo": "BE",
        "name": "Belgium",
        "share_pct": 11.78
      }
      // ... all export partners
    ]
  }
}
```

---

## Data Flow Summary

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           SOURCE DATASETS                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  EUROSTAT IMPORT DEPENDENCY           EUROSTAT ENERGY TRADE                 │
│  ─────────────────────────            ─────────────────────                 │
│  estat_nrg_ind_id      → ID           estat_nrg_ti_sff → IMPORT SFF         │
│  estat_nrg_ind_id3cf   → ID3CF        estat_nrg_ti_oil → IMPORT OIL         │
│                                        estat_nrg_ti_gas → IMPORT GAS         │
│                                        estat_nrg_ti_bio → IMPORT BIO         │
│                                        estat_nrg_ti_eh  → IMPORT EH          │
│                                        estat_nrg_te_*   → EXPORT *           │
│                                                                              │
└───────────────────────────────┬─────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    INTERMEDIATE CSV FILES                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  combined_import_dependency.csv        combined_energy_trade.csv             │
│  ───────────────────────────────       ─────────────────────────             │
│  Columns:                              Columns:                              │
│  - indicator (ID, ID3CF)               - flow (IMPORT, EXPORT)              │
│  - siec (fuel type code)               - energy_type (SFF, OIL, GAS...)     │
│  - partner (TOTAL, THRD, country)      - partner (country code)             │
│  - geo (reporting country)             - geo (reporting country)            │
│  - year                                - year                                │
│  - value (%)                           - value (quantity)                   │
│                                                                              │
└───────────────────────────────┬─────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PROCESSING SCRIPT                                         │
│         create_imports_exports_json.py                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Phase 1: load_dependency_data()                                            │
│           → Parses dependency CSV, extracts ID/ID3CF indicators             │
│           → Maps SIEC codes to fuel names using SIEC_TO_FUEL dict           │
│                                                                              │
│  Phase 2: process_trade_data()                                              │
│           → Reads trade CSV in 500K chunks (31.8M rows total)               │
│           → Accumulates imports_by_partner and exports_by_partner           │
│           → Filters out TOTAL, THRD, NSP pseudo-partners                    │
│                                                                              │
│  Phase 3: calculate_shares_and_rankings()                                   │
│           → Calculates partner shares as % of total                         │
│           → Sorts partners by share descending                              │
│                                                                              │
│  Phase 4: build_json_output()                                               │
│           → Combines dependency + trade data                                │
│           → Structures by country → year → metrics                          │
│           → Adds metadata and lookups                                       │
│                                                                              │
│  Phase 5: verify_output()                                                   │
│           → Validates country count, year range                             │
│           → Spot-checks sample values                                       │
│                                                                              │
└───────────────────────────────┬─────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    OUTPUT JSON                                               │
│         energy_imports_exports_dependency.json                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  {                                                                           │
│    "metadata": { generated, sources, time_range, energy_types, ... },       │
│    "countries": {                                                            │
│      "DE": {                                                                 │
│        "name": "Germany",                                                    │
│        "years": {                                                            │
│          "2023": { dependency, imports, exports }                           │
│        }                                                                     │
│      }                                                                       │
│    },                                                                        │
│    "country_lookup": { "DE": "Germany", ... }                               │
│  }                                                                           │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## SIEC Code Reference

| Code | Mapped Name | Description |
|------|-------------|-------------|
| `C0000X0350-0370` | coal | Hard coal (aggregate) |
| `C0110` | anthracite | Anthracite |
| `C0121` | coking_coal | Coking coal |
| `C0129` | other_bituminous_coal | Other bituminous coal |
| `C0210` | lignite | Brown coal/lignite |
| `C0220` | sub_bituminous_coal | Sub-bituminous coal |
| `G3000` | natural_gas | Natural gas |
| `G3200` | lng | Liquefied natural gas |
| `O4000XBIO` | oil | Oil excluding biofuels |
| `O4100_TOT` | crude_oil | Crude oil |
| `O4200` | ngl | Natural gas liquids |
| `E7000` | electricity | Electricity |
| `S2000` | nuclear_fuels | Nuclear fuels |
| `P1100` | peat | Peat |
| `TOTAL` | total | All fuels combined |

Note: `CF_R` (renewable_fuels) and `SFF_OTH` (other_solid_fossil_fuels) are excluded from this dataset as they only have third_countries data with no overall dependency values.

---

## Energy Type Units

| Code | Name | Unit | Description |
|------|------|------|-------------|
| `SFF` | coal | THS_T | Thousand tonnes |
| `OIL` | oil | THS_T | Thousand tonnes |
| `GAS` | gas | TJ_GCV | Terajoules (Gross Calorific Value) |
| `BIO` | biofuels | THS_T | Thousand tonnes |
| `EH` | electricity | GWH | Gigawatt-hours |

---

## Regional Aggregate Codes

Some partner codes represent regional aggregates rather than individual countries:

| Code | Description |
|------|-------------|
| `EUR_OTH` | Other European countries |
| `AFR_OTH` | Other African countries |
| `AME_OTH` | Other American countries |
| `ASI_OTH` | Other Asian countries |
| `ASI_NME_OTH` | Other non-Middle Eastern Asian countries |

---

## Notes

1. **All Partners Included**: The `partners` array includes all trading partners with non-zero shares, sorted by share percentage descending. Unlike some datasets, this is not limited to top N partners.

2. **Null Values**: Fields may be `null` when data is not available in the source dataset for that country/year/indicator combination.

3. **Negative Dependency**: Dependency values can be negative for net exporters. For example, a country that exports more of a fuel than it imports will have negative dependency for that fuel.

4. **Values >100%**: Dependency values above 100% indicate stock changes, statistical adjustments, or re-exports in the source data.

5. **Share Aggregation**: Partner shares are calculated by aggregating trade values across all energy types. Since different energy types use different units (tonnes vs TJ vs GWh), gas values (in TJ) may dominate the aggregate ranking due to their larger numeric values.

6. **Time Range**: Data spans 1990-2024, though not all countries have data for all years. Earlier years may have sparser coverage.

---

## Third Countries Definition

In Eurostat and EU terminology, **"third countries"** refers to countries that are **not members of the European Union**. This includes:

- Non-EU European countries (e.g., Norway, Switzerland, UK post-Brexit)
- All countries outside Europe (e.g., Russia, USA, Saudi Arabia, China)

The `ID3CF` indicator specifically measures what percentage of a country's energy imports come from these non-EU sources. This is an important metric for assessing the EU's external energy vulnerability and strategic autonomy.

**Data Availability**: Third country import dependency data (ID3CF) is only available from **2010 onwards**. Years before 2010 will have `null` values for all `third_countries` fields.

For example, if Germany has:
- `dependency.overall`: 66% (total import dependency)
- `dependency.third_countries`: 48% (imports from non-EU countries)

This means 66% of Germany's energy needs are met by imports, and 48% of total energy comes from countries outside the EU (i.e., roughly 73% of imports are from third countries).

---

## Why No Electricity Import Dependency

Eurostat does not publish an overall import dependency rate (ID indicator) for electricity. The `electricity.overall` field is always `null`. Only `electricity.third_countries` is available.

### Why Eurostat Doesn't Calculate It

**Mixed Grids**: Once electricity enters the interconnected European grid, electrons from different sources (domestic production, imports, renewables) mix together. Unlike physical fuels that can be tracked from origin to destination, electricity flows are fungible and origin is difficult to define meaningfully.

**Intra-EU Trade for Balancing**: The EU single electricity market treats cross-border electricity trade largely as internal grid balancing, not external dependency. The EU collectively generates enough electricity, but individual countries import/export to manage supply and demand fluctuations throughout the day.

**Focus on Primary Fuels**: The standard energy dependency metric is designed to measure reliance on imported **primary fuels** (coal, oil, gas) that enter the country and are consumed or transformed. These represent clearer indicators of external vulnerability and strategic dependence.

### What Eurostat Does Provide

- **Overall Energy Dependency**: The aggregate rate (e.g., 63% for EU in 2022) shows reliance on net imports for all energy needs
- **Energy Balances**: They track electricity production, consumption, and trade (imports/exports) for each country
- **Fuel-Specific Imports**: They show import dependency for specific fuels like natural gas or crude oil, highlighting true external reliance
- **Third Country Electricity**: The `ID3CF` indicator IS available for electricity, showing what percentage of electricity imports come from non-EU countries

### Data Available in This Dataset

For electricity, you can still find:
- `dependency.by_fuel.electricity.third_countries`: % of electricity imports from non-EU
- `imports.total_by_type.EH`: Total electricity imports (GWh)
- `exports.total_by_type.EH`: Total electricity exports (GWh)
- `imports.partners` / `exports.partners`: Trading partners (includes electricity trade)
