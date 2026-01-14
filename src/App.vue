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

<style scoped>
#app-container {
  display: flex;
  background-color: #f8f9fa;
}

.main-content {
  margin-left: 300px;
  margin-top: 150px;
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
}

.page-section {
  min-height: 80vh;
  padding: 2rem;
  background-color: white;
  margin-bottom: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  scroll-margin-top: 2rem;
  border-top: 3px solid #e0e0e0;
  border-bottom: 3px solid #e0e0e0;
}

.page-section h2 {
  font-size: 2.5rem;
  color: #1a1a1a;
  margin-top: 0;
}

.page-section p {
  font-size: 1.1rem;
  color: #666;
  line-height: 1.6;
}
</style>
