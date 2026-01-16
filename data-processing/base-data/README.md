# Project Fundamental Data

Energy data collection for visualization project.

## Overview

| Folder | Description | Key Files | Total Rows |
|--------|-------------|-----------|------------|
| `01_Energy-Consumption/` | Global energy consumption (OWID) | Excel + codebook | ~22K |
| `02_Energy-Sector-Consumption/` | Sector breakdown (IEA) | 22 CSVs + Excel | ~60K |
| `03_Eurostat-Energy-Statistics/` | EU energy balances & productivity | 2 CSVs + combined | ~4.5M |
| `04_Energy-Metrics/` | Efficiency indicators | Combined CSV + Excel | ~163K |
| `05_Energy-Imports-Exports/` | EU trade & dependency | 2 combined CSVs | ~32M |

**Total**: ~36M+ rows of energy data

## Data Sources

| Source | Datasets |
|--------|----------|
| **Our World in Data** | Global energy consumption |
| **IEA** | Sector consumption, efficiency, electricity access |
| **Eurostat** | EU energy balances, trade, indicators |

## Folder Structure

```
project-fundamental-data/
├── 01_Energy-Consumption/
│   ├── owid-energy-data.xlsx        # Main global dataset
│   └── owid-energy-codebook.csv     # Column definitions
│
├── 02_Energy-Sector-Consumption/
│   ├── end_uses_efficiency/         # IEA efficiency indicators
│   │   ├── *_energy.csv             # Sector energy consumption
│   │   ├── *_emissions.csv          # CO2 emissions
│   │   └── *_indicators.csv         # Efficiency metrics
│   └── WorldEnergyBalancesHighlights2025.xlsx
│
├── 03_Eurostat-Energy-Statistics/
│   ├── eurostat_energy_balance_1990-2024.csv  # Energy balance (1.2M rows)
│   ├── eurostat_energy_productivity_2000-2024.csv  # Energy productivity
│   └── consumption_eurostat_sectors/
│       └── output/eurostat_sector_consumption_combined_2010-2023.csv  # 3.2M rows
│
├── 04_Energy-Metrics/
│   ├── electricity_indicators_eurostat/
│   │   └── output/combined_electricity_indicators.csv  # 163K rows
│   └── WEO2023 - Electricity access database.xlsx
│
└── 05_Energy-Imports-Exports/
    ├── energy_trade_eurostat/
    │   └── output/combined_energy_trade.csv  # 31.8M rows, 1.3GB
    └── import_dependency_eurostat/
        └── output/combined_import_dependency.csv  # 53K rows
```

## Geographic Coverage

| Dataset | Coverage |
|---------|----------|
| OWID | 200+ countries globally |
| IEA | 50+ countries (IEA members + associates) |
| Eurostat | 41 EU/EEA countries + neighbors |

## Time Coverage

| Dataset | Years |
|---------|-------|
| OWID | 1900-2024 (varies) |
| IEA | 2000-2023 |
| Eurostat | 1990-2024 |

## Key Metrics Available

### Consumption
- Primary energy by source (coal, oil, gas, nuclear, renewables)
- Electricity generation by source
- Per capita consumption
- Sector breakdown (industry, residential, services, transport)

### Efficiency
- Energy intensity (energy per GDP)
- Energy productivity (GDP per energy)
- Rate of electrification
- Carbon intensity

### Trade
- Import/export volumes by energy type
- Trade partners
- Import dependency ratios

## File Formats

| Format | Usage |
|--------|-------|
| `.csv` | Most data files |
| `.xlsx` / `.xlsb` | IEA source files |
| `.tsv.gz` | Eurostat originals (archived) |

## Special Values

| Value | Meaning |
|-------|---------|
| NaN / empty | Missing data |
| `:` | Confidential/unavailable (Eurostat) |
| `..` | Not available (IEA) |
| Negative | Net exports (dependency data) |

## Notes

- Combined CSVs are derived from original Eurostat sources
- Conversion scripts are in `scripts/` subfolders
- Original compressed files in `originals/` subfolders
- See individual folder READMEs for detailed documentation
