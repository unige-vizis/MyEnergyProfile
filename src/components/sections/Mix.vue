<template>
  <section id="mix" class="page-section">
    <h2>My energy mix</h2>

    <!-- Subsection: Where does my Energy Come from -->
    <div class="mix-subsection">
      <h3>Where does my Energy Come from</h3>
      <p>
        See how much of your country's energy is imported versus produced domestically. Import dependency shows what
        share of each fuel type comes from abroad, helping you understand your nation's energy security and reliance on
        foreign sources.
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

    <!-- Subsection: Production & Consumption by Resource -->
    <div class="mix-subsection">
      <h3>Production &amp; Consumption by Resource Over Time</h3>
      

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
import DependencyChart from '../charts/DependencyChart.vue'
import TradingPartnersMap from '../charts/TradingPartnersMap.vue'
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
