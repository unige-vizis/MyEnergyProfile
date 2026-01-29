# OWID Energy Data

Global energy consumption dataset from Our World in Data.

## Files

| File | Description |
|------|-------------|
| `owid-energy-data.xlsx` | Main dataset (Excel format) |
| `owid-energy-codebook.csv` | Column definitions and metadata |

## Dataset Overview

- **Rows**: ~22,000+ (countries × years)
- **Columns**: 130
- **Time Range**: 1900-2024 (varies by indicator)
- **Coverage**: 200+ countries and regions

## Key Columns

| Column | Description | Unit |
|--------|-------------|------|
| `country` | Country or region name | - |
| `year` | Year of observation | - |
| `iso_code` | ISO 3166-1 alpha-3 code | - |
| `population` | Population | people |
| `gdp` | GDP (PPP, 2011 prices) | international-$ |

## Energy Categories

### Consumption (TWh)
- `coal_consumption`, `oil_consumption`, `gas_consumption`
- `nuclear_consumption`, `hydro_consumption`
- `solar_consumption`, `wind_consumption`
- `biofuel_consumption`, `other_renewables_consumption`
- `fossil_fuel_consumption`, `renewables_consumption`
- `primary_energy_consumption`

### Electricity Generation (TWh)
- `coal_electricity`, `oil_electricity`, `gas_electricity`
- `nuclear_electricity`, `hydro_electricity`
- `solar_electricity`, `wind_electricity`
- `fossil_electricity`, `renewables_electricity`
- `electricity_generation`

### Per Capita (kWh/person)
- `*_per_capita` variants for most metrics

### Shares (%)
- `*_share_energy` - share of primary energy
- `*_share_elec` - share of electricity generation

### Production (TWh)
- `coal_production`, `oil_production`, `gas_production`

### Carbon Metrics
- `carbon_intensity_elec` - gCO2/kWh

## Special Values

- Empty/NaN = Data not available
- See codebook for detailed definitions

## Sources

Primary sources (via OWID):
- Energy Institute - Statistical Review of World Energy (2025)
- Ember - Yearly Electricity Data (2025)
- U.S. Energy Information Administration (2025)
- Maddison Project Database (GDP)

## Usage

```python
import pandas as pd

# Load data
df = pd.read_excel('owid-energy-data.xlsx')

# Filter by country
germany = df[df['country'] == 'Germany']

# Get renewable share over time
renewable_trend = df[['country', 'year', 'renewables_share_energy']]
```

## Source

Our World in Data: https://github.com/owid/energy-data
