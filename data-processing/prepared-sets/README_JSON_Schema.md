# JSON Schema Documentation

## Required Header Format

All JSON files in `prepared-sets/` must include a header with a `sources` array that references:
1. Our combined/intermediate datasets
2. The original Eurostat dataset codes

**Example header:**
```json
{
  "header": {
    "sources": [
      "Eurostat energy trade (estat_nrg_ti_*, estat_nrg_te_*)",
      "Eurostat import dependency (estat_nrg_ind_id, estat_nrg_ind_id3cf)"
    ],
    "generated": "2024-01-15T10:30:00Z",
    "version": "1.0"
  },
  "data": { ... }
}
```

This ensures traceability back to original data sources for transparency and reproducibility.

---

## Example: Germany (DE) - 2023

This document explains every field in the JSON output using Germany 2023 as an example.
Each field includes an annotation describing its meaning and data source.

---

## Full JSON Structure (Annotated)

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

      "anthracite": {
        "overall": 100.0
        // Source: indicator='ID', siec='C0110'
        // Meaning: 100% of anthracite is imported (no domestic production)
      },

      "coking_coal": {
        "overall": 100.0
        // Source: indicator='ID', siec='C0121'
      },

      "other_bituminous": {
        "overall": 103.165
        // Source: indicator='ID', siec='C0129'
        // Note: >100% indicates stock drawdown or statistical adjustments
      },

      "lignite": {
        "overall": 0.0
        // Source: indicator='ID', siec='C0210'
        // Meaning: Germany produces all its lignite domestically
      },

      "C0220": {
        "overall": 0.054
        // Source: indicator='ID', siec='C0220' (sub-bituminous coal)
        // Note: SIEC code not mapped to readable name in script
      },

      "gas": {
        "overall": 93.66,
        // Source: indicator='ID', siec='G3000' (natural gas)
        // Meaning: Germany imports 93.7% of its natural gas

        "third_countries": 49.94
        // Source: indicator='ID3CF', siec='G3000'
        // Meaning: ~50% of gas imports from non-EU (was much higher pre-2022)
      },

      "oil": {
        "overall": 95.396,
        // Source: indicator='ID', siec='O4000XBIO' (oil excl. biofuels)

        "third_countries": 70.47
        // Source: indicator='ID3CF', siec='O4000XBIO'
      },

      "O4100_TOT": {
        "overall": 97.638
        // Source: indicator='ID', siec='O4100_TOT' (crude oil)
      },

      "O4200": {
        "overall": 0.0
        // Source: indicator='ID', siec='O4200' (NGL - natural gas liquids)
      },

      "P1100": {
        "overall": 0.0
        // Source: indicator='ID', siec='P1100' (oil shale)
      },

      "S2000": {
        "overall": 0.0
        // Source: indicator='ID', siec='S2000' (nuclear fuels)
      },

      "CF_R": {
        "third_countries": 6.1
        // Source: indicator='ID3CF', siec='CF_R' (renewable fuels)
      },

      "E7000": {
        "third_countries": 8.14
        // Source: indicator='ID3CF', siec='E7000' (electricity)
        // Meaning: 8.1% of electricity imports from non-EU
      },

      "SFF_OTH": {
        "third_countries": 0.0
        // Source: indicator='ID3CF', siec='SFF_OTH' (other solid fossil fuels)
      }
    },

    "gas_origins": {
      // ═════════════════════════════════════════════════════════════════════
      // GAS IMPORT ORIGINS BY COUNTRY (%)
      // Source: indicator='IDOGAS' from estat_nrg_ind_idogas
      // Note: Shows % share of gas imports from specific countries
      // ═════════════════════════════════════════════════════════════════════

      "DZ": null,  // Algeria - no data for 2023
      "NG": null,  // Nigeria
      "NO": null,  // Norway
      "QA": null,  // Qatar
      "RU": null,  // Russia
      "UK": null,  // United Kingdom
      "US": null   // United States
      // Note: null values indicate data not available in source
      // This indicator has limited coverage in Eurostat
    },

    "oil_origins": {
      // ═════════════════════════════════════════════════════════════════════
      // OIL IMPORT ORIGINS BY COUNTRY (%)
      // Source: indicator='IDOOIL' from estat_nrg_ind_idooil
      // ═════════════════════════════════════════════════════════════════════

      "AZ": null,  // Azerbaijan
      "DZ": null,  // Algeria
      "IQ": null,  // Iraq
      "KZ": null,  // Kazakhstan
      "LY": null,  // Libya
      "NG": null,  // Nigeria
      "NO": null,  // Norway
      "RU": null,  // Russia
      "SA": null,  // Saudi Arabia
      "UK": null,  // United Kingdom
      "US": null   // United States
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
      // Script location: process_trade_data() → imports_totals accumulator
      // ═════════════════════════════════════════════════════════════════════

      "SFF": {
        "value": 96128.47,
        "unit": "THS_T"
        // ┌─────────────────────────────────────────────────────────────────┐
        // │ SOLID FOSSIL FUELS (Coal)                                       │
        // │ Source: estat_nrg_ti_sff                                        │
        // │ Unit: Thousand tonnes                                           │
        // │ Meaning: Germany imported 96.1 million tonnes of coal in 2023  │
        // └─────────────────────────────────────────────────────────────────┘
      },

      "OIL": {
        "value": 609290.0,
        "unit": "THS_T"
        // ┌─────────────────────────────────────────────────────────────────┐
        // │ OIL & PETROLEUM PRODUCTS                                        │
        // │ Source: estat_nrg_ti_oil                                        │
        // │ Unit: Thousand tonnes                                           │
        // └─────────────────────────────────────────────────────────────────┘
      },

      "GAS": {
        "value": 2960810.36,
        "unit": "TJ_GCV"
        // ┌─────────────────────────────────────────────────────────────────┐
        // │ NATURAL GAS                                                     │
        // │ Source: estat_nrg_ti_gas                                        │
        // │ Unit: Terajoules (Gross Calorific Value)                       │
        // │ Note: 1 TJ ≈ 27,778 cubic meters of natural gas                │
        // └─────────────────────────────────────────────────────────────────┘
      },

      "BIO": {
        "value": 482.0,
        "unit": "THS_T"
        // ┌─────────────────────────────────────────────────────────────────┐
        // │ BIOFUELS                                                        │
        // │ Source: estat_nrg_ti_bio                                        │
        // │ Unit: Thousand tonnes                                           │
        // └─────────────────────────────────────────────────────────────────┘
      },

      "EH": {
        "value": 40624.0,
        "unit": "GWH"
        // ┌─────────────────────────────────────────────────────────────────┐
        // │ ELECTRICITY & HEAT                                              │
        // │ Source: estat_nrg_ti_eh                                         │
        // │ Unit: Gigawatt-hours                                            │
        // └─────────────────────────────────────────────────────────────────┘
      }
    },

    "top_partners": [
      // ═════════════════════════════════════════════════════════════════════
      // TOP 10 IMPORT PARTNERS
      // Calculated: Aggregated across all energy types, sorted by total value
      // Script location: calculate_shares_and_rankings()
      // Note: Shares are calculated from value sums, so gas (TJ) dominates
      //       due to larger numeric values compared to coal (THS_T)
      // ═════════════════════════════════════════════════════════════════════

      {
        "geo": "NO",
        // ┌─────────────────────────────────────────────────────────────────┐
        // │ ISO 3166-1 alpha-2 country code                                │
        // │ Source: 'partner' column in combined_energy_trade.csv          │
        // └─────────────────────────────────────────────────────────────────┘

        "name": "Norway",
        // ┌─────────────────────────────────────────────────────────────────┐
        // │ Full country name                                               │
        // │ Source: COUNTRY_NAMES lookup dict in script                    │
        // └─────────────────────────────────────────────────────────────────┘

        "share_pct": 33.94,
        // ┌─────────────────────────────────────────────────────────────────┐
        // │ Percentage share of total imports                              │
        // │ Calculated: (partner_value / grand_total) * 100                │
        // │ Note: Aggregated across ALL energy types (not per-type)        │
        // └─────────────────────────────────────────────────────────────────┘

        "is_eu": false
        // ┌─────────────────────────────────────────────────────────────────┐
        // │ EU membership status                                            │
        // │ Source: EU_MEMBERS list in script (EU27 as of 2020)            │
        // │ Note: Norway is EEA but not EU, so is_eu=false                 │
        // └─────────────────────────────────────────────────────────────────┘
      },
      {
        "geo": "NL",
        "name": "Netherlands",
        "share_pct": 22.61,
        "is_eu": true
      },
      {
        "geo": "BE",
        "name": "Belgium",
        "share_pct": 17.2,
        "is_eu": true
      },
      {
        "geo": "US",
        "name": "United States",
        "share_pct": 14.77,
        "is_eu": false
      },
      {
        "geo": "FR",
        "name": "France",
        "share_pct": 1.44,
        "is_eu": true
      },
      {
        "geo": "KZ",
        "name": "Kazakhstan",
        "share_pct": 1.24,
        "is_eu": false
      },
      {
        "geo": "LY",
        "name": "Libya",
        "share_pct": 1.2,
        "is_eu": false
      },
      {
        "geo": "UK",
        "name": "United Kingdom",
        "share_pct": 1.15,
        "is_eu": false
      },
      {
        "geo": "AU",
        "name": "Australia",
        "share_pct": 0.69,
        "is_eu": false
      },
      {
        "geo": "IQ",
        "name": "Iraq",
        "share_pct": 0.49,
        "is_eu": false
      }
    ],

    "by_partner_group": {
      // ═════════════════════════════════════════════════════════════════════
      // IMPORT SUMMARY BY PARTNER GROUP
      // Calculated: Sum of shares for EU vs non-EU partners
      // Script location: calculate_shares_and_rankings() → eu_total, third_total
      // ═════════════════════════════════════════════════════════════════════

      "eu": 42.24,
      // ┌─────────────────────────────────────────────────────────────────────┐
      // │ Percentage of imports from EU member states                        │
      // │ Calculated: Sum of share_pct where is_eu=true                      │
      // └─────────────────────────────────────────────────────────────────────┘

      "third_countries": 57.76
      // ┌─────────────────────────────────────────────────────────────────────┐
      // │ Percentage of imports from non-EU countries                        │
      // │ Calculated: Sum of share_pct where is_eu=false                     │
      // │ Note: eu + third_countries = 100%                                  │
      // └─────────────────────────────────────────────────────────────────────┘
    }
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
        // Germany exports 5.5 million tonnes of coal (mostly to neighbors)
      },
      "OIL": {
        "value": 148945.0,
        "unit": "THS_T"
        // Refined petroleum products exported
      },
      "GAS": {
        "value": 0.0,
        "unit": "TJ_GCV"
        // Zero gas exports in 2023 (Germany is gas importer, not exporter)
      },
      "BIO": {
        "value": 771.0,
        "unit": "THS_T"
      },
      "EH": {
        "value": 37309.0,
        "unit": "GWH"
        // Electricity exports to neighboring countries
      }
    },

    "top_partners": [
      {
        "geo": "NL",
        "name": "Netherlands",
        "share_pct": 22.78,
        "is_eu": true
      },
      {
        "geo": "AT",
        "name": "Austria",
        "share_pct": 18.33,
        "is_eu": true
      },
      {
        "geo": "PL",
        "name": "Poland",
        "share_pct": 12.79,
        "is_eu": true
      },
      {
        "geo": "CH",
        "name": "Switzerland",
        "share_pct": 11.88,
        "is_eu": false
        // Switzerland is not EU (but has bilateral agreements)
      },
      {
        "geo": "CZ",
        "name": "Czechia",
        "share_pct": 11.77,
        "is_eu": true
      },
      {
        "geo": "FR",
        "name": "France",
        "share_pct": 7.34,
        "is_eu": true
      },
      {
        "geo": "BE",
        "name": "Belgium",
        "share_pct": 5.73,
        "is_eu": true
      },
      {
        "geo": "UK",
        "name": "United Kingdom",
        "share_pct": 1.56,
        "is_eu": false
        // UK left EU in 2020, so is_eu=false
      },
      {
        "geo": "SE",
        "name": "Sweden",
        "share_pct": 1.1,
        "is_eu": true
      },
      {
        "geo": "HU",
        "name": "Hungary",
        "share_pct": 0.97,
        "is_eu": true
      }
    ],

    "by_partner_group": {
      "eu": 84.01,
      // 84% of German energy exports go to EU countries

      "third_countries": 15.99
      // Only 16% to non-EU (mainly Switzerland and UK)
    }
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
│  estat_nrg_ind_idogas  → IDOGAS       estat_nrg_ti_gas → IMPORT GAS         │
│  estat_nrg_ind_idooil  → IDOOIL       estat_nrg_ti_bio → IMPORT BIO         │
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
│  - indicator (ID, ID3CF, IDOGAS...)    - flow (IMPORT, EXPORT)              │
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
│           → Parses dependency CSV, extracts ID/ID3CF/IDOGAS/IDOOIL          │
│           → Maps SIEC codes to fuel names using SIEC_TO_FUEL dict           │
│                                                                              │
│  Phase 2: process_trade_data()                                              │
│           → Reads trade CSV in 500K chunks (31.8M rows total)               │
│           → Accumulates imports_by_partner and exports_by_partner           │
│           → Filters out TOTAL, THRD, NSP pseudo-partners                    │
│                                                                              │
│  Phase 3: calculate_shares_and_rankings()                                   │
│           → Calculates partner shares as % of total                         │
│           → Sorts partners by value, takes top 10                           │
│           → Classifies partners as EU/non-EU using EU_MEMBERS list          │
│                                                                              │
│  Phase 4: build_json_output()                                               │
│           → Combines dependency + trade data                                │
│           → Structures by country → year → metrics                          │
│           → Adds metadata and lookups                                       │
│                                                                              │
│  Phase 5: verify_output()                                                   │
│           → Validates country count, year range                             │
│           → Spot-checks sample values                                       │
│           → Verifies partner shares sum to 100%                             │
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
│    "metadata": { ... },                                                      │
│    "countries": {                                                            │
│      "DE": {                                                                 │
│        "years": {                                                            │
│          "2023": { ... }  ← THIS DOCUMENT EXPLAINS THIS STRUCTURE           │
│        }                                                                     │
│      }                                                                       │
│    },                                                                        │
│    "country_lookup": { ... },                                               │
│    "eu_members": [ ... ]                                                    │
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
| `C0129` | other_bituminous | Other bituminous coal |
| `C0210` | lignite | Brown coal/lignite |
| `G3000` | gas | Natural gas |
| `O4000XBIO` | oil | Oil excluding biofuels |
| `TOTAL` | total | All fuels combined |
| Other codes | (unmapped) | Kept as raw SIEC code |

