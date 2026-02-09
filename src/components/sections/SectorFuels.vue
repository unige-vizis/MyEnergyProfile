<script setup>
import { useEnergyDataStore } from '@/stores/energyData'
import { ref, computed } from 'vue'
import PieChart from '../charts/PieChart.vue'

const store = useEnergyDataStore()
const selectedSector = ref('Residential')
const hasData = computed(() => {
  return store.sunburstData.name?.length > 0 && store.pieChartData[0]
})
</script>

<template>
  <section id="sectorfuels" class="page-section">
    <div class="chart-header">
      <h2>What Energy Sources Do Different Sectors Rely On?</h2>
    </div>
    <div class="section-container">
      <div v-if="!hasData" class="no-data">
        <span>No consumption data available for this configuration.</span>
      </div>
      <div v-else-if="store.isLoading" class="loading">Loading energy data...</div>
      <div v-else-if="store.error" class="error">{{ store.error }}</div>
      <div v-else class="charts-container">
        <div class="interactive-graphic">
          <img
            src="../../assets/img/consumption_background.svg"
            alt="Energy Consumption Background"
            style="width: 100%; cursor: pointer;"
            @click="selectedSector = 'Residential'"
            class="bg-image"
          />
          <div class="interactive-image-container">
            <img
              src="../../assets/img/consumption_service.svg"
              alt="Energy Consumption Service"
              style="width: 20%; cursor: pointer;"
              @click="selectedSector = 'Service'"
              :class="{ active: selectedSector === 'Service' }"
              class="interactive-image svg-glow"
            />
            <img
              src="../../assets/img/consumption_residential.svg"
              alt="Energy Consumption Residential"
              style="width: 15%; cursor: pointer;"
              @click="selectedSector = 'Residential'"
              :class="{ active: selectedSector === 'Residential' }"
              class="interactive-image svg-glow"
            />
            <img
              src="../../assets/img/consumption_transport.svg"
              alt="Energy Consumption Transport"
              style="width: 20%; cursor: pointer;"
              @click="selectedSector = 'Transport'"
              :class="{ active: selectedSector === 'Transport' }"
              class="interactive-image svg-glow"
            />
            <img
              src="../../assets/img/consumption_industry.svg"
              alt="Energy Consumption Industry"
              style="width: 30%; cursor: pointer;"
              @click="selectedSector = 'Industry'"
              :class="{ active: selectedSector === 'Industry' }"
              class="interactive-image svg-glow"
            />
          </div>
        </div>
        <PieChart
          :data="store.pieChartData"
          :year="store.selectedYear"
          :country="store.selectedCountry"
          :selectedSector="selectedSector"
        />
      </div>
      <div class="text-container">
        <p>
          This visualization shows how different sectors rely on different types of energy sources. Although the exact
          shares change from country to country and over time, some broad patterns appear consistently across the
          dataset.
        </p>
        <p>
          <strong>Residential</strong> energy use is mixed. Households tend to combine several energy carriers, commonly
          electricity, gas, biofuels, or district heat, depending on climate conditions, building types, and heating
          technologies. In many countries electricity and gas form the core of household consumption.
        </p>
        <p>
          <strong>Transport</strong> relies primarily on oil‑based fuels. Across almost all countries and years, road,
          air, and freight transport are dominated by gasoline, diesel, jet fuel, and other oil products. Alternative
          fuels such as electricity or gas are present but remain small compared to oil.
        </p>
        <p>
          <strong>Services</strong> rely heavily on electricity. Hotels, offices, public buildings, and commercial
          activities typically use electricity as their main energy source, with gas or heat sometimes contributing
          depending on the country. Oil and coal appear only as small shares in most cases.
        </p>
        <p>
          <strong>Industry</strong> uses a varied mix. Manufacturing and industrial processes draw on electricity, gas,
          coal, bioenergy, and oil to different extents. This reflects the diverse technical needs of industrial
          production, from high‑temperature heat to mechanical power.
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
