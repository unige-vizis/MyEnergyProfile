<template>
  <div v-if="gridIntensity == null" class="no-data">
    <span class="material-symbols-outlined">info</span>
    <p>No grid intensity data available to compute comparisons.</p>
  </div>
  <div v-else class="stat-cards-wrapper">
    <div v-for="group in groupedCards" :key="group.label" class="stat-group">
      <h4 class="group-label">
        <span class="material-symbols-outlined group-icon" :style="{ color: group.color }">{{ group.icon }}</span>
        {{ group.label }}
      </h4>
      <div class="stat-cards-grid">
        <div
          v-for="card in group.cards"
          :key="card.id"
          class="stat-card"
          :class="card.colorClass"
        >
          <div class="card-icon">
            <span class="material-symbols-outlined">{{ card.icon }}</span>
          </div>
          <div class="card-content">
            <h4 class="card-title">{{ card.title }}</h4>
            <p class="card-result">{{ card.result }}</p>
            <p class="card-detail">{{ card.detail }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  gridIntensity: { type: Number, default: null }
})

// ── Shared constants (IPCC AR6 WGIII + IEA + Eurostat + EPA + ICCT + DOE) ──

// Transport
const PETROL_CAR_G_PER_KM = 166           // EU fleet avg (IPCC AR6 / EEA)
const EV_KWH_PER_KM = 0.20               // IEA Global EV Outlook 2024
const TRAIN_KWH_PER_PKM = 0.06           // IEA transport energy intensity (EU electric rail)

// Household
const HP_SCOP = 3.0                       // IEA Future of Heat Pumps (residential avg)
const COMBINED_GAS_HEATING_G = 220        // Weighted avg: 80% space (215) + 20% water (256)
const AVG_HOUSEHOLD_KWH = 3500           // Eurostat EU avg household electricity

// Services
const DC_IT_LOAD_KW = 77400              // NTT Frankfurt 1: 77.4 MW IT load
const DC_PUE = 1.55                      // Uptime Institute global avg (~2023-2024)
const DIESEL_TRUCK_G_PER_KM = 885        // ICCT 2023: 33 L/100km x 2.68 kgCO2/L (40t long-haul)
const ELECTRIC_TRUCK_KWH_PER_KM = 1.30   // ICCT 2025: real-world EU avg (40t tractor-trailer)

// Industry
const ELECTROLYSIS_KWH_PER_KG_H2 = 55    // DOE H2 Program Record #24005: PEM system-level
const SMR_KG_CO2_PER_KG_H2 = 9           // IEA Global Hydrogen Review 2024: SMR direct emissions
const BF_T_CO2_PER_T_STEEL = 2.2         // IEA steel sector (BF-BOF route)
const EAF_KWH_PER_T_STEEL = 400          // IEA steel data (scrap-based EAF)
const EAF_DIRECT_KG_CO2_PER_T = 50       // EAF process emissions (electrodes, lime)

function colorClass(electricG, conventionalG) {
  const ratio = electricG / conventionalG
  if (ratio < 0.5) return 'card-green'
  if (ratio <= 1.0) return 'card-yellow'
  return 'card-red'
}