---

## Key Script Constants

```python
# EU member states (used for is_eu classification)
EU_MEMBERS = [
    'AT', 'BE', 'BG', 'CY', 'CZ', 'DE', 'DK', 'EE', 'EL', 'ES',
    'FI', 'FR', 'HR', 'HU', 'IE', 'IT', 'LT', 'LU', 'LV', 'MT',
    'NL', 'PL', 'PT', 'RO', 'SE', 'SI', 'SK'
]

# Energy type units
ENERGY_TYPE_UNITS = {
    'SFF': 'THS_T',    # Thousand tonnes
    'OIL': 'THS_T',    # Thousand tonnes
    'GAS': 'TJ_GCV',   # Terajoules (gross calorific value)
    'BIO': 'THS_T',    # Thousand tonnes
    'EH': 'GWH'        # Gigawatt-hours
}
```

---

## Notes

1. **Aggregated Partners**: The `top_partners` list aggregates across all energy types. Gas (TJ) values dominate the ranking due to larger numeric values.

2. **Null Values**: `gas_origins` and `oil_origins` often contain null values because the IDOGAS/IDOOIL indicators have limited coverage in Eurostat.

3. **Negative Dependency**: Dependency values can be negative for net exporters (e.g., lignite in Germany = 0% because Germany produces all lignite domestically).

4. **Values >100%**: Dependency values above 100% indicate stock changes or statistical adjustments in the source data.
