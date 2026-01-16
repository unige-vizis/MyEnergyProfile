<template>
  <section id="mix" class="page-section">
    <h2>My energy mix</h2>
    <p>
      This section provides an overview of your energy mix over the past year. You can analyze your renewable and
      non-renewable energy sources, peak consumption periods, and compare your data with average household consumption.
    </p>

    <div class="mix-controls">
      <CountrySelector />
      <YearPicker
        v-model="selectedYear"
        :years="availableYears"
      />
    </div>

    <div v-if="store.isLoading" class="loading">Loading energy data...</div>
    <div v-else-if="store.error" class="error">{{ store.error }}</div>
    <div v-else-if="dependencyData" class="chart-section">
      <DependencyChart
        :dependencyData="dependencyData"
        :year="selectedYear"
      />
    </div>
  </section>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useEnergyDataStore } from '@/stores/energyData'
import CountrySelector from './CountrySelector.vue'
import DependencyChart from './DependencyChart.vue'
import YearPicker from './YearPicker.vue'

const store = useEnergyDataStore()

const selectedYear = ref(null)

const availableYears = computed(() => {
  if (!store.selectedCountry?.years) return []
  return Object.keys(store.selectedCountry.years)
    .map(Number)
    .sort((a, b) => b - a)
})

const dependencyData = computed(() => {
  if (!store.selectedCountry?.years || !selectedYear.value) return null
  const yearData = store.selectedCountry.years[selectedYear.value]
  return yearData?.dependency || null
})

watch(availableYears, (years) => {
  if (years.length > 0 && !years.includes(selectedYear.value)) {
    selectedYear.value = years[0]
  }
}, { immediate: true })

onMounted(() => {
  store.loadData()
})
</script>

<style scoped>
.mix-controls {
  display: flex;
  gap: 1rem;
  align-items: center;
  margin: 1.5rem 0;
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
