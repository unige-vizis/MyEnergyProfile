<template>
  <section id="tradingpartner" class="page-section">
    <div class="chart-header">
      <h2>The Trading Partners</h2>
      <p class="chart-subtitle">Import and export partners by energy type</p>
    </div>
    <div class="section-container">
      <div v-if="store.isLoading" class="loading">Loading energy data...</div>
      <div v-else-if="store.error" class="error">{{ store.error }}</div>
      <div class="charts-container" v-else>
        <TradingPartnersMap :tradeData="store.tradeData" :country="store.selectedCountry" :year="store.selectedYear" />
      </div>
      <div class="text-container">
        <p>
          This section provides an overview of the availability of energy in your area over the past year. You can
          analyze grid reliability, outage frequency, and compare your data with regional availability trends.
        </p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { useEnergyDataStore } from '@/stores/energyData'
import TradingPartnersMap from '../charts/TradingPartnersMap.vue'

const store = useEnergyDataStore()
</script>
