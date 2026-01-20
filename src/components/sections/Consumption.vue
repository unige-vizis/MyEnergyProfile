<template>
  <section id="consumption" class="page-section">
    <h2>My energy consumption</h2>
    <p>
      This section provides an overview of your energy consumption patterns over the past year. You can analyze your
      monthly usage, peak consumption periods, and compare your data with average household consumption.
    </p>
    <div class="consumption-container">
      <div class="interactive-graphic">
        <div
          :class="{ active: selectedSector === 'Residential' }"
          @click="selectedSector = 'Residential'"
          class="interactive-icon"
        >
          <span style="font-size: 8rem;" class="material-symbols-outlined">home</span>
        </div>
        <div style="position: relative; margin-left: -1rem;">
          <div
            style="position: absolute; top: 2px; left: 20px; z-index: 10; rotate: 7deg;"
            class="interactive-icon"
            :class="{ active: selectedSector === 'Transport' }"
            @click="selectedSector = 'Transport'"
          >
            <span style="font-size: 5rem;" class="material-symbols-outlined">local_shipping</span>
          </div>
          <svg width="250" height="150" viewBox="0 0 250 150" xmlns="http://www.w3.org/2000/svg">
            <path d="M0 60 C40 40, 80 80, 250 60" fill="none" stroke="#000" stroke-width="4" stroke-linejoin="round" />
            <path
              d="M0 75 C40 55, 80 95, 250 75"
              fill="none"
              stroke="#000"
              stroke-width="4"
              stroke-dasharray="15,15"
              stroke-linecap="round"
            />
            <path d="M0 90 C40 70, 80 110, 250 90" fill="none" stroke="#000" stroke-width="4" stroke-linejoin="round" />
          </svg>
        </div>
        <div
          :class="{ active: selectedSector === 'Industry' }"
          @click="selectedSector = 'Industry'"
          class="interactive-icon"
        >
          <span style="font-size: 5rem;" class="material-symbols-outlined">factory</span>
        </div>
      </div>
      <Streamgraph :data="filteredData" />
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import Streamgraph from '../charts/Streamgraph.vue'

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

const filteredData = computed(() => {
  if (!consumptionsData.value || !selectedCountry.value || !selectedSector.value) return []
  const countryData = consumptionsData.value.countries[selectedCountry.value]

  if (!countryData || !countryData[selectedSector.value]) return []

  const sectorData = countryData[selectedSector.value]
  return Object.entries(sectorData).map(([endUse, data]) => ({
    name: endUse,
    years: data.years
  }))
})
</script>

<style scoped>
.consumption-container {
  display: flex;
  gap: 2rem;
  align-items: flex-start;
}

.interactive-graphic {
  display: flex;
  flex-wrap: wrap;
}

.interactive-icon {
  cursor: pointer;
}

.interactive-icon.active {
  color: #c59330;
}

.interactive-icon:hover {
  scale: 1.1;
  transition: all 0.2s ease;
}
</style>
