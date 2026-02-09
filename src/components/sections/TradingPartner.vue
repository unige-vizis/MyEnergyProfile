<template>
  <section id="tradingpartner" class="page-section">
    <div class="chart-header">
      <h2>The Trading Partners</h2>
    </div>
    <div class="section-container">
      <div v-if="store.isLoading" class="loading">Loading energy data...</div>
      <div v-else-if="store.error" class="error">{{ store.error }}</div>
      <div class="charts-container" v-else>
        <TradingPartnersMap :tradeData="store.tradeData" :country="store.selectedCountry" :year="store.selectedYear" />
      </div>
      <div class="text-container">
        <p>
        Now that we understand how dependent countries are on
        energy imports, the next step is to examine where this
        energy originates.
        <br><br>
        Despite their economic strength, many Western countries
        consume far more energy than they can produce themselves.
        <br>
        These energy dependencies arise from the uneven global
        distribution of resources.
        <br>
        Most Western countries rely heavily on imports of fossil
        energy sources such as oil, gas, and coal from a small
        number of key suppliers, including Russia, the United
        States, Saudi Arabia, and Australia.
        <br>
        Norway stands out as an exception, exporting significantly
        more oil and natural gas than it imports.
        <br><br>
        In contrast, Germany and Italy import nearly all of their
        natural gas from a limited set of suppliers — a pattern
        that can be observed across many Western countries.
        <br>
        Electricity trade, however, is mainly regional.
        <br>
        Strong exchange between neighbouring Central European
        countries is visible, with France playing a key role as
        one of the most important electricity exporters due to its
        large nuclear power capacity.
        </p>
      </div>
    </div>
    <div class="chart-meta">
      <div class="meta-section">
        <span class="meta-label">Source</span>
        <ul class="meta-list">
          <li>
            Eurostat
            <a href="https://ec.europa.eu/eurostat/web/energy/database" target="_blank" rel="noopener"
              >Energy Database</a
            >
            (European Commission)
          </li>
          <li>Tables <code>nrg_ti_*</code> (imports) and <code>nrg_te_*</code> (exports) for sff, oil, gas, bio, eh</li>
          <li>Derived: <code>share_pct</code> = partner value ÷ total × 100</li>
        </ul>
      </div>
      <div class="meta-section">
        <span class="meta-label">Data Hints</span>
        <ul class="meta-list">
          <li>
            EU-reported data only; non-EU partner volumes data may be incomplete or reflect only the EU perspective of
            the trade relationship.
          </li>
          <li>Regional aggregates (e.g., "Other Asian countries") excluded from map arrows but included in totals.</li>
        </ul>
      </div>
    </div>
  </section>
</template>

<script setup>
import { useEnergyDataStore } from '@/stores/energyData'
import TradingPartnersMap from '../charts/TradingPartnersMap.vue'

const store = useEnergyDataStore()
</script>
