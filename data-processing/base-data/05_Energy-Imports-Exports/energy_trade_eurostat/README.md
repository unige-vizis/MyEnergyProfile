# Energy Trade - Imports & Exports (Eurostat)

Combined dataset from 10 Eurostat energy trade sources.

## Flow Types

| Code | Description |
|------|-------------|
| IMPORT | Energy imports by partner country |
| EXPORT | Energy exports by partner country |

## Energy Types

| Code | Name | Unit |
|------|------|------|
| SFF | Solid fossil fuels (coal) | THS_T (thousand tonnes) |
| OIL | Oil & petroleum products | THS_T (thousand tonnes) |
| GAS | Natural gas | TJ_GCV (terajoules) |
| BIO | Biofuels | THS_T (thousand tonnes) |
| EH | Electricity & derived heat | GWH (gigawatt hours) |

## Columns

- `flow` - IMPORT or EXPORT
- `energy_type` - SFF, OIL, GAS, BIO, EH
- `freq` - Frequency (A = Annual)
- `siec` - Detailed energy product code
- `partner` - Trade partner country code
- `unit` - Measurement unit
- `geo` - Reporting country
- `year` - 1990-2024
- `value` - Trade volume (NaN = missing)

## Statistics

| Property | Value |
|----------|-------|
| Total rows | 31,855,320 |
| File size | 1.3 GB |
| Countries | 43 |
| Partners | 200+ |
| Years | 1990-2024 (35 years) |

### Rows by Flow & Energy Type

| Flow | SFF | OIL | GAS | BIO | EH |
|------|-----|-----|-----|-----|-----|
| IMPORT | 3.5M | 9.4M | 993K | 1.5M | 497K |
| EXPORT | 3.5M | 9.4M | 993K | 1.5M | 497K |

### Null Values

~6.5M null values in `value` column (data gaps for certain country-partner-year combinations).

## Source

Eurostat: nrg_ti_sff, nrg_ti_oil, nrg_ti_gas, nrg_ti_bio, nrg_ti_eh,
nrg_te_sff, nrg_te_oil, nrg_te_gas, nrg_te_bio, nrg_te_eh
