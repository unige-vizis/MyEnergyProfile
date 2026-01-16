# Energy Consumption by Sector (Eurostat)

Combined dataset from 4 Eurostat sector consumption sources.

## Output File

`output/eurostat_sector_consumption_combined_2010-2023.csv`

| Property | Value |
|----------|-------|
| Rows | 3,238,326 |
| Columns | 8 |
| Size | ~128 MB |

## Columns

| Column | Type | Unique | Description |
|--------|------|--------|-------------|
| `sector` | string | 4 | Economic sector |
| `freq` | string | 1 | Frequency (A = Annual) |
| `siec` | string | 60 | Energy product code |
| `unit` | string | 5 | Measurement unit |
| `geo` | string | 41 | Country/region code |
| `category` | string | 156 | Sector-specific category |
| `year` | int | 14 | 2010-2023 |
| `value` | float | - | Consumption value (NaN = missing) |

## Sector Codes

| Code | Name | Source | Year Range |
|------|------|--------|------------|
| HH | Households | nrg_d_hhq | 2010-2023 |
| IND | Industry | nrg_d_indq_n | 2017-2023 |
| SER | Services | nrg_d_serq_n | 2020-2023 |
| TRA | Transport | nrg_d_traq | 2020-2023 |

## Unit Codes

| Code | Description |
|------|-------------|
| GWH | Gigawatt-hours |
| THS_T | Thousand tonnes |
| TJ | Terajoules |
| TJ_GCV | Terajoules (gross calorific value) |
| TJ_NCV | Terajoules (net calorific value) |

## Category Column

Contains sector-specific classifications:
- **HH**: Energy balance codes (FC_OTH_HH_E, etc.)
- **IND/SER**: NACE Rev.2 industry codes (B07-B09, C10, etc.)
- **TRA**: Transport mode + balance (e.g., FR|FC_TRA_DAVI_E)

## Geo Codes (sample)

| Code | Country |
|------|---------|
| DE | Germany |
| FR | France |
| AT | Austria |
| EU27_2020 | European Union (27) |
| EA20 | Euro area (20) |

## Null Values

~2.3M null values in `value` column (expected due to different time ranges per sector).

## Source

Eurostat: nrg_d_hhq, nrg_d_indq_n, nrg_d_serq_n, nrg_d_traq
