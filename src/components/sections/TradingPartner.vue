<template>
  <section id="tradingpartner" class="page-section">
    <div class="chart-header">
      <h2>The Trading Partners</h2>
      <p>Import and export partners by energy type</p>
    </div>
    <div class="section-container">
      <div v-if="store.isLoading" class="loading">Loading energy data...</div>
      <div v-else-if="store.error" class="error">{{ store.error }}</div>
      <div class="charts-container" v-else>
        <TradingPartnersMap :tradeData="store.tradeData" :country="store.selectedCountry" :year="store.selectedYear" />
      </div>
      <div class="text-container">
        <p>
        Which countries supply and receive energy, and how does this differ by energy type?<br>
        This section shows the main import and export partners for different energy carriers such as coal, oil, gas, biofuels, and electricity.<br>
        <br>
        Trade patterns reflect resource availability, geographic proximity, and long-term infrastructure connections.<br>
        High import shares often indicate structural dependency rather than short-term market decisions, while export flows highlight a country’s role within regional and global energy networks.
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
