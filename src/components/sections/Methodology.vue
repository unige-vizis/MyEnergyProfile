<template>
  <section id="methodology" class="page-section methodology">
    <h2>Methodology</h2>

    <h3>Data Sources</h3>
    <p>
      This application combines data from four primary sources to provide a comprehensive picture of European energy systems.
    </p>
    <ul>
      <li>
        <strong>Eurostat</strong> &mdash; The EU's statistical office provides the core trade and dependency data.
        Energy trade volumes (imports and exports by partner country) come from 10 datasets covering five energy types:
        solid fossil fuels, oil, natural gas, biofuels, and electricity
        (<code>estat_nrg_ti_sff</code>, <code>estat_nrg_te_sff</code>, etc.).
        Import dependency indicators come from four datasets
        (<code>estat_nrg_ind_id</code>, <code>estat_nrg_ind_id3cf</code>, <code>estat_nrg_ind_idogas</code>, <code>estat_nrg_ind_idooil</code>).
        Sector-level consumption data comes from household, industry, services, and transport datasets
        (<code>estat_nrg_d_hhq</code>, <code>estat_nrg_d_indq_n</code>, <code>estat_nrg_d_serq_n</code>, <code>estat_nrg_d_traq</code>).
        Coverage: 41 EU/EEA countries, 1990&ndash;2024.
      </li>
      <li>
        <strong>Our World in Data (OWID)</strong> &mdash; Provides global energy production and consumption figures (in TWh)
        for coal, oil, gas, biofuels, and electricity, as well as carbon intensity of electricity generation (gCO<sub>2</sub>/kWh)
        and population data. OWID aggregates from the Energy Institute, Ember, and the US Energy Information Administration.
        Coverage: 200+ countries, 1900&ndash;2024.
      </li>
      <li>
        <strong>International Energy Agency (IEA)</strong> &mdash; The Energy End-uses and Efficiency Indicators Database provides
        sector-level consumption breakdowns (by end-use and fuel product), per-capita CO<sub>2</sub> emissions, and total emissions
        by sector (industry, residential, transport, services).
        Coverage: 50+ countries, 2000&ndash;2023.
      </li>
      <li>
        <strong>EnergyCPI</strong> &mdash; A global database for energy consumer prices, providing quarterly Consumer Price Index
        values for energy sub-categories (electricity, gas, liquid fuels, solid fuels, district heating, transport fuels).
        Supplemented by World Bank electricity price data (US cents/kWh).
        Coverage: 102 countries, 1996&ndash;2024.
      </li>
    </ul>

    <h3>Data cleaning and imputation</h3>
    <p>
      Raw Eurostat data is distributed as TSV files with comma-separated dimension codes packed into the first column.
      These are parsed and pivoted from wide format (one column per year) to long format (one row per observation).
      Statistical flags appended to values (e.g. <code>p</code> for provisional, <code>e</code> for estimated, <code>b</code> for break in series)
      are stripped and the underlying numeric values retained.
      Missing value markers (<code>:</code> in Eurostat, <code>..</code> in IEA data) are converted to <code>null</code>.
    </p>
    <p>
      Country codes are normalized to ISO 3166-1 alpha-2 using a central mapping table.
      Eurostat uses non-standard codes for Greece (<code>EL</code> instead of <code>GR</code>) and
      the United Kingdom (<code>UK</code> instead of <code>GB</code>), which are corrected during processing.
      IEA data uses full country names, matched to ISO codes via fuzzy matching with the <code>pycountry</code> library.
    </p>
    <p>
      No imputation is applied &mdash; missing values remain as <code>null</code> in the final datasets
      and are handled at the visualization level. The only derived value is industry emissions per capita,
      which is calculated from total industry emissions divided by OWID population figures where both are available.
    </p>

    <h3>Data processing and analysis</h3>
    <p>
      The main dataset (<code>energy_mix.json</code>) is built in a multi-phase pipeline.
      First, over 140 SIEC fuel codes from Eurostat are mapped to five main energy categories:
      coal (solid fossil fuels), oil, gas, biofuels, and electricity.
      Nuclear fuels and renewable fuel codes are excluded from the dependency analysis.
    </p>
    <p>
      Trade data (31.8 million rows) is read in 500,000-row chunks for memory efficiency.
      Regional aggregates (EU27, EA20) and non-specific partners (TOTAL, THRD, NSP) are filtered out
      so that only bilateral country-to-country flows remain.
      Import and export volumes are aggregated by reporting country, year, energy type, and partner.
      Partner shares are then calculated as a percentage of total trade volume per energy type and ranked.
    </p>
    <p>
      Dependency metrics are sourced directly from Eurostat's published indicators:
      overall import dependency (ID) measures <code>(Imports &minus; Exports) / (Gross Inland Consumption + Bunkers)</code>,
      while third-country dependency (ID3CF) measures the share of imports originating from non-EU countries.
      Both are provided at the total and individual fuel level.
    </p>
    <p>
      OWID production and consumption data (in TWh) is merged into the Eurostat structure by matching
      Eurostat ISO-2 codes to OWID ISO-3 codes via the country code mastersheet.
      Sector consumption data from IEA is organized hierarchically: sector, end-use category, and fuel product (in PJ).
      Emissions data combines OWID carbon intensity with IEA per-sector emissions.
      Energy price indices are structured at quarterly granularity with annual electricity prices.
    </p>
    <p>
      All processing scripts include verification steps that spot-check sample countries
      and validate value ranges before writing output.
      Four JSON files are produced: <code>energy_mix.json</code> (trade, dependency, production/consumption),
      <code>energy_consumptions_by_sector.json</code> (sector breakdowns),
      <code>eco_data.json</code> (emissions and carbon intensity),
      and <code>energy_prices.json</code> (CPI indices and electricity prices).
    </p>

    <h3>Limitations</h3>
    <ul>
      <li>
        <strong>Geographic scope</strong> &mdash; Trade and dependency data covers 41 EU/EEA countries only.
        Global coverage (OWID, IEA) is available for production, consumption, and emissions metrics,
        but not for bilateral trade flows.
      </li>
      <li>
        <strong>Temporal coverage varies by sector</strong> &mdash; Household consumption data is available from 2010,
        industry from 2017, and services and transport only from 2020.
        Third-country dependency (ID3CF) is only available from 2010 onward.
      </li>
      <li>
        <strong>No electricity dependency rate</strong> &mdash; Eurostat does not publish an overall import dependency
        indicator for electricity. Cross-border electricity trade within the interconnected European grid
        is treated as internal balancing rather than external dependency.
        Only third-country electricity dependency is available.
      </li>
      <li>
        <strong>Non-comparable trade units</strong> &mdash; Different energy types use different units:
        thousand tonnes for coal, oil, and biofuels; terajoules for gas; gigawatt-hours for electricity.
        Aggregate partner rankings sum these numeric values across types,
        meaning gas (large TJ values) may dominate the overall ranking.
      </li>
      <li>
        <strong>Dependency edge cases</strong> &mdash; Dependency values can be negative (for net exporters)
        or exceed 100% (due to stock changes or re-exports). These are correct per Eurostat's formula
        and are not clamped.
      </li>
      <li>
        <strong>Missing countries</strong> &mdash; Kosovo (XK) has no official ISO code and is absent from OWID.
        Liechtenstein (LI) is also not covered by OWID. These countries may lack production, consumption,
        or emissions data.
      </li>
      <li>
        <strong>Price data is index-based</strong> &mdash; Energy price series are CPI indices (rebased, not absolute prices),
        suitable for tracking trends over time but not for comparing price levels across countries.
        The exception is electricity prices, reported in US cents/kWh.
      </li>
      <li>
        <strong>IEA data gaps</strong> &mdash; The energy efficiency indicator from Eurostat has approximately 88% missing values.
        IEA sector data coverage varies by country and may not be available for all 41 EU/EEA countries.
      </li>
    </ul>
  </section>
</template>
