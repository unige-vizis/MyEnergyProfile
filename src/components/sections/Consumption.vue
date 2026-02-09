<script setup>
import { useEnergyDataStore } from '@/stores/energyData'
import { ref, computed } from 'vue'
import SunburstChart from '../charts/SunburstChart.vue'

const store = useEnergyDataStore()
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
        <p>
          Have you ever wondered which sectors actually consume the most energy across countries? Energy use varies
          greatly between <strong>households, services, transport, and industry</strong>. We often assume industry
          dominates because energy-intensive production processes requires large amounts of heat and power. But as you
          can see with this sunburst chart, many countries consume nearly as much or sometimes more energy in the
          transport and residential sectors as in industry.
        </p>
        <p>
          But still the largest energy use by sector comes mostly from industry. The biggest industrial slice is often
          Manufacturing, which combines food production, textiles, machinery, electronics, and more.
        </p>
        <p>
          Transport accounts only slightly behind industry. It is dominated by cars and trucks, which is always the
          largest share of transport demand.
        </p>
        <p>
          Within households, space heating is almost always the dominant end‑use. Kosovo and Estonia appears with
          unusual high residential energy use not because households consume an unusually large amount of energy, but
          because its transport and industrial energy use are very small.
        </p>
        <p>
          Most countries have relatively low energy demand in the service sector, but some service-intensive economies
          such as Malta have a high share of energy demand in the service sector due to their tourism-driven economy.
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
