# Eurostat Energy Datasets - Documentation

This folder contains Eurostat energy datasets.

## Contents

### Files

| File | Description | Rows | Time Range |
|------|-------------|------|------------|
| `eurostat_energy_productivity_2000-2024.csv` | SDG 7.30 - Energy productivity | 75 | 2000-2024 |
| `eurostat_energy_balance_1990-2024.csv` | Energy balance - Complete | 1.2M | 1990-2024 |

### Subfolders

| Folder | Description |
|--------|-------------|
| `consumption_eurostat_sectors/` | Combined sector consumption (3.2M rows) |

See `consumption_eurostat_sectors/README.md` for details.

**Note:** Energy productivity (SDG 7.30) = GDP / Gross Inland Consumption. The balance dataset contains `GIC` (energy consumption denominator) but NOT GDP. To calculate energy productivity yourself, you would need GDP data from Eurostat's national accounts (nama_10_gdp).

---

## Common Columns (All Files)

### `freq` - Frequency
| Code | Description |
|------|-------------|
| `A` | Annual |

### `geo` - Geographic Area
Standard Eurostat country codes (ISO 3166-1 alpha-2 with some modifications):

| Code | Country/Region |
|------|----------------|
| `AL` | Albania |
| `AT` | Austria |
| `BA` | Bosnia and Herzegovina |
| `BE` | Belgium |
| `BG` | Bulgaria |
| `CY` | Cyprus |
| `CZ` | Czechia |
| `DE` | Germany |
| `DK` | Denmark |
| `EE` | Estonia |
| `EL` | Greece (Eurostat uses EL, not GR) |
| `ES` | Spain |
| `EU27_2020` | EU 27 countries (post-Brexit composition) |
| `FI` | Finland |
| `FR` | France |
| `GE` | Georgia |
| `HR` | Croatia |
| `HU` | Hungary |
| `IE` | Ireland |
| `IS` | Iceland |
| `IT` | Italy |
| `LT` | Lithuania |
| `LU` | Luxembourg |
| `LV` | Latvia |
| `MD` | Moldova |
| `ME` | Montenegro |
| `MK` | North Macedonia |
| `MT` | Malta |
| `NL` | Netherlands |
| `NO` | Norway |
| `PL` | Poland |
| `PT` | Portugal |
| `RO` | Romania |
| `RS` | Serbia |
| `SE` | Sweden |
| `SI` | Slovenia |
| `SK` | Slovakia |
| `TR` | Turkey |
| `UA` | Ukraine |
| `UK` | United Kingdom |
| `XK` | Kosovo |

### `TIME_PERIOD` - Years
Columns representing years (e.g., 2000, 2001, ..., 2024). Values are numeric or `:` (missing data).

---

## eurostat_energy_productivity_2000-2024.csv - Energy Productivity

