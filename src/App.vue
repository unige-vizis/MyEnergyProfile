<script setup>
import Sidebar from './components/Sidebar.vue';
</script>

<template>
  <div id="app-container">
    <Sidebar></Sidebar>
    <main class="main-content">
      <section id="consumption" class="page-section">
        <h2>consumption</h2>
      </section>
      <section id="costs" class="page-section">
        <h2>costs</h2>
      </section>
      <section id="availability" class="page-section">
        <h2>availability</h2>
        <p>Add your data sources content here...</p>
      </section>
      <section id="mix" class="page-section">
        <h2>mix</h2>
        <p>Add your contact content here...</p>
      </section>

      <!-- <Consumption></Consumption>
      <Costs></Costs>
      <Availability></Availability>
      <Mix></Mix>
      <Household></Household>
      <ETransition></ETransition>
      <If></If>
      <Global></Global> -->
    </main>
  </div>
</template>

<style scoped>
#app-container {
  display: flex;
  background-color: #f8f9fa;
}

.main-content {
  margin-left: 300px;
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
