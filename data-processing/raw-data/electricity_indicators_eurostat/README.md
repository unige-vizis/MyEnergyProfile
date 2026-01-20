# Electricity Indicators (Eurostat)

Combined dataset from 4 Eurostat energy indicator sources.

## Indicators

| Code | Name | Unit | Description |
|------|------|------|-------------|
| RE | Rate of electrification | PC (%) | Share of electricity in final energy consumption |
| EFF | Energy efficiency | PC, MTOE | Progress towards efficiency targets |
| EI | Energy intensity | KGOE_TEUR | Energy per unit of GDP |
| ESC | Energy supply per capita | GJ_HAB | Energy consumption per inhabitant |

## Columns

- `indicator` - RE, EFF, EI, ESC
- `freq` - Frequency (A = Annual)
- `siec` - Energy product (TOTAL)
- `nrg_bal` - Energy balance category
- `unit` - Measurement unit
- `geo` - Country code (EU countries)
- `year` - 1990-2024
- `value` - Numeric value (NaN = missing)

## Statistics

| Property | Value |
|----------|-------|
| Total rows | 163,205 |
| Countries | 44 |
| Years | 1990-2024 (35 years) |

### Rows by Indicator

| Indicator | Rows | Non-null |
|-----------|------|----------|
| RE | 55,930 | 43,947 |
| EFF | 25,340 | 3,076 |
| EI | 5,215 | 4,278 |
| ESC | 76,720 | 50,100 |

Note: EFF has mostly missing values (~88% null).

## Source

Eurostat: nrg_ind_re, nrg_ind_eff, nrg_ind_ei, nrg_ind_esc
