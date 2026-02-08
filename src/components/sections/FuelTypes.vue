<template>
  <section id="fueltypes" class="page-section">
    <div class="chart-header">
      <h2>Energy as a Resource: Understanding the Sources</h2>
    </div>
    <ItemsSlider title="Types of Fuel">
      <div v-for="(item, index) in fuelTypes" :key="index">
        <Card :title="item.title" :content="item.content" :imgSrc="item.imgSrc" />
      </div>
    </ItemsSlider>
  </section>
</template>

<script setup>
import { useEnergyDataStore } from '@/stores/energyData'
import ItemsSlider from '../ItemsSlider.vue';
import Card from '../Card.vue';

const store = useEnergyDataStore()

const fuelTypes = [
  { title: 'Electricity', imgSrc: `fuel-electricity.jpg`, content: "A comon miss conception is to think of energy as just electricity. While it is the most versatile energy carrier for lighting, appliances, industry, and increasingly transport it's just a part of what is consumed at scale and often product from other fossil sources. Cannot be stored at scale, requiring real-time grid balancing." },
  // TODO - Petula: dependency raus
  { title: 'Oil & Petroleum', imgSrc: `fuel-gas.jpg`, content: "World's largest primary energy source. Backbone of transportation and petrochemical feedstock. High energy density (45 MJ/kg). Nearly all European countries import 90%+ (2022): Germany (97%), France (99%), Italy (93%). Norway is a major net exporter. Non-EU dependency typically 75-90% across the EU (2022)." },
  { title: 'Oil & Petroleum - Crude Oil', imgSrc: `fuel-crude-oil.webp`, content: "Unrefined petroleum sent to refineries for gasoline, diesel, jet fuel. Quality varies by sulfur (sweet/sour) and density (light/heavy). ~98% imported in most EU countries (2022)." },
  { title: 'Oil & Petroleum - NGL', imgSrc: `fuel-ngl.webp`, content: "Natural Gas Liquids (propane, butane, ethane). Extracted during gas processing. Typically 0% import dependency (2022) as they're separated domestically from imported gas." },
  { title: 'Natural Gas', imgSrc: `fuel-gas.jpg`, content: "Primarily methane (CH₄). Burns 50% cleaner than coal. Critical for heating, electricity, and fertilizer production. Transported via pipelines or LNG tankers. Dependency above 100% indicates reserve drawdowns, observed during the 2022 energy crisis (Germany 106%, France 109%). In 2022: Netherlands (65%) has domestic production; Poland (78%) diversified via Baltic LNG. Norway is Europe's largest non-Russian supplier." },
  { title: 'Coal', imgSrc: `fuel-coal.jpg`, content: 'Most carbon-intensive fossil fuel. Ranked by age: lignite → sub-bituminous → bituminous → anthracite. Still important for power and steel. Import dependency (2022): Germany ~50%; Poland (8%) and Czechia (14%) rely on domestic production. Values above 100% indicate stock usage. Being phased out across Europe due to climate commitments.' },
  { title: 'Coal - Anthracite', imgSrc: `fuel-anthracite.jpg`, content: 'Highest grade (86-97% carbon, 30-35 MJ/kg). Burns hot and clean. Geologically rare. Most countries import 100% (2022), but Poland (79%), Slovakia (56%), and Czechia (96%) retain some domestic production.' },
  { title: 'Coal - Coking Coal', imgSrc: `fuel-coking-coal.jpg`, content: 'Essential for blast furnace steel production. Must have low ash/sulfur. ~100% imported in most EU countries (2022) from Australia, USA, Canada.' },
  { title: 'Coal - Other Bituminous', imgSrc: `fuel-bituminous.jpg`, content: 'Steam coal for power plants (45-86% carbon, 24-35 MJ/kg). Highest trade volume. Poland/Czechia have domestic reserves.' },
  { title: 'Coal - Sub-bituminous', imgSrc: `fuel-sub-bituminous.jpg`, content: 'Grade between lignite and bituminous (35-45% carbon, 17-23 MJ/kg). Used mainly for power generation. Limited trade in Europe; most countries show 0% or no data (2013-2022).' },
  { title: 'Coal - Lignite', imgSrc: `fuel-lignite.jpg`, content: "Brown coal (25-35% carbon, up to 75% moisture). Rarely traded due to low energy density and crumbling when dried. Usually 0% import (2022), but Austria (100%), Slovenia, Hungary, and Lithuania import from neighbors. Germany is Europe's largest producer." },
  { title: 'Peat', imgSrc: `fuel-peat.jpg`, content: 'Partially decomposed organic matter from bogs. Lowest energy density (8-12 MJ/kg). Pre-coal stage fuel used historically in northern Europe for heating and power. Almost always sourced locally (0% import dependency, 2023) due to low energy density. Finland is the exception (~1%). Being phased out due to CO₂ emissions and ecosystem destruction. Most countries show no peat data.' },
]
</script>

<style scoped>
.loading,
.error {
  padding: 2rem;
  text-align: center;
  color: var(--text-color-gray);
}

.error {
  color: var(--text-color-red);
}
</style>
