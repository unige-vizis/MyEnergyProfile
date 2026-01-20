<script setup>
import Sidebar from './components/Sidebar.vue';
import Consumption from './components/sections/Consumption.vue';
import Global from './components/sections/Global.vue';
import Costs from './components/sections/Costs.vue';
import Availability from './components/sections/Availability.vue';
import Mix from './components/sections/Mix.vue';
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
        <Availability></Availability>
        <Mix></Mix>
        <Household></Household>
        <ETransition></ETransition>
        <If></If>
      </main>
    </div>
  </div>
</template>
