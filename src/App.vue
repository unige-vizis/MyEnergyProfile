<script setup>
import Sidebar from './components/Sidebar.vue';
import Consumption from './components/sections/Consumption.vue';
import Global from './components/sections/Global.vue';
import Costs from './components/sections/Costs.vue';
import TradingPartner from './components/sections/TradingPartner.vue';
import Dependency from './components/sections/Dependency.vue';
import Household from './components/sections/Household.vue';
import ETransition from './components/sections/ETransition.vue';
import If from './components/sections/If.vue';
import ConfigHeader from './components/ConfigHeader.vue';
</script>

<template>
  <div id="app-container">
    <Sidebar></Sidebar>
    <div>
      <ConfigHeader></ConfigHeader>
      <main class="main-content">
        <Consumption></Consumption>
        <Global></Global>
        <Costs></Costs>
        <TradingPartner></TradingPartner>
        <Dependency></Dependency>
        <Household></Household>
        <ETransition></ETransition>
        <If></If>
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
