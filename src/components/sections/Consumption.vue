<template>
  <section id="consumption" class="page-section">
    <h2>My energy consumption</h2>
    <div class="section-container">
      <div class="charts-container">
        <PieChart :data="sectorTotalsData" :year="store.selectedYear" />
        <div class="interactive-graphic">
          <img
            src="../../assets/img/consumption_background.svg"
            alt="Energy Consumption Background"
            style="height: 200px; cursor: pointer;"
            @click="selectedSector = 'Residential'"
            :class="{ active: selectedSector === 'Residential' }"
          />
          <div class="interactive-image-container">
            <img
              src="../../assets/img/consumption_service.svg"
              alt="Energy Consumption Service"
              style="height: 140px; cursor: pointer;"
              @click="selectedSector = 'Service'"
              :class="{ active: selectedSector === 'Service' }"
              class="interactive-image svg-glow"
            />
            <img
              src="../../assets/img/consumption_residential.svg"
              alt="Energy Consumption Residential"
              style="height: 100px; cursor: pointer;"
              @click="selectedSector = 'Residential'"
              :class="{ active: selectedSector === 'Residential' }"
              class="interactive-image svg-glow"
            />
            <img
              src="../../assets/img/consumption_transport.svg"
              alt="Energy Consumption Transport"
              style="height: 60px; cursor: pointer;"
              @click="selectedSector = 'Transport'"
              :class="{ active: selectedSector === 'Transport' }"
              class="interactive-image svg-glow"
            />
            <img
              src="../../assets/img/consumption_industry.svg"
              alt="Energy Consumption Industry"
              style="height: 140px; cursor: pointer;"
              @click="selectedSector = 'Industry'"
              :class="{ active: selectedSector === 'Industry' }"
              class="interactive-image svg-glow"
            />
          </div>
        </div>
        <SunburstChart :data="filteredData" :year="store.selectedYear" />
      </div>
      <div class="text-container">
        <p>
          This section provides an overview of your energy consumption patterns over the past year. You can analyze your
          monthly usage, peak consumption periods, and compare your data with average household consumption.
        </p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { useEnergyDataStore } from '@/stores/energyData'
import { ref, computed, onMounted } from 'vue'
import SunburstChart from '../charts/SunburstChart.vue'
import PieChart from '../charts/PieChart.vue'

const store = useEnergyDataStore()

const selectedSector = ref('Residential')
const consumptionsData = ref(null)
const selectedCountry = ref('Italy') // Default country

onMounted(async () => {
  try {
    const response = await fetch(`${import.meta.env.BASE_URL}data/energy_consumptions_by_sector.json`)
    const text = await response.text()
    const cleanedText = text.replace(/:\s*NaN/g, ': null')
    consumptionsData.value = JSON.parse(cleanedText)
  } catch (e) {
    console.error('Failed to load consumptions data:', e)
  }
})

const sectorTotalsData = computed(() => {
  if (!consumptionsData.value || !selectedCountry.value || !store.selectedYear) return []

  const countryData = consumptionsData.value.countries[selectedCountry.value]
  if (!countryData) return []

  const sectors = ['Industry', 'Residential', 'Transport', 'Service']
  const children = sectors.map(sector => {
    const sectorData = countryData[sector]
    if (!sectorData) return null

    const yearData = sectorData[store.selectedYear]
    if (!yearData) return null

    // Sum all end uses for this sector
    let total = 0
    Object.values(yearData).forEach(endUseData => {
      const products = endUseData.products || {}
      total += products['Total final use (PJ)'] || 0
    })

    return {
      name: sector,
      value: total
    }
  }).filter(d => d && d.value > 0)

  return {
    name: 'Sectors',
    children: children
  }
})

const filteredData = computed(() => {
  if (!consumptionsData.value || !selectedCountry.value || !selectedSector.value || !store.selectedYear) return {}

  const countryData = consumptionsData.value.countries[selectedCountry.value]
  if (!countryData || !countryData[selectedSector.value]) return {}

  const sectorData = countryData[selectedSector.value]
  const yearData = sectorData[store.selectedYear]
  if (!yearData) return {}

  // Transform data for sunburst chart
  const children = Object.entries(yearData).map(([endUse, endUseData]) => {
    const products = endUseData.products || {}
    const productChildren = Object.entries(products)
      .filter(([key, value]) => key !== 'Total final use (PJ)' && value !== null && value !== 0)
      .map(([product, value]) => ({
        name: product.replace(' (PJ)', ''),
        value: value
      }))

    return {
      name: endUse,
      children: productChildren.length > 0 ? productChildren : [{ name: 'Total', value: products['Total final use (PJ)'] || 0 }]
    }
  })

  return {
    name: selectedSector.value,
    children: children.filter(child => child.children && child.children.length > 0)
  }
})
</script>

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
  margin-top: -143px;
  width: 600px;
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}
</style>
