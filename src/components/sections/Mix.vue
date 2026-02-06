<template>
  <section id="mix" class="page-section">
    <h2>My energy mix</h2>

    <!-- Subsection: Where does my Energy Come from -->
    <div class="mix-subsection">
      <h3>Where does my Energy Come from</h3>
      <p>
        The stacked bar chart below shows how much of a country’s energy supply is produced domestically and how much is imported from abroad, broken down by energy source. Import dependency highlights the degree to which national energy systems rely on foreign suppliers and therefore reflects aspects of energy security, resilience, and exposure to geopolitical risks.
        By comparing energy sources, it becomes clear that some fuels are structurally dependent on imports, while others are more closely tied to domestic resources. The detailed descriptions of each energy source below provide additional context on their role, availability, and typical dependency patterns.
      </p>

      <div v-if="store.isLoading" class="loading">Loading energy data...</div>
      <div v-else-if="store.error" class="error">{{ store.error }}</div>
      <template v-else>
        <div v-if="store.dependencyData" class="chart-section">
          <DependencyChart :dependencyData="store.dependencyData" :year="store.selectedYear" />
        </div>

        <div class="chart-section">
          <TradingPartnersMap
            :tradeData="store.tradeData"
            :country="store.selectedCountry"
            :year="store.selectedYear"
          />
        </div>
      </template>
    </div>
  </section>
</template>

<script setup>
import { useEnergyDataStore } from '@/stores/energyData'
import DependencyChart from '../charts/DependencyChart.vue'
import TradingPartnersMap from '../charts/TradingPartnersMap.vue'

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
  color: black;
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
