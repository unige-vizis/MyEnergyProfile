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
        <!-- TODO - Mali -->
        <!-- Ideen:
          - allgemeines trade portrait eines westlichen landes 
          - Große Player in einzelnen resourcen
          -->
        <p>
          This section provides an overview of the availability of energy in your area over the past year. You can
          analyze grid reliability, outage frequency, and compare your data with regional availability trends.
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
