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
      <div class="text-container">
        <p>
          The sunburst diagram on the left shows how energy consumption<br />
          is distributed across sectors and activities over the past year.<br />
          It shows that the majority of the energy is beeing used for Space<br />
          Heating and Cars. Within the transport sector, cars account for 51%<br />
          of total energy use, reflecting their widespread daily use. Air travel,<br />
          while highly energy-intensive per trip, represents only 4% of<br />
          total transport energy consumption.
          <br />
          <br />
          <br />
          This visualization shows how different energy sources are used across<br />
          sectors. It highlights that sectors such as transport and industry still<br />
          rely heavily on fossil fuels, while electricity and renewable sources play<br />
          a larger role in residential and service sectors. These structural differences<br />
          strongly influence how easily each sector can transition to low-carbon energy systems.
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
</style>
