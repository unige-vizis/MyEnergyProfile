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
        </div>
      </template>
      <p class="text-container">
        Was energy always this expensive? The line charts show how the Energy Consumer Price Index (CPI) has evolved
        over time, reflecting broader economic developments and changing market conditions. Sharp increases in household
        energy prices influence production decisions, consumption behaviour, and public perception. As prices rise,
        energy becomes more visible in everyday life, as both households and industries directly feel the economic
        impact. By exploring the data, it becomes clear that Germany, a country highly dependent on major energy
        suppliers, has experienced some of the strongest increases in energy prices in recent years.
      </p>
    </div>
    <div class="chart-meta">
      <div class="meta-section">
        <span class="meta-label">Source</span>
        <ul class="meta-list">
          <li>
            <strong>EnergyCPI</strong>
            <a href="https://github.com/MilesIParker/EnergyCPI" target="_blank" rel="noopener">
              Global Energy Consumer Price Index
            </a>
            (IMF/Eurostat). Series: <code>CPI0450</code> (Electricity, gas &amp; fuels).
          </li>
          <li>
            <strong>World Bank</strong>
            <a href="https://databank.worldbank.org/embed/Electric-Prices-by-Country/id/7b12e700" target="_blank" rel="noopener">
              Electric Prices by Country
            </a>
            . Electricity price (US cents/kWh).
          </li>
        </ul>
      </div>
      <div class="meta-section">
        <span class="meta-label">Data Hints</span>
        <ul class="meta-list">
          <li>World Bank electricity prices are only available for 2014 to 2019.</li>
        </ul>
      </div>
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

.no-data {
  padding:1.25rem;
  color: var(--text-color-gray);
}
</style>
