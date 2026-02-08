<template>
  <section id="costs" class="page-section">
    <div class="chart-header">
      <h2>Evolution of Energy and Electricity Prices</h2>
    </div>
    <div class="section-container">
      <div v-if="store.isLoading" class="loading">Loading energy data...</div>
      <div v-else-if="store.error" class="error">{{ store.error }}</div>

      <template v-else class="charts-container">
        <div v-if="!store.pricesLoaded" class="no-data">Price data not available for this country.</div>

        <div v-else class="charts-container">
          <PricesFocusContext
            :data="store.electricitySeries"
            :focusYear="store.selectedYear"
            :view="view"
            activeSeries="energy"
            @update:focusYear="onFocusYear"
          />
          <PricesFocusContext
            :data="store.electricitySeries"
            :focusYear="store.selectedYear"
            :view="view"
            activeSeries="electricity"
            @update:focusYear="onFocusYear"
          />
          <div class="chart-footer">
            <small
              >Source: IMF/Eurostat <code>energycpiq.csv</code>. Columns: <code>country</code>, <code>year</code>,
              <code>quarter</code>, CPI series <code>CPI0450</code> (Electricity, gas &amp; fuels),
              <code>CPI0451</code> (Electricity), <code>CPI0452</code> (Gas), <code>CPI0453</code> (Liquid fuels),
              <code>CPI0454</code> (Solid fuels), <code>CPI0722</code> (Transport fuels). World Bank
              <code>Electric-Prices-by-Country.csv</code>. Columns: <code>Country Name</code>, <code>Time</code>,
              electricity price (US cents/kWh). Missing years are shown explicitly.</small
            >
          </div>
        </div>
      </template>
      <p class="text-container">
        <!-- TODO - Mali -->
        How have energy prices changed over time? The Energy Consumer Price Index (CPI) shows how the cost of energy for
        households evolves across years, reflecting broader economic and market conditions. Electricity prices are
        influenced by fuel costs, energy mix, infrastructure, and regulation.
      </p>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { useEnergyDataStore } from '@/stores/energyData'
import PricesFocusContext from '../charts/PricesFocusContext.vue'

const store = useEnergyDataStore()
const view = ref('annual')

function onFocusYear(year) {
  if (!year) return
  store.setSelectedYear(Number(year))
}
</script>

<style scoped>
.chart-topline {
  display:flex;
  justify-content:space-between;
  align-items:center;
  gap:1rem
}

.kpi {
  display:flex;
  flex-direction:column
}

.kpi-value {
  font-size:1.5rem;
  font-weight:700
}

.kpi-sub {
  color: var(--text-color-gray);
}

.chart-footer {
  margin-top:0.5rem;
  color: var(--text-color-gray);
}

.no-data {
  padding:1.25rem;
  color: var(--text-color-gray);
}
</style>
