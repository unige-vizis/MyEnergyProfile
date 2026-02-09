<script setup>
import AppSelect from './inputElements/AppSelect.vue';
import YearSlot from './inputElements/YearSlot.vue';
import { ref, computed, onMounted } from 'vue';
import { useEnergyDataStore } from '@/stores/energyData';
import { useGlobalConfigStore } from '@/stores/globalConfig';

const energyStore = useEnergyDataStore();
const globalConfig = useGlobalConfigStore();

// Country options from eurostat data
const countryOptions = computed(() => {
  return energyStore.countries.map(c => ({
    value: c.code,
    label: c.name
  }));
});


// Computed getters/setters for store values
const selectedCountry = computed({
  get: () => energyStore.selectedCountryCode,
  set: (val) => energyStore.setSelectedCountry(val)
});

const selectedYear = computed({
  get: () => energyStore.selectedYear,
  set: (val) => energyStore.setSelectedYear(Number(val))
});

// Local state for fields that don't have an effect yet
const age = ref('');
const householdSizeValue = ref('');
const livingSpace = ref('');

const householdSizeOptions = [
  {value:1, label:1},
  {value:2, label:2},
  {value:3, label:3},
  {value:4, label:4},
  {value:5, label:5},
  {value:6, label:'6+'},
];

onMounted(() => {
  energyStore.loadData();
});
import { useRoute, useRouter } from "vue-router";

const router = useRouter();
const route = useRoute();

const isInfo = computed(() => route.path.startsWith("/info"));

function openMethodology() {
  router.push("/info");
}
</script>

<template>
  <div class="config-header">
    <template v-if="!isInfo">
      <AppSelect
        class="config-item"
        :options="countryOptions"
        label="Country"
        v-model="selectedCountry"
        placeholder="Select country"
      />
      <YearSlot class="config-item" :years="globalConfig.yearsDescending" label="Year" v-model="selectedYear" />
    </template>

    <button
      class="methodology-button"
      @click="openMethodology"
      type="button"
      aria-label="Info / Methodology"
      title="Info / Methodology"
    >
      <span class="material-symbols-outlined">info</span>
    </button>
  </div>
</template>

<style scoped>
  .config-header{
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  box-sizing: border-box;

  display: flex;
  gap: 2rem;
  align-items: flex-end;

  margin-left: 2rem;
  padding-left: var(--sidebar-width);   /* Platz für Sidebar */
  padding-right: 2rem;   /* ✅ damit der Button fast ganz rechts sitzt */
  padding-top: 2rem;
  padding-bottom: 2rem;

  background: var(--secondary-color);
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
  background-color: var(--primary-color);
}

.config-header :deep(label) {
  display: block;
  margin-bottom: 0.5rem;
}
.config-header :deep(input::placeholder) {
  color: var(--placeholder-color); /* grau */
  opacity: 1;     /* wichtig für Firefox */
}
/* grauer Placeholder-Zustand */
.config-header :deep(select:has(option:checked[value=""])) {
  color: var(--placeholder-color);
}

/* normale Farbe, sobald echte Auswahl */
.config-header :deep(select) {
  color: black;
}
</style>
