<script setup>
import Header from './components/Sidebar.vue'
</script>

<template>
  <div id="app-container">
    <Header></Header>
    <main class="main-content">
      <section id="features" class="page-section">
        <h2>Features</h2>
        <p>Add your features content here...</p>
      </section>
      <section id="about" class="page-section">
        <h2>About</h2>
        <p>Add your about content here...</p>
      </section>
      <section id="data" class="page-section">
        <h2>Data Sources</h2>
        <p>Add your data sources content here...</p>
      </section>
      <section id="contact" class="page-section">
        <h2>Contact</h2>
        <p>Add your contact content here...</p>
      </section>
    </main>
  </div>
</template>

<style scoped>
#app-container {
  display: flex;
  min-height: 100vh;
  background-color: #f8f9fa;
}

.main-content {
  margin-left: 200px;
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
