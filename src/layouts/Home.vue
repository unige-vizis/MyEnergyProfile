<script setup>
import Sidebar from '../components/Sidebar.vue';
import Footer from '../components/Footer.vue';
import Consumption from '../components/sections/Consumption.vue';
import SectorFuels from '../components/sections/SectorFuels.vue';
import Costs from '../components/sections/Costs.vue';
import TradingPartner from '../components/sections/TradingPartner.vue';
import Dependency from '../components/sections/Dependency.vue';
import FuelTypes from '../components/sections/FuelTypes.vue';
import ProductionConsumption from '../components/sections/ProductionConsumption.vue';
import Eco from '../components/sections/Eco.vue';
import ConfigHeader from '../components/ConfigHeader.vue';
import { ref } from 'vue'
import { useEnergyDataStore } from '@/stores/energyData'

const energyStore = useEnergyDataStore()

const sections = ref([
  { id: "fueltypes", name: "Types of Fuel", icon: "oil_barrel",},
  { id: "dependency", name: "Dependency on Imports", icon: "trending_up",},
  { id: "tradingpartner", name: "Trading Partners", icon: "cycle",},
  { id: "consumption", name: "Sectoral Energy Use", icon: "battery_android_frame_5", },
  { id: "sectorfuels", name: "Energy Sources", icon: "delivery_truck_bolt", },
  { id: "productionconsumption", name: "Production & Consumption", icon: "instant_mix", },
  { id: "costs", name: "Energy Prices", icon: "euro", },
  { id: "eco", name: "Carbon Footprint", icon: "energy_savings_leaf",},
]);
</script>

<template>
  <div id="app-container">
    <Sidebar :sections="sections"></Sidebar>
    <main>
      <ConfigHeader></ConfigHeader>
      <div class="main-content main-with-config">
        <Transition name="fade">
          <div v-if="energyStore.isYearChanging" class="year-loading-overlay">
            <div class="year-loading-spinner"></div>
          </div>
        </Transition>
        <FuelTypes></FuelTypes>
        <Dependency></Dependency>
        <TradingPartner></TradingPartner>
        <Consumption></Consumption>
        <SectorFuels></SectorFuels>
        <ProductionConsumption></ProductionConsumption>
        <Costs></Costs>
        <Eco></Eco>
      </div>
      <Footer></Footer>
    </main>
  </div>
</template>

<style scoped>
.main-content {
  position: relative;
}

.year-loading-overlay {
  position: fixed;
  top: 0;
  left: var(--sidebar-width, 200px);
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.5);
  z-index: 50;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
}

.year-loading-spinner {
  width: 36px;
  height: 36px;
  border: 3px solid rgba(0, 0, 0, 0.1);
  border-top-color: var(--accent-color, #333);
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.fade-enter-active { transition: opacity 0.1s ease; }
.fade-leave-active { transition: opacity 0.15s ease; }
.fade-enter-from,
.fade-leave-to { opacity: 0; }
</style>
