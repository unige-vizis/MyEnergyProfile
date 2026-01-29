import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useGlobalConfigStore = defineStore('globalConfig', () => {
  // Global year range configuration
  // This can be updated later to pull from multiple data sources
  const yearRange = ref({
    min: 1990,
    max: 2024
  })

  const minYear = computed(() => yearRange.value.min)
  const maxYear = computed(() => yearRange.value.max)

  // Generate array of years for dropdowns (newest first)
  const yearsDescending = computed(() => {
    const years = []
    for (let y = yearRange.value.max; y >= yearRange.value.min; y--) {
      years.push(y)
    }
    return years
  })

  // Generate array of years (oldest first)
  const yearsAscending = computed(() => {
    const years = []
    for (let y = yearRange.value.min; y <= yearRange.value.max; y++) {
      years.push(y)
    }
    return years
  })

  function setYearRange(min, max) {
    yearRange.value = { min, max }
  }

  return {
    yearRange,
    minYear,
    maxYear,
    yearsDescending,
    yearsAscending,
    setYearRange
  }
})
