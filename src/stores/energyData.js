import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useEnergyDataStore = defineStore('energyData', () => {
  const rawData = ref(null)
  const selectedCountryCode = ref('DE')
  const isLoading = ref(false)
  const error = ref(null)

  const countries = computed(() => {
    if (!rawData.value?.countries) return []
    return Object.entries(rawData.value.countries)
      .map(([code, data]) => ({
        code,
        name: data.name
      }))
      .sort((a, b) => a.name.localeCompare(b.name))
  })

  const selectedCountry = computed(() => {
    if (!rawData.value?.countries || !selectedCountryCode.value) return null
    const countryData = rawData.value.countries[selectedCountryCode.value]
    if (!countryData) return null
    return {
      code: selectedCountryCode.value,
      name: countryData.name,
      years: countryData.years
    }
  })

  const metadata = computed(() => rawData.value?.metadata || null)

  async function loadData() {
    if (rawData.value) return

    isLoading.value = true
    error.value = null

    try {
      const response = await fetch(`${import.meta.env.BASE_URL}data/energy_imports_exports_dependency.json`)
      const text = await response.text()
      // Handle NaN values in JSON (convert to null)
      const cleanedText = text.replace(/:\s*NaN/g, ': null')
      rawData.value = JSON.parse(cleanedText)
    } catch (e) {
      error.value = e.message
      console.error('Failed to load energy data:', e)
    } finally {
      isLoading.value = false
    }
  }

  function setSelectedCountry(code) {
    selectedCountryCode.value = code
  }

  return {
    rawData,
    selectedCountryCode,
    isLoading,
    error,
    countries,
    selectedCountry,
    metadata,
    loadData,
    setSelectedCountry
  }
})
