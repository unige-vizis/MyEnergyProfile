# Energy Import Dependency (Eurostat)

Combined dataset from 4 Eurostat import dependency sources.

## Indicators

| Code | Name | Description |
|------|------|-------------|
| ID | Import dependency | General energy import dependency |
| ID3CF | Third countries by fuel | Import dependency on non-EU countries |
| IDOGAS | Gas by origin | Natural gas imports by source country |
| IDOOIL | Oil by origin | Oil/petroleum imports by source country |

## Columns

- `indicator` - ID, ID3CF, IDOGAS, IDOOIL
- `freq` - Frequency (A = Annual)
- `siec` - Energy product (C0000X0350-0370, G3000, O4000XBIO)
- `partner` - Trade partner/origin (country code or TOTAL/THRD)
- `unit` - PC (percentage)
- `geo` - Country code
- `year` - 1990-2024
- `value` - % dependency (NaN = missing, negative = net exporter)

## Partner Codes

| Code | Description |
|------|-------------|
| TOTAL | All partners (general) |
| THRD | Third countries (non-EU) |
| DZ | Algeria |
| RU | Russia |
| NO | Norway |
| AZ | Azerbaijan |
| etc. | Other origin countries |

## Statistics

| Property | Value |
|----------|-------|
| Total rows | 53,270 |
| Countries | 43 |
| Partners | 14 |
| Years | 1990-2024 |

### Rows by Indicator

| Indicator | Rows | Non-null |
|-----------|------|----------|
| ID | 19,110 | 17,498 |
| ID3CF | 8,330 | 3,304 |
| IDOGAS | 10,045 | 1,372 |
| IDOOIL | 15,785 | 2,574 |

## Source

Eurostat: nrg_ind_id, nrg_ind_id3cf, nrg_ind_idogas, nrg_ind_idooil
