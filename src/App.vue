<script setup>
import Sidebar from './components/Sidebar.vue';
import Consumption from './components/sections/Consumption.vue';
import Costs from './components/sections/Costs.vue';
import TradingPartner from './components/sections/TradingPartner.vue';
import Dependency from './components/sections/Dependency.vue';
import ProductionConsumption from './components/sections/ProductionConsumption.vue';
import ETransition from './components/sections/ETransition.vue';
import ConfigHeader from './components/ConfigHeader.vue';
</script>

<template>
  <div id="app-container">
    <Sidebar></Sidebar>
    <main>
      <ConfigHeader></ConfigHeader>
      <div class="main-content">
        <Consumption></Consumption>
        <ProductionConsumption></ProductionConsumption>
        <Costs></Costs>
        <TradingPartner></TradingPartner>
        <Dependency></Dependency>
        <ETransition></ETransition>
      </div>
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
        </div>
        <div class="footer-right">
          <span class="footer-title">VIZIS</span>
        </div>
      </footer>
    </main>
  </div>
</template>
