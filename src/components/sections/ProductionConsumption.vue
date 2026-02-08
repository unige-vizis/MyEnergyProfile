<template>
  <section id="productionconsumption" class="page-section">
    <h2>Production &amp; Consumption by Resource Over Time</h2>
    <!-- Subsection: Production & Consumption by Resource -->
    <div>
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
.loading,
.error {
  padding: 2rem;
  text-align: center;
  color: var(--text-color-gray);
}

.error {
  color: var(--text-color-red);
}

.chart-section {
  margin-top: 1.5rem;
}
</style>
