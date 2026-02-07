<template>
  <section id="productionconsumption" class="page-section">
    <h2>Production &amp; Consumption by Resource Over Time</h2>
    <p class="text-left">
      Energy systems change over time in response to economic growth, technological progress, and policy decisions.
      This visualization shows how energy production and consumption evolve across different energy sources, such as
      coal, oil, gas, biofuels, and electricity.<br>
      Comparing production and consumption reveals structural patterns: some energy sources are largely produced
      domestically, while others depend more strongly on imports or are gradually phased out. Rising or declining trends
      often reflect broader shifts in energy systems rather than short-term behavior.<br>
      These developments are shaped by resource availability, infrastructure, and long-term energy strategies,
      offering insight into how national energy systems adapt and where transition dynamics become visible.
    </p>

    <!-- Subsection: Production & Consumption by Resource -->
    <div class="mix-subsection">
      <div v-if="store.isLoading" class="loading">Loading energy data...</div>
      <div v-else-if="store.error" class="error">{{ store.error }}</div>
      <div v-else class="chart-section">
        <SmallMultiplesChart
          :productionConsumptionData="store.productionConsumptionData"
          :countryYears="store.selectedCountry?.years"
          :selectedYear="store.selectedYear"
          :countryName="store.selectedCountry?.name || ''"
        />
      </div>
    </div>
  </section>
</template>

<script setup>
import { useEnergyDataStore } from '@/stores/energyData'
import SmallMultiplesChart from '../charts/SmallMultiplesChart.vue'

const store = useEnergyDataStore()
</script>

<style scoped>
.mix-subsection {
  margin-bottom: 3rem;
}

.mix-subsection:last-child {
  margin-bottom: 0;
}

.mix-subsection h3 {
  font-size: 1.4rem;
  margin-bottom: 0.75rem;
  color: #2c3e50;
}

.mix-subsection > p {
  color: #666;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.loading,
.error {
  padding: 2rem;
  text-align: center;
  color: #666;
}

.error {
  color: #c44536;
}

.chart-section {
  margin-top: 1.5rem;
}
</style>
