<script setup>
import { useEnergyDataStore } from '@/stores/energyData'
import { ref, computed } from 'vue'
import SunburstChart from '../charts/SunburstChart.vue'

const store = useEnergyDataStore()
const selectedSector = ref('Residential')
const hasData = computed(() => {
  return store.sunburstData.name?.length > 0 && store.pieChartData[0]
})
</script>

<template>
  <section id="consumption" class="page-section">
    <div class="chart-header">
      <h2>How Different Sectors Use Energy?</h2>
    </div>
    <div class="section-container">
      <div v-if="!hasData" class="no-data">
        <span>No consumption data available for this configuration.</span>
      </div>
      <div v-else-if="store.isLoading" class="loading">Loading energy data...</div>
      <div v-else-if="store.error" class="error">{{ store.error }}</div>
      <div v-else class="charts-container">
        <SunburstChart :data="store.sunburstData" :year="store.selectedYear" :country="store.selectedCountry" />
      </div>
      <div class="text-container">
        <!-- TODO - Petula -->
        <p>
          Have you ever wondered what sectors consume the most energy in your country? Energy consumption differs across
          <strong>households, services, transport, and industry</strong> because each sector uses energy for
          fundamentally different purposes. Industry consumes the most energy due to energy-intensive production
          processes and high-temperature heat requirements. The transport sector is dominated by fossil fuels and
          internal combustion engines, which are inherently inefficient and driven by growing mobility demand. Household
          energy use is mainly shaped by space heating, building characteristics, and everyday behavior. The service
          sector consumes energy primarily for heating, lighting, cooling, and IT in large buildings with long operating
          hours. Overall, sectoral differences in energy consumption are driven more by structural and technical factors
          than by individual efficiency or waste. This interactive sunburst diagram shows how total energy consumption
          is distributed across the four major sectors and how it is further broken down into specific activities.
        </p>
      </div>
    </div>
  </section>
</template>

<style scoped>
.interactive-image {
  cursor: pointer;
  width: 20%;
  transform-origin: center bottom;
  transition: transform 0.2s ease;
}

.interactive-image.active {
  filter: drop-shadow(0 0 6px var(--secondary-color))
             drop-shadow(0 0 10px var(--secondary-color));
}

.interactive-image:hover,
.interactive-image.active {
  transform: scale(1.1);
}

.interactive-graphic {
  position: relative;
  width: 100%;
}

.bg-image {
  width: 100%;
  display: block;
}

.interactive-image-container {
  position: absolute;
  bottom: 0.5%;
  left: 0;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}

.svg-glow:not(.active) {
  filter: drop-shadow(0 0 1px var(--primary-color))
          drop-shadow(0 0 3px var(--primary-color))
          drop-shadow(0 0 5px var(--primary-color));
  animation: subtle-svg-pulse 2s ease-in-out infinite;
}

@keyframes subtle-svg-pulse {
  0%, 100% { filter: drop-shadow(0 0 2px var(--primary-color)); }
  50% { filter: drop-shadow(0 0 8px var(--primary-color))
             drop-shadow(0 0 12px var(--primary-color)); }
}
</style>
