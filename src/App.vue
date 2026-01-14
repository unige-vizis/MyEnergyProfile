<script setup>
import Sidebar from './components/Sidebar.vue';
import Consumption from './components/Consumption.vue';
import Costs from './components/Costs.vue';
import Availability from './components/Availability.vue';
import Mix from './components/Mix.vue';
import Household from './components/Household.vue';
import ETransition from './components/ETransition.vue';
import If from './components/If.vue';
import Global from './components/Global.vue';
import ConfigHeader from './components/ConfigHeader.vue';
</script>

<template>
  <div id="app-container">
    <Sidebar></Sidebar>
    <div>
      <ConfigHeader></ConfigHeader>
      <main class="main-content">
        <Consumption></Consumption>
        <Costs></Costs>
        <Availability></Availability>
        <Mix></Mix>
        <Household></Household>
        <ETransition></ETransition>
        <If></If>
        <Global></Global>
      </main>
    </div>
  </div>
</template>