const cards = computed(() => {
  const gi = props.gridIntensity
  if (gi == null) return []

  const results = []

  // ── Transport ──
  const evG = EV_KWH_PER_KM * gi
  const evRatio = PETROL_CAR_G_PER_KM / evG
  results.push({
    id: 'ev', group: 'transport',
    icon: 'electric_car',
    title: 'EV vs Petrol Car',
    result: evRatio >= 1
      ? `${evRatio.toFixed(1)}x less CO\u2082 per km`
      : `${(1 / evRatio).toFixed(1)}x more CO\u2082 per km`,
    detail: `EV: ${Math.round(evG)} gCO\u2082/km (0.20 kWh/km). Petrol: ${PETROL_CAR_G_PER_KM} gCO\u2082/km.`,
    colorClass: colorClass(evG, PETROL_CAR_G_PER_KM)
  })

  const trainG = TRAIN_KWH_PER_PKM * gi
  const trainRatio = PETROL_CAR_G_PER_KM / trainG
  results.push({
    id: 'train', group: 'transport',
    icon: 'train',
    title: 'Electric Train vs Car',
    result: trainRatio >= 1
      ? `${trainRatio.toFixed(1)}x less CO\u2082 per passenger-km`
      : `${(1 / trainRatio).toFixed(1)}x more CO\u2082 per passenger-km`,
    detail: `Train: ${trainG.toFixed(1)} gCO\u2082/pkm (0.06 kWh/pkm). Car: ${PETROL_CAR_G_PER_KM} gCO\u2082/km.`,
    colorClass: colorClass(trainG, PETROL_CAR_G_PER_KM)
  })

  // ── Household ──
  const hpG = gi / HP_SCOP
  const hpSaving = ((COMBINED_GAS_HEATING_G - hpG) / COMBINED_GAS_HEATING_G * 100)
  results.push({
    id: 'hp', group: 'household',
    icon: 'heat_pump',
    title: 'Heat Pump vs Gas (Heating + Hot Water)',
    result: hpSaving > 0
      ? `${Math.round(hpSaving)}% less CO\u2082`
      : `${Math.round(-hpSaving)}% more CO\u2082`,
    detail: `HP: ${Math.round(hpG)} gCO\u2082/kWh_th (SCOP ${HP_SCOP}). Gas: ${COMBINED_GAS_HEATING_G} gCO\u2082/kWh_th (weighted avg).`,
    colorClass: colorClass(hpG, COMBINED_GAS_HEATING_G)
  })

  const householdTonnes = (AVG_HOUSEHOLD_KWH * gi) / 1e6
  const equivKm = (householdTonnes * 1e6) / PETROL_CAR_G_PER_KM
  results.push({
    id: 'footprint', group: 'household',
    icon: 'home',
    title: 'Household Electricity Footprint',
    result: `${householdTonnes.toFixed(2)} tCO\u2082/yr \u2248 ${Math.round(equivKm).toLocaleString()} km by petrol car`,
    detail: `From ${AVG_HOUSEHOLD_KWH.toLocaleString()} kWh/yr (EU avg household). Car equivalent at ${PETROL_CAR_G_PER_KM} gCO\u2082/km.`,
    colorClass: householdTonnes < 0.5 ? 'card-green' : householdTonnes < 1.5 ? 'card-yellow' : 'card-red'
  })

  // ── Services ──
  const dcTotalKw = DC_IT_LOAD_KW * DC_PUE
  const dcKwhPerHour = Math.round(dcTotalKw)
  const dcGCO2PerHour = dcKwhPerHour * gi
  const dcKmPerHour = Math.round(dcGCO2PerHour / PETROL_CAR_G_PER_KM)
  results.push({
    id: 'datacenter', group: 'services',
    icon: 'dns',
    title: 'Data Center (NTT Frankfurt 1)',
    result: `1 hr of operation \u2248 ${dcKmPerHour.toLocaleString()} km by petrol car`,
    detail: `Est. ${dcKwhPerHour.toLocaleString()} kWh/hr (77.4 MW IT, PUE ${DC_PUE}).`,
    colorClass: dcKmPerHour < 30000 ? 'card-green' : dcKmPerHour < 120000 ? 'card-yellow' : 'card-red'
  })

  const eTruckG = ELECTRIC_TRUCK_KWH_PER_KM * gi
  const truckRatio = DIESEL_TRUCK_G_PER_KM / eTruckG
  results.push({
    id: 'truck', group: 'services',
    icon: 'local_shipping',
    title: 'Electric Truck vs Diesel Truck (Logistics)',
    result: truckRatio >= 1
      ? `${truckRatio.toFixed(1)}x less CO\u2082 per km`
      : `${(1 / truckRatio).toFixed(1)}x more CO\u2082 per km`,
    detail: `Electric: ${Math.round(eTruckG)} gCO\u2082/km (1.30 kWh/km). Diesel: ${DIESEL_TRUCK_G_PER_KM} gCO\u2082/km (33 L/100km, 40t).`,
    colorClass: colorClass(eTruckG, DIESEL_TRUCK_G_PER_KM)
  })

  // ── Industry ──
  const electrolyserKgCO2 = ELECTROLYSIS_KWH_PER_KG_H2 * gi / 1000
  const h2Saving = ((SMR_KG_CO2_PER_KG_H2 - electrolyserKgCO2) / SMR_KG_CO2_PER_KG_H2 * 100)
  results.push({
    id: 'green-h2', group: 'industry',
    icon: 'science',
    title: 'Green Hydrogen vs Grey Hydrogen',
    result: h2Saving > 0
      ? `${Math.round(h2Saving)}% less CO\u2082 per kg H\u2082`
      : `${Math.round(-h2Saving)}% more CO\u2082 per kg H\u2082`,
    detail: `Electrolysis: ${electrolyserKgCO2.toFixed(1)} kgCO\u2082/kgH\u2082 (${ELECTROLYSIS_KWH_PER_KG_H2} kWh/kg). SMR: ${SMR_KG_CO2_PER_KG_H2} kgCO\u2082/kgH\u2082.`,
    colorClass: colorClass(electrolyserKgCO2, SMR_KG_CO2_PER_KG_H2)
  })

  const eafElecKg = EAF_KWH_PER_T_STEEL * gi / 1000
  const eafTotalKg = eafElecKg + EAF_DIRECT_KG_CO2_PER_T
  const bfKg = BF_T_CO2_PER_T_STEEL * 1000
  const steelSaving = ((bfKg - eafTotalKg) / bfKg * 100)
  results.push({
    id: 'steel', group: 'industry',
    icon: 'construction',
    title: 'Electric Arc Furnace vs Blast Furnace',
    result: steelSaving > 0
      ? `${Math.round(steelSaving)}% less CO\u2082 per tonne steel`
      : `${Math.round(-steelSaving)}% more CO\u2082 per tonne steel`,
    detail: `EAF: ${Math.round(eafTotalKg)} kgCO\u2082/t (${EAF_KWH_PER_T_STEEL} kWh). BF-BOF: ${bfKg.toLocaleString()} kgCO\u2082/t.`,
    colorClass: colorClass(eafTotalKg, bfKg)
  })

  return results
})

