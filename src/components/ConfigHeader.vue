<script setup>
import AppInput from './AppInput.vue';
import AppSelect from './AppSelect.vue';
import { ref } from 'vue';

const country = ref('GE');
const countryOptions =
  [
        { value: 'GE', label: 'Germany' },
        { value: 'IT', label: 'Italy' },
        { value: 'FR', label: 'France' },
        { value: 'ES', label: 'Spain' },
        { value: 'PL', label: 'Poland' },
        { value: 'RO', label: 'Romania' },
        { value: 'NL', label: 'Netherlands' },
        { value: 'BE', label: 'Belgium' },
        { value: 'CZ', label: 'Czechia' },
        { value: 'PT', label: 'Portugal' },
        { value: 'HU', label: 'Hungary' },
        { value: 'SE', label: 'Sweden' },
        { value: 'AT', label: 'Austria' },
        { value: 'CH', label: 'Switzerland' },
        { value: 'BG', label: 'Bulgaria' },
        { value: 'DK', label: 'Denmark' },
        { value: 'FI', label: 'Finland' },
        { value: 'SK', label: 'Slovakia' },
        { value: 'IE', label: 'Ireland' },
        { value: 'HR', label: 'Croatia' },
        { value: 'LT', label: 'Lithuania' },
        { value: 'SI', label: 'Slovenia' },
        { value: 'LV', label: 'Latvia' },
        { value: 'EE', label: 'Estonia' },
        { value: 'CY', label: 'Cyprus' },
        { value: 'LU', label: 'Luxembourg' },
        { value: 'MT', label: 'Malta' },
        { value: 'GR', label: 'Greece' },
        { value: 'IS', label: 'Iceland' },
        { value: 'NO', label: 'Norway' },
        { value: 'AL', label: 'Albania' },
        { value: 'BA', label: 'Bosnia and Herzegovina' },
        { value: 'RS', label: 'Serbia' },
        { value: 'UA', label: 'Ukraine' },
        { value: 'RU', label: 'Russia' },
        { value: 'AM', label: 'Armenia' },
        { value: 'KZ', label: 'Kazakhstan' }
];
</script>

<template>
  <div class="config-header">
    <AppSelect :options="countryOptions" label="Country" v-model="country"> </AppSelect>
    <AppInput label="Age" placeholder="Age" type="number"> </AppInput>
  </div>
</template>

<style scoped>
  .config-header {
  position: fixed;
  display: flex;
  gap: 2rem;
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
