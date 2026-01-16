# IEA Energy End-uses and Efficiency Indicators Database - Highlights

## Overview
The IEA Energy End-uses and Efficiency Indicators database provides detailed end-use energy consumption data, activity metrics, and efficiency indicators across four sectors: residential, services, industry, and transport. This is the December 2025 Highlights edition.

## Data Source
- **Provider**: International Energy Agency (IEA)
- **Edition**: December 2025 Highlights
- **Last Update**: December 12, 2025
- **Next Update**: June 19, 2026
- **License**: Subject to IEA terms and conditions (https://www.iea.org/terms/)
- **Original Format**: XLSB (converted to CSV)

## Coverage
- **Time Period**: 2000, 2005, 2010, and 2015-2023
- **Countries**: 50+ countries including:
  - IEA Member countries (Australia, Austria, Belgium, Canada, Czech Republic, Denmark, Estonia, Finland, France, Germany, Greece, Hungary, Ireland, Italy, Japan, Korea, Latvia, etc.)
  - IEA Accession countries (Chile, Colombia)
  - IEA Association countries (Argentina, Brazil, Morocco, South Africa, Ukraine)
  - Additional countries (Albania, Armenia, Azerbaijan, Belarus, Bosnia and Herzegovina, Bulgaria, Croatia, Cyprus, etc.)

## Files (22 CSV files, 3.6 MB total)

### Documentation Files
| File | Size | Description |
|------|------|-------------|
| `contents.csv` | 2.6 KB | Database structure and contents overview |
| `coverage.csv` | 3.3 KB | Countries and time periods covered |
| `methodological_notes.csv` | 7.8 KB | Methodology documentation |

### Energy Consumption Data
| File | Size | Rows | Description |
|------|------|------|-------------|
| `industry_energy.csv` | 285 KB | 10,249 | Industry sector energy by sub-sector and product |
| `services_energy.csv` | 211 KB | 9,518 | Services sector energy by end-use and product |
| `residential_energy.csv` | 182 KB | 5,711 | Residential energy by end-use (heating, cooling, etc.) |
| `transport_energy.csv` | 300 KB | 9,822 | Transport energy by mode (cars, buses, rail, etc.) |
| `activity_data.csv` | 347 KB | 5,070 | Economic activity data (value-added, population) |

### Energy Indicators
| File | Size | Rows | Description |
|------|------|------|-------------|
| `industry_energy_indicators.csv` | 35 KB | 437 | Industry efficiency indicators |
| `services_energy_indicators.csv` | 91 KB | 1,160 | Services efficiency indicators |
| `residential_energy_indicators.csv` | 66 KB | 306 | Residential efficiency indicators |
| `transport_energy_indicators.csv` | 325 KB | 4,425 | Transport efficiency indicators |

### Emissions Data
| File | Size | Rows | Description |
|------|------|------|-------------|
| `industry_emissions.csv` | 108 KB | 1,282 | Industry CO2 emissions |
| `services_emissions.csv` | 50 KB | 1,408 | Services CO2 emissions |
| `residential_emissions.csv` | 79 KB | 1,221 | Residential CO2 emissions |
| `transport_emissions.csv` | 587 KB | 9,761 | Transport CO2 emissions |

### Carbon Indicators
| File | Size | Rows | Description |
|------|------|------|-------------|
| `industry_carbon_indicators.csv` | 12 KB | 56 | Industry carbon intensity |
| `services_carbon_indicators.csv` | 58 KB | 357 | Services carbon intensity |
| `residential_carbon_indicators.csv` | 67 KB | 459 | Residential carbon intensity |
| `transport_carbon_indicators.csv` | 63 KB | 1,506 | Transport carbon intensity |

### Decomposition Analysis
| File | Size | Rows | Description |
|------|------|------|-------------|
| `energy_decomposition.csv` | 282 KB | 946 | Energy consumption decomposition factors |
| `carbon_decomposition.csv` | 416 KB | 1,216 | Carbon emissions decomposition factors |

## Data Structure

### Energy Consumption Files
```csv
Country,End use,Product,2000.0,2005.0,2010.0,2015.0,...,2023.0
Australia,Space heating,Total final use (PJ),165.416,161.054,...,157.005
```

**Columns:**
- `Country`: Country name
- `End use`: Sector-specific end-use category
- `Product`: Energy product or "Total final use (PJ)"
- `2000.0` - `2023.0`: Values for each year

### Sector-Specific End Uses

#### Industry (ISIC codes)
- Food and tobacco [ISIC 10-12]
- Textiles and leather [ISIC 13-15]
- Wood and wood products [ISIC 16]
- Paper, pulp and printing [ISIC 17-18]
- Chemical and pharmaceutical products [ISIC 20-21]
- Non-metallic minerals [ISIC 23]
- Basic metals [ISIC 24]
- Machinery [ISIC 25-28]
- Transport equipment [ISIC 29-30]
- Mining and quarrying [ISIC 05-09]
- Construction [ISIC 41-43]

#### Residential
- Space heating
- Space cooling
- Water heating
- Cooking
- Lighting
- Appliances

#### Services
- Space heating
- Space cooling
- Water heating
- Lighting
- Other equipment

#### Transport
- Cars/light trucks
- Motorcycles
- Buses
- Trucks
- Rail (passenger and freight)
- Domestic navigation
- Domestic aviation
- Pipelines

## Units
- **PJ**: Petajoules (energy)
- **billion USD PPP**: Value-added (activity data)
- **million**: Population
- **Various**: Efficiency indicators (MJ/USD, kWh/m², etc.)

## Data Qualifiers
- `..` = Not available
- `0` = Zero or negligible
- Empty cell = No data

## Usage Examples

### Python
```python
import pandas as pd

# Load residential energy data
residential = pd.read_csv('residential_energy.csv', skiprows=1)

# Filter for space heating
heating = residential[residential['End use'] == 'Space heating']

# Get data for a specific country
germany = residential[residential['Country'] == 'Germany']

# Time series analysis
years = ['2000.0', '2005.0', '2010.0', '2015.0', '2020.0', '2023.0']
trends = residential[['Country', 'End use'] + years]
```

### Aggregating by Sector
```python
# Sum all end-uses for total sector consumption
sector_totals = residential.groupby('Country')[years].sum()
```

## Related IEA Resources
- Energy Efficiency Indicators Manual: https://www.iea.org/reports/energy-efficiency-indicators-fundamentals-on-statistics
- Full database (subscription): https://www.iea.org/data-and-statistics/data-product/energy-end-uses-and-efficiency-indicators
- Greenhouse Gas Emissions from Energy: https://www.iea.org/data-and-statistics/data-product/greenhouse-gas-emissions-from-energy

## Citation
```
IEA (2025), Energy End-uses and Efficiency Indicators, IEA, Paris
https://www.iea.org/data-and-statistics/data-product/energy-end-uses-and-efficiency-indicators
```

## Notes
- This is the Highlights (free) version with selected data
- Full database requires subscription (from EUR 660/year)
- The first row of each CSV contains the IEA copyright notice
- Years are formatted as floats (2000.0) due to Excel conversion
- Data updated twice yearly (June and December)
