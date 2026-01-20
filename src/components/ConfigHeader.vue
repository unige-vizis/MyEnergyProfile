<script setup>
import AppInput from './inputElements/AppInput.vue';
import AppSelect from './inputElements/AppSelect.vue';
import { ref } from 'vue';

const country = ref('');
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

const householdSize = [
  {value:1, label:1},
  {value:2, label:2},
  {value:3, label:3},
  {value:4, label:4},
  {value:5, label:5},
  {value:6, label:'6+'},
];
</script>

<template>
  <div class="config-header">
    <AppSelect class="config-item" :options="countryOptions" label="Country" v-model="country" placeholder="Germany">
    </AppSelect>
    <AppInput class="config-item" label="Age" placeholder="Age" type="number"> </AppInput>
    <AppSelect class="config-item" :options="householdSize" label="Household Size" placeholder="2"></AppSelect>
    <AppInput class="config-item" label="Living Space" placeholder="Living Space" type="number" :min="10" :max="500">
    </AppInput>
    <AppInput class="config-item" label="Year" placeholder="Year" type="number" :min="1970" :max="2024"> </AppInput>
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

.config-item {
  flex: 0 0 200px;
  min-width: 200px;
}

.config-header :deep(input),
.config-header :deep(select) {
  width: 100%;
  height: 42px;
  box-sizing: border-box;
  padding: 0 0.75rem;
  border-radius: 10px;
}

.config-header :deep(label) {
  display: block;
  margin-bottom: 0.5rem;
}
.config-header :deep(input::placeholder) {
  color: #9ca3af; /* grau */
  opacity: 1;     /* wichtig für Firefox */
}
/* grauer Placeholder-Zustand */
.config-header :deep(select:has(option:checked[value=""])) {
  color: #9ca3af;
}

/* normale Farbe, sobald echte Auswahl */
.config-header :deep(select) {
  color: black;
}
</style>