**Source:** [SDG 7 - Affordable and Clean Energy](https://ec.europa.eu/eurostat/web/sdi/affordable-and-clean-energy)

### `unit` - Unit of Measurement
| Code | Description |
|------|-------------|
| `EUR_KGOE` | Euro per kilogram of oil equivalent - Measures GDP generated per unit of energy consumed (in chain-linked volumes, reference year 2015) |
| `PPS_KGOE` | Purchasing Power Standard per kilogram of oil equivalent - Same as above but adjusted for price level differences between countries |

**Interpretation:** Higher values = more energy-efficient economy (more GDP generated per unit of energy consumed).

---

## eurostat_energy_balance_1990-2024.csv - Energy Balance

**Source:** [Eurostat Energy Balance](https://ec.europa.eu/eurostat/web/energy/database)

### `unit` - Unit of Measurement
| Code | Description |
|------|-------------|
| `KTOE` | Kilotonnes of oil equivalent (1 ktoe = 41.868 TJ) |
| `GWH` | Gigawatt-hours |
| `TJ` | Terajoules |

### `nrg_bal` - Energy Balance Flows

Reference: [Eurostat Energy Balance Guide](https://ec.europa.eu/eurostat/documents/38154/4956218/Energy-balance-guide-draft-31Jan2019.pdf)

#### Supply Side
| Code | Description |
|------|-------------|
| `PPRD` | Primary production |
| `RCV_RCY` | Recovered and recycled products |
| `IMP` | Imports |
| `EXP` | Exports |
| `STK_CHG` | Stock changes |
| `STK_BLD` | Stock build |
| `STK_DRW` | Stock draw |
| `NRGSUP` | Energy supply |
| `GIC` | Gross inland consumption |
| `GIC_EED` | Gross inland consumption (EED definition) |
| `GIC2020-2030` | Gross inland consumption (2020-2030 target) |

#### Available for Final Consumption
| Code | Description |
|------|-------------|
| `AFC` | Available for final consumption |

#### Transformation Input (TI_)
| Code | Description |
|------|-------------|
| `TI_E` | Transformation input - Total |
| `TI_EHG_E` | Electricity and heat generation |
| `TI_EHG_MAPCHP_E` | Main activity producer CHP plants |
| `TI_EHG_MAPE_E` | Main activity producer electricity only |
| `TI_EHG_MAPH_E` | Main activity producer heat only |
| `TI_EHG_APCHP_E` | Autoproducer CHP plants |
| `TI_EHG_APE_E` | Autoproducer electricity only |
| `TI_EHG_APH_E` | Autoproducer heat only |
| `TI_CO_E` | Coke ovens |
| `TI_BF_E` | Blast furnaces |
| `TI_GW_E` | Gas works |
| `TI_RPI_E` | Refineries and petrochemical industry |
| `TI_RPI_RI_E` | Refineries |
| `TI_RPI_PII_E` | Petrochemical industry |

#### Transformation Output (TO_)
| Code | Description |
|------|-------------|
| `TO` | Transformation output - Total |
| `TO_EHG` | Electricity and heat generation |
| `TO_EHG_MAPCHP` | Main activity producer CHP |
| `TO_EHG_MAPE` | Main activity producer electricity only |
| `TO_EHG_MAPH` | Main activity producer heat only |
| `TO_EHG_APCHP` | Autoproducer CHP |
| `TO_EHG_APE` | Autoproducer electricity only |
| `TO_EHG_APH` | Autoproducer heat only |
| `TO_CO` | Coke ovens output |
| `TO_BF` | Blast furnaces output |
| `TO_GW` | Gas works output |
| `TO_RPI` | Refineries and petrochemical |

#### Energy Sector Consumption (NRG_)
| Code | Description |
|------|-------------|
| `NRG_E` | Energy sector - Total |
| `NRG_EHG_E` | Electricity and heat generation |
| `NRG_CO_E` | Coke ovens |
| `NRG_BF_E` | Blast furnaces |
| `NRG_GW_E` | Gas works |
| `NRG_OIL_NG_E` | Oil and gas extraction |
| `NRG_PR_E` | Petroleum refineries |
| `NRG_CM_E` | Coal mines |
| `NRG_LNG_E` | Liquefaction/regasification plants |
| `NRG_BIOG_E` | Biogas production |
| `NRG_PF_E` | Patent fuel plants |

#### Final Consumption - Total (FC_)
| Code | Description |
|------|-------------|
| `FC_E` | Final consumption - Total energy use |
| `FC_NE` | Final consumption - Non-energy use |

#### Final Consumption - Industry (FC_IND_)
| Code | Description |
|------|-------------|
| `FC_IND_E` | Industry - Total |
| `FC_IND_IS_E` | Iron and steel |
| `FC_IND_NFM_E` | Non-ferrous metals |
| `FC_IND_NMM_E` | Non-metallic minerals |
| `FC_IND_CPC_E` | Chemical and petrochemical |
| `FC_IND_MQ_E` | Mining and quarrying |
| `FC_IND_FBT_E` | Food, beverages and tobacco |
| `FC_IND_TL_E` | Textile and leather |
| `FC_IND_PPP_E` | Paper, pulp and printing |
| `FC_IND_WP_E` | Wood and wood products |
| `FC_IND_CON_E` | Construction |
| `FC_IND_MAC_E` | Machinery |
| `FC_IND_TE_E` | Transport equipment |
| `FC_IND_NSP_E` | Not elsewhere specified |

#### Final Consumption - Transport (FC_TRA_)
| Code | Description |
|------|-------------|
| `FC_TRA_E` | Transport - Total |
| `FC_TRA_RAIL_E` | Rail |
| `FC_TRA_ROAD_E` | Road |
| `FC_TRA_DAVI_E` | Domestic aviation |
| `FC_TRA_DNAVI_E` | Domestic navigation |
| `FC_TRA_PIPE_E` | Pipeline transport |
| `FC_TRA_NSP_E` | Not elsewhere specified |

#### Final Consumption - Other Sectors (FC_OTH_)
| Code | Description |
|------|-------------|
| `FC_OTH_E` | Other sectors - Total |
| `FC_OTH_HH_E` | Households |
| `FC_OTH_CP_E` | Commercial and public services |
| `FC_OTH_AF_E` | Agriculture/Forestry |
| `FC_OTH_FISH_E` | Fishing |
| `FC_OTH_NSP_E` | Not elsewhere specified |

#### Electricity/Heat Generation (GEP_, GHP_)
| Code | Description |
|------|-------------|
| `GEP` | Gross electricity production |
| `GEP_MAPCHP` | Gross electricity - Main activity CHP |
| `GEP_MAPE` | Gross electricity - Main activity electricity only |
| `GEP_APCHP` | Gross electricity - Autoproducer CHP |
| `GEP_APE` | Gross electricity - Autoproducer electricity only |
| `GHP` | Gross heat production |
| `GHP_MAPCHP` | Gross heat - Main activity CHP |
| `GHP_MAPH` | Gross heat - Main activity heat only |
| `GHP_APCHP` | Gross heat - Autoproducer CHP |
| `GHP_APH` | Gross heat - Autoproducer heat only |

#### Other
| Code | Description |
|------|-------------|
| `GAE` | Gross available energy |
| `DL` | Distribution losses |
| `INTAVI` | International aviation bunkers |
| `INTMARB` | International maritime bunkers |
| `STATDIFF` | Statistical difference |
| `FEC_EED` | Final energy consumption (EED) |
| `FEC2020-2030` | Final energy consumption (2020-2030) |
| `PEC_EED` | Primary energy consumption (EED) |
| `PEC2020-2030` | Primary energy consumption (2020-2030) |

### `siec` - Standard International Energy Product Classification

Reference: [SIEC 2019 Classification](https://ec.europa.eu/eurostat/ramon/nomenclatures/index.cfm?TargetUrl=LST_NOM_DTL&StrNom=CL_SIEC&StrLanguageCode=EN)

#### Solid Fossil Fuels (C)
| Code | Description |
|------|-------------|
| `C0000X0350-0370` | Solid fossil fuels (excluding peat) |
| `C0110` | Anthracite |
| `C0121` | Coking coal |
| `C0129` | Other bituminous coal |
| `C0210` | Sub-bituminous coal |
| `C0220` | Lignite |
| `C0311` | Coke oven coke |
| `C0312` | Gas coke |
| `C0320` | Coal tar |
| `C0330` | Patent fuel (BKB) |
| `C0340` | Gas works gas |
| `C0350` | Peat |
| `C0350-0370` | Peat and peat products |
| `C0360` | Peat products |
| `C0371` | Oil shale and oil sands |
| `C0379` | Other |

#### Manufactured Gases (G)
| Code | Description |
|------|-------------|
| `G3000` | Natural gas |
| `G3000_C0350-370` | Natural gas and peat products |

#### Heat (H)
| Code | Description |
|------|-------------|
| `H8000` | Heat |

#### Nuclear (N)
| Code | Description |
|------|-------------|
| `N900H` | Nuclear heat |

#### Oil and Petroleum Products (O)
| Code | Description |
|------|-------------|
| `O4000XBIO` | Oil and petroleum products (excluding biofuels) |
| `O4100_TOT` | Crude oil, NGL, and other hydrocarbons |
| `O4200` | Natural gas liquids |
| `O4200-4500` | Feedstocks |
| `O4300` | Refinery feedstocks |
| `O4400X4410` | Additives and oxygenates (excl. biofuels) |
| `O4500` | Other hydrocarbons |
| `O4610` | Refinery gas |
| `O4620` | Ethane |
| `O4630` | Liquefied petroleum gases |
| `O4640` | Naphtha |
| `O4651` | Motor gasoline (excl. biofuels) |
| `O4652XR5210B` | Motor gasoline (excl. biofuel portion) |
| `O4653` | Aviation gasoline |
| `O4661XR5230B` | Kerosene (excl. biofuel portion) |
| `O4669` | Other kerosene |
| `O4671XR5220B` | Road diesel (excl. biofuel portion) |
| `O4680` | Fuel oil |
| `O4691` | White spirit |
| `O4692` | Lubricants |
| `O4693` | Bitumen |
| `O4694` | Paraffin waxes |
| `O4695` | Petroleum coke |
| `O4699` | Other oil products |

#### Electricity (E)
| Code | Description |
|------|-------------|
| `E7000` | Electricity |

#### Renewables (R)
| Code | Description |
|------|-------------|
| `RA000` | Renewables and biofuels - Total |
| `RA100` | Hydro |
| `RA200` | Geothermal |
| `RA300` | Wind |
| `RA410` | Solar thermal |
| `RA420` | Solar photovoltaic |
| `RA500` | Tide, wave, ocean |
| `RA500_5160` | Ambient heat and other renewables |
| `RA600` | Ambient heat (heat pumps) |
| `R5110-5150_W6000RI` | Primary solid biofuels and renewable waste |
| `R5160` | Charcoal |
| `R5200` | Biogases |
| `R5210B` | Biogasoline (blended) |
| `R5210P` | Pure biogasoline |
| `R5220B` | Biodiesels (blended) |
| `R5220P` | Pure biodiesels |
| `R5230B` | Bio jet kerosene (blended) |
| `R5230P` | Pure bio jet kerosene |
| `R5290` | Other liquid biofuels |
| `R5300` | Non-renewable waste |

#### Bioenergy and Special Aggregates
| Code | Description |
|------|-------------|
| `BIOE` | Bioenergy |
| `FE` | Final energy |
| `P1000` | Nuclear fuel |
| `P1100` | Uranium |
| `P1200` | Plutonium |
| `S2000` | Secondary fuels |
| `TOTAL` | Total all products |

#### Waste (W)
| Code | Description |
|------|-------------|
| `W6100` | Industrial waste (non-renewable) |
| `W6100_6220` | Industrial waste and municipal waste |
| `W6210` | Municipal waste (renewable) |
| `W6220` | Municipal waste (non-renewable) |

#### Other
| Code | Description |
|------|-------------|
| `SFF_OTH` | Other solid fossil fuels |
| `SFF_P1000` | Solid fossil fuels and nuclear |
| `PP_OTH` | Other petroleum products |

---

## Missing Data

The character `:` represents missing or confidential data.

---

## Resources

- **Eurostat Energy Statistics:** https://ec.europa.eu/eurostat/web/energy
- **Energy Balance Guide:** https://ec.europa.eu/eurostat/documents/38154/4956218/Energy-balance-guide-draft-31Jan2019.pdf
- **SIEC Classification:** https://ec.europa.eu/eurostat/ramon/nomenclatures/index.cfm?TargetUrl=LST_NOM_DTL&StrNom=CL_SIEC
- **Country Codes:** https://ec.europa.eu/eurostat/statistics-explained/index.php/Glossary:Country_codes
- **SDG Indicators:** https://ec.europa.eu/eurostat/web/sdi/affordable-and-clean-energy
- **nrg_bal codes (Code List):** https://ec.europa.eu/eurostat/ramon/nomenclatures/index.cfm?TargetUrl=LST_NOM_DTL&StrNom=CL_NRG_BAL

---

## Notes

1. **CHP** = Combined Heat and Power
2. **Main Activity Producers** = Entities whose primary purpose is electricity/heat generation
3. **Autoproducers** = Entities that generate electricity/heat primarily for their own use
4. **EED** = Energy Efficiency Directive definition
5. **ktoe** = 1000 tonnes of oil equivalent = 41.868 TJ = 11,630 GWh
