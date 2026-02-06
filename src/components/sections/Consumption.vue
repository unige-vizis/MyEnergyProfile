<script setup>
import { useEnergyDataStore } from '@/stores/energyData'
import { ref, computed } from 'vue'
import SunburstChart from '../charts/SunburstChart.vue'
import PieChart from '../charts/PieChart.vue'

const store = useEnergyDataStore()
const selectedSector = ref('Residential')
const hasData = computed(() => {
  return store.sunburstData.name?.length > 0 && store.pieChartData[0]
})
</script>

<template>
  <section id="consumption" class="page-section">
    <h2>My energy consumption</h2>
    <div class="section-container">
      <div v-if="!hasData" class="no-data">
        <span>No consumption data available for this configuration.</span>
      </div>
      <div v-else-if="store.isLoading" class="loading">Loading energy data...</div>
      <div v-else-if="store.error" class="error">{{ store.error }}</div>
      <div v-else class="charts-container">
        <SunburstChart :data="store.sunburstData" :year="store.selectedYear" :country="store.selectedCountry" />
        <div class="interactive-graphic">
          <img
            src="../../assets/img/consumption_background.svg"
            alt="Energy Consumption Background"
            style="width: 100%; cursor: pointer;"
            @click="selectedSector = 'Residential'"
            :class="{ active: selectedSector === 'Residential' }"
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
      <div class="text-container1">
        <p>
           This interactive sunburst diagram shows how total energy consumption is distributed across the four major sectors
           and how it is further broken down into specific activities.<br><br>

           A high share in <strong>residential</strong> energy use often reflects heating needs, building efficiency, and household size, while
           a dominant transport sector can indicate high mobility demand or car-dependent infrastructures.<br>
           Elevated consumption in <strong>industry</strong> typically points to an energy-intensive economic structure, whereas the service
           sector is often associated with electricity use for buildings, lighting, and digital services.<br><br>

           High consumption values should be interpreted in context: differences between countries and years are often driven
           by climate, infrastructure, economic activity, and access to energy services rather than individual behavior alone.<br><br>
        </p>
      </div>
      <div class="text-container2">
      <p>
      The visualization below shows which <strong>energy sources</strong> are most commonly used in each sector.<br><br>
      Different sectors rely on distinct energy carriers depending on their technical requirements: transport tends to
      depend on oil-based fuels, while residential and service sectors use a higher share of electricity and heat.
      </p>
      </div>
    </div>
  </section>
</template>

<style scoped>
.interactive-image {
  cursor: pointer;
}

.interactive-image.active {
  filter: drop-shadow(0 0 6px #ab61ff99)
             drop-shadow(0 0 10px #ab61ff99);
}

.interactive-image:hover {
  scale: 1.1;
  transition: all 0.2s ease;
}

.svg-glow:not(.active) {
  filter: drop-shadow(0 0 3px #619dff99)
          drop-shadow(0 0 6px #619dff99)
          drop-shadow(0 0 12px #619dff99);
  animation: subtle-svg-pulse 2s ease-in-out infinite;
}

@keyframes subtle-svg-pulse {
  0%, 100% { filter: drop-shadow(0 0 2px #619dff99); }
  50% { filter: drop-shadow(0 0 6px #619dff99)
             drop-shadow(0 0 10px #619dff99); }
}

.interactive-image-container {
  margin-top: -133px;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}

.section-container {
  display: grid;
  grid-template-columns: 2fr 1fr;
  grid-template-areas:
    "charts text1"
    "charts text2";
  column-gap: 0.75rem; /* vorher z. B. 2rem */
  row-gap: 2rem;
  align-items: start;
}


.charts-container {
  grid-area: charts;
}

.text-container1 {
  grid-area: text1;
  max-width: 60ch;
}

.text-container2 {
  grid-area: text2;
  max-width: 60ch;
}

.text-container1,
.text-container2 {
  margin-left: -0.2rem;
}


</style>
