# Energy Imports & Exports

EU energy trade and import dependency data from Eurostat.

## Datasets

### energy_trade_eurostat/
Energy imports and exports by partner country and energy type.

**Output**: `combined_energy_trade.csv`

| Property | Value |
|----------|-------|
| Rows | 31.8M |
| Size | 1.3 GB |
| Years | 1990-2024 |

| Flow | Energy Types |
|------|--------------|
| IMPORT | SFF, OIL, GAS, BIO, EH |
| EXPORT | SFF, OIL, GAS, BIO, EH |

Energy type codes:
- **SFF** - Solid fossil fuels (coal)
- **OIL** - Oil & petroleum products
- **GAS** - Natural gas
- **BIO** - Biofuels
- **EH** - Electricity & derived heat

See `energy_trade_eurostat/README.md` for details.

### import_dependency_eurostat/
Energy import dependency indicators.

**Output**: `combined_import_dependency.csv`

| Property | Value |
|----------|-------|
| Rows | 53K |
| Years | 1990-2024 |

| Indicator | Description |
|-----------|-------------|
| ID | General import dependency |
| ID3CF | Third countries by fuel |
| IDOGAS | Gas by origin country |
| IDOOIL | Oil by origin country |

See `import_dependency_eurostat/README.md` for details.

## Data Source

Eurostat energy trade statistics
