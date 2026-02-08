<script setup>
import Sidebar from '../components/Sidebar.vue';
import Consumption from '../components/sections/Consumption.vue';
import Costs from '../components/sections/Costs.vue';
import TradingPartner from '../components/sections/TradingPartner.vue';
import Dependency from '../components/sections/Dependency.vue';
import ProductionConsumption from '../components/sections/ProductionConsumption.vue';
import Eco from '../components/sections/Eco.vue';
import ConfigHeader from '../components/ConfigHeader.vue';

const sections = ref([
  { id: "consumption", name: "My energy consumption", icon: "battery_android_frame_5", },
  { id: "productionconsumption", name: "Production & Consumption", icon: "instant_mix", },
  { id: "costs", name: "Energy costs", icon: "euro", },
  { id: "tradingpartner", name: "The Trading Partners", icon: "cycle",},
  { id: "dependency", name: "Dependency on imports", icon: "trending_up",},
  { id: "eco", name: "Ecological footprint", icon: "energy_savings_leaf",},
]);
</script>

<template>
  <div id="app-container">
    <Sidebar :sections="sections"></Sidebar> 
    <div>
      <ConfigHeader></ConfigHeader>
      <main class="main-content">
        <Consumption></Consumption>
        <ProductionConsumption></ProductionConsumption>
        <Costs></Costs>
        <TradingPartner></TradingPartner>
        <Dependency></Dependency>
        <Eco></Eco>
      </main>
      <footer class="site-footer">
        <div class="footer-names">
          <div class="name-with-tooltip">
            <span class="footer-name">Matteo Gläser</span>
            <div class="tooltip">Data research, development & data set management</div>
          </div>

          <div class="name-with-tooltip">
            <span class="footer-name">Petula Arnold</span>
            <div class="tooltip">Concept, statistics & content structure</div>
          </div>

          <div class="name-with-tooltip">
            <span class="footer-name">Maleah Leonie Kögler</span>
            <div class="tooltip">Design, storytelling & content structure</div>
          </div>

          <div class="name-with-tooltip">
            <span class="footer-name">Methodology</span>
            <div class="tooltip">Learn more about My Energy Profile</div>
          </div>
        </div>
        <div class="footer-right">
          <span class="footer-title">VIZIS</span>
        </div>
      </footer>
    </div>
  </div>
</template>
