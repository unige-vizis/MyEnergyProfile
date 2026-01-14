<template>
  <div class="config-header">
    <h3>Configuriation</h3>
    <select>
      <option value="option1">Option 1</option>
      <option value="option2">Option 2</option>
      <option value="option3">Option 3</option>
    </select>
  </div>
</template>

<script setup></script>

<style scoped>
  .config-header {
  position: fixed;
  left: 250px;
  top: 0;
  width: 100%;
  padding: 2rem 5rem;
  background: linear-gradient(to right, #4c4c4c, #1a1a1a);
  color: white;
  box-shadow: 4px 0 12px rgba(0, 0, 0, 0.4);
  z-index: 100;
}
</style>