const groupedCards = computed(() => {
  const groups = [
    { key: 'transport', label: 'Transport', icon: 'directions_car', color: '#ffb56b' },
    { key: 'household', label: 'Household', icon: 'home', color: '#63b3df' },
    { key: 'services', label: 'Services', icon: 'business', color: '#76d76b' },
    { key: 'industry', label: 'Industry', icon: 'factory', color: '#898989' }
  ]
  return groups.map(g => ({
    ...g,
    cards: cards.value.filter(c => c.group === g.key)
  })).filter(g => g.cards.length > 0)
})
</script>

<style scoped>
.no-data {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 200px;
  color: var(--placeholder-color);
  gap: 0.5rem;
}
.no-data .material-symbols-outlined {
  font-size: 48px;
}

.stat-cards-wrapper {
  width: 100%;
}

.stat-group {
  margin-bottom: 1rem;
}

.group-label {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  margin: 0 0 0.5rem;
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--text-color-basic);
}

.group-icon {
  font-size: 20px;
  color: var(--text-color-gray);
}

.stat-cards-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
  width: 100%;
}

.stat-card {
  display: flex;
  gap: 0.75rem;
  padding: 0.75rem;
  border-radius: 8px;
  border: 1.5px solid #ddd;
  background: #fff;
  transition: box-shadow 0.2s;
}

.stat-card:hover {
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.card-green {
  border-color: #27ae60;
  background: rgba(39, 174, 96, 0.04);
}
.card-yellow {
  border-color: #f39c12;
  background: rgba(243, 156, 18, 0.04);
}
.card-red {
  border-color: #e74c3c;
  background: rgba(231, 76, 60, 0.04);
}

.card-icon {
  display: flex;
  align-items: flex-start;
  padding-top: 0.1rem;
}
.card-green .card-icon .material-symbols-outlined { color: #27ae60; }
.card-yellow .card-icon .material-symbols-outlined { color: #f39c12; }
.card-red .card-icon .material-symbols-outlined { color: #e74c3c; }

.card-icon .material-symbols-outlined {
  font-size: 28px;
}

.card-content {
  flex: 1;
  min-width: 0;
}

.card-title {
  margin: 0 0 0.2rem;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-color-basic);
}

.card-result {
  margin: 0 0 0.15rem;
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--text-color-basic);
}

.card-detail {
  margin: 0;
  font-size: 0.75rem;
  color: #888;
  line-height: 1.3;
}


</style>
