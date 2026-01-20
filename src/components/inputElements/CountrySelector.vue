<template>
  <div class="country-selector">
    <button
      class="country-button"
      @click="toggleDropdown"
      :aria-expanded="isOpen"
    >
      <span class="country-flag">{{ getFlagEmoji(selectedCountryCode) }}</span>
      <span class="country-name">{{ selectedCountryName }}</span>
      <svg class="chevron" :class="{ open: isOpen }" width="12" height="12" viewBox="0 0 12 12">
        <path d="M3 4.5L6 7.5L9 4.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" fill="none"/>
      </svg>
    </button>

    <div v-if="isOpen" class="dropdown-overlay" @click="closeDropdown"></div>

    <div v-if="isOpen" class="dropdown-panel">
      <div class="search-box">
        <input
          ref="searchInput"
          v-model="searchQuery"
          type="text"
          placeholder="Search countries..."
          @keydown.escape="closeDropdown"
        />
      </div>
      <div class="country-grid">
        <button
          v-for="country in filteredCountries"
          :key="country.code"
          class="country-option"
          :class="{ selected: country.code === selectedCountryCode }"
          @click="selectCountry(country.code)"
        >
          <span class="option-flag">{{ getFlagEmoji(country.code) }}</span>
          <span class="option-code">{{ country.code }}</span>
          <span class="option-name">{{ country.name }}</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, watch } from 'vue'
import { useEnergyDataStore } from '@/stores/energyData'

const store = useEnergyDataStore()

const isOpen = ref(false)
const searchQuery = ref('')
const searchInput = ref(null)

const selectedCountryCode = computed(() => store.selectedCountryCode)
const selectedCountryName = computed(() => {
  const country = store.countries.find(c => c.code === store.selectedCountryCode)
  return country?.name || 'Select country'
})

const filteredCountries = computed(() => {
  if (!searchQuery.value) return store.countries
  const query = searchQuery.value.toLowerCase()
  return store.countries.filter(c =>
    c.name.toLowerCase().includes(query) ||
    c.code.toLowerCase().includes(query)
  )
})

function getFlagEmoji(countryCode) {
  // Handle special cases
  const codeMap = {
    'EL': 'GR', // Greece uses EL in Eurostat but GR for flag
    'UK': 'GB', // United Kingdom
    'XK': 'XK'  // Kosovo (no official emoji, will show letters)
  }
  const code = codeMap[countryCode] || countryCode

  if (code.length !== 2) return ''

  const codePoints = code
    .toUpperCase()
    .split('')
    .map(char => 127397 + char.charCodeAt(0))

  return String.fromCodePoint(...codePoints)
}

function toggleDropdown() {
  isOpen.value = !isOpen.value
  if (isOpen.value) {
    nextTick(() => {
      searchInput.value?.focus()
    })
  }
}

function closeDropdown() {
  isOpen.value = false
  searchQuery.value = ''
}

function selectCountry(code) {
  store.setSelectedCountry(code)
  closeDropdown()
}

watch(isOpen, (newVal) => {
  if (!newVal) {
    searchQuery.value = ''
  }
})
</script>

<style scoped>
.country-selector {
  position: relative;
  display: inline-block;
}

.country-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  background: white;
  border: 1px solid #d0d0d0;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s ease;
}

.country-button:hover {
  border-color: #999;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.country-flag {
  font-size: 1.1rem;
}

.country-name {
  color: #333;
  font-weight: 500;
}

.chevron {
  color: #666;
  transition: transform 0.2s ease;
}

.chevron.open {
  transform: rotate(180deg);
}

.dropdown-overlay {
  position: fixed;
  inset: 0;
  z-index: 99;
}

.dropdown-panel {
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  z-index: 100;
  background: white;
  border: 1px solid #d0d0d0;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
  width: 360px;
  max-height: 400px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.search-box {
  padding: 0.75rem;
  border-bottom: 1px solid #eee;
}

.search-box input {
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: 1px solid #d0d0d0;
  border-radius: 4px;
  font-size: 0.9rem;
  outline: none;
}

.search-box input:focus {
  border-color: #666;
}

.country-grid {
  overflow-y: auto;
  max-height: 320px;
}

.country-option {
  display: grid;
  grid-template-columns: 1.5rem 2.5rem 1fr;
  gap: 0.5rem;
  align-items: center;
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: none;
  background: transparent;
  cursor: pointer;
  text-align: left;
  font-size: 0.85rem;
  transition: background 0.15s ease;
}

.country-option:hover {
  background: #f5f5f5;
}

.country-option.selected {
  background: #e8f4fc;
}

.option-flag {
  font-size: 1rem;
}

.option-code {
  color: #666;
  font-weight: 500;
  font-family: monospace;
}

.option-name {
  color: #333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
