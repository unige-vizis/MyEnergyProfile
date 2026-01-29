import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useEnergyDataStore = defineStore('energyData', () => {
  const rawData = ref(null)
  const selectedCountryCode = ref('IT')
  const selectedYear = ref(2023)
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

  // Available years for the selected country (newest first)
  const availableYears = computed(() => {
    if (!selectedCountry.value?.years) return []
    return Object.keys(selectedCountry.value.years)
      .map(Number)
      .sort((a, b) => b - a)
  })

  // Dependency data for the selected country and year
  const dependencyData = computed(() => {
    if (!selectedCountry.value?.years || !selectedYear.value) return null
    const yearData = selectedCountry.value.years[selectedYear.value]
    return yearData?.dependency || null
  })

  // Trade data (imports/exports with partners) for the selected country and year
  const tradeData = computed(() => {
    if (!selectedCountry.value?.years || !selectedYear.value) return null
    const yearData = selectedCountry.value.years[selectedYear.value]
    if (!yearData) return null
    return {
      imports: yearData.imports || null,
      exports: yearData.exports || null
    }
  })

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

  function setSelectedYear(year) {
    selectedYear.value = year
  }

  return {
    rawData,
    selectedCountryCode,
    selectedYear,
    isLoading,
    error,
    countries,
    selectedCountry,
    metadata,
    availableYears,
    dependencyData,
    tradeData,
    loadData,
    setSelectedCountry,
    setSelectedYear
  }
})
