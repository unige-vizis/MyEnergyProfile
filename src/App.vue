<script setup>
import Sidebar from './components/Sidebar.vue';
import Consumption from './components/Consumption.vue';
import Global from './components/Global.vue';
import Costs from './components/Costs.vue';
import Availability from './components/Availability.vue';
import Mix from './components/Mix.vue';
import Household from './components/Household.vue';
import ETransition from './components/ETransition.vue';
import If from './components/If.vue';
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


