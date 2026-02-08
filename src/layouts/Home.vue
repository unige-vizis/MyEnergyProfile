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
