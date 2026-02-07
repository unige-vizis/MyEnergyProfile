<template>
  <section id="dependency" class="page-section">
    <div class="chart-header">
      <h2>Fuel by Fuel: Measuring Our Energy Import Dependence</h2>
      <p>
        The stacked bar chart below shows how much of a country’s energy supply is produced domestically and how much is
        imported from abroad, broken down by energy source. Import dependency highlights the degree to which national
        energy systems rely on foreign suppliers and therefore reflects aspects of energy security, resilience, and
        exposure to geopolitical risks. By comparing energy sources, it becomes clear that some fuels are structurally
        dependent on imports, while others are more closely tied to domestic resources. The detailed descriptions of
        each energy source below provide additional context on their role, availability, and typical dependency
        patterns.
      </p>
    </div>
    <div class="section-container">
      <div v-if="store.isLoading" class="loading">Loading energy data...</div>
      <div v-else-if="store.error" class="error">{{ store.error }}</div>
      <div class="charts-container" v-else>
        <div v-if="store.dependencyData" class="chart-section">
          <DependencyChart :dependencyData="store.dependencyData" :year="store.selectedYear" />
        </div>
      </div>
      <div class="text-container">
        <p>
          Share of imports vs domestic production ·
          <span class="formula">Net Imports ÷ Gross Available Energy</span>
          <br />
          <span class="formula">
            Net Imports = Imports − Exports · Gross Available Energy ≈ Primary production + Net imports ± Stock changes
          </span>
          <br />
          <a
            href="https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Glossary:Energy_dependency_rate"
            target="_blank"
            rel="noopener"
            class="source-link"
            >https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Glossary:Energy_dependency_rate</a
          >
        </p>
      </div>
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
import DependencyChart from '../charts/DependencyChart.vue'
import ItemsSlider from '../ItemsSlider.vue';
import Card from '../Card.vue';

const baseUrl = import.meta.env.BASE_URL + "src/assets/"
const store = useEnergyDataStore()

const fuelTypes = [
  { title: 'Electricity', imgSrc: `${baseUrl}img/fuel-electricity.jpg`, content: "Most versatile energy carrier for lighting, appliances, industry, and increasingly transport. Cannot be stored at scale, requiring real-time grid balancing. Non-EU dependency varies by geography (2022): Moldova (68%), Georgia (30%), Lithuania (25%) rely on non-EU sources; Western Europe imports almost exclusively from EU neighbors (Germany 6%, France 2%, non-EU). France is typically a net exporter thanks to its nuclear fleet." },
  { title: 'Oil & Petroleum', imgSrc: `${baseUrl}img/fuel-gas.jpg`, content: "World's largest primary energy source (~30% of global consumption). Backbone of transportation and petrochemical feedstock. High energy density (45 MJ/kg). Nearly all European countries import 90%+ (2022): Germany (97%), France (99%), Italy (93%). Norway is a major net exporter. Non-EU dependency typically 75-90% across the EU (2022)." },
  { title: 'Oil & Petroleum - Crude Oil', imgSrc: `${baseUrl}img/fuel-crude-oil.webp`, content: "Unrefined petroleum sent to refineries for gasoline, diesel, jet fuel. Quality varies by sulfur (sweet/sour) and density (light/heavy). ~98% imported in most EU countries (2022)." },
  { title: 'Oil & Petroleum - NGL', imgSrc: `${baseUrl}img/fuel-ngl.webp`, content: "Natural Gas Liquids (propane, butane, ethane). Extracted during gas processing. Typically 0% import dependency (2022) as they're separated domestically from imported gas." },
  { title: 'Natural Gas', imgSrc: `${baseUrl}img/fuel-gas.jpg`, content: "Primarily methane (CH₄). Burns 50% cleaner than coal. Critical for heating, electricity, and fertilizer production. Transported via pipelines or LNG tankers. Dependency above 100% indicates reserve drawdowns, observed during the 2022 energy crisis (Germany 106%, France 109%). In 2022: Netherlands (65%) has domestic production; Poland (78%) diversified via Baltic LNG. Norway is Europe's largest non-Russian supplier." },
  { title: 'Coal', imgSrc: `${baseUrl}img/fuel-coal.jpg`, content: 'Most carbon-intensive fossil fuel. Ranked by age: lignite → sub-bituminous → bituminous → anthracite. Still important for power and steel. Import dependency (2022): Germany ~50%; Poland (8%) and Czechia (14%) rely on domestic production. Values above 100% indicate stock usage. Being phased out across Europe due to climate commitments.' },
  { title: 'Coal - Anthracite', imgSrc: `${baseUrl}img/fuel-anthracite.jpg`, content: 'Highest grade (86-97% carbon, 30-35 MJ/kg). Burns hot and clean. Geologically rare. Most countries import 100% (2022), but Poland (79%), Slovakia (56%), and Czechia (96%) retain some domestic production.' },
  { title: 'Coal - Coking Coal', imgSrc: `${baseUrl}img/fuel-coking-coal.jpg`, content: 'Essential for blast furnace steel production. Must have low ash/sulfur. ~100% imported in most EU countries (2022) from Australia, USA, Canada.' },
  { title: 'Coal - Other Bituminous', imgSrc: `${baseUrl}img/fuel-bituminous.jpg`, content: 'Steam coal for power plants (45-86% carbon, 24-35 MJ/kg). Highest trade volume. Poland/Czechia have domestic reserves.' },
  { title: 'Coal - Sub-bituminous', imgSrc: `${baseUrl}img/fuel-sub-bituminous.jpg`, content: 'Grade between lignite and bituminous (35-45% carbon, 17-23 MJ/kg). Used mainly for power generation. Limited trade in Europe; most countries show 0% or no data (2013-2022).' },
  { title: 'Coal - Lignite', imgSrc: `${baseUrl}img/fuel-lignite.jpg`, content: "Brown coal (25-35% carbon, up to 75% moisture). Rarely traded due to low energy density and crumbling when dried. Usually 0% import (2022), but Austria (100%), Slovenia, Hungary, and Lithuania import from neighbors. Germany is Europe's largest producer." },
  { title: 'Peat', imgSrc: `${baseUrl}img/fuel-peat.jpg`, content: 'Partially decomposed organic matter from bogs. Lowest energy density (8-12 MJ/kg). Pre-coal stage fuel used historically in northern Europe for heating and power. Almost always sourced locally (0% import dependency, 2023) due to low energy density. Finland is the exception (~1%). Being phased out due to CO₂ emissions and ecosystem destruction. Most countries show no peat data.' },
]
</script>

<style scoped>
.mix-subsection {
  margin-bottom: 3rem;
}

.mix-subsection:last-child {
  margin-bottom: 0;
}

.mix-subsection h3 {
  font-size: 1.4rem;
  margin-bottom: 0.75rem;
  color: #2c3e50;
}

.mix-subsection > p {
  color: #666;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.loading,
.error {
  padding: 2rem;
  text-align: center;
  color: #666;
}

.error {
  color: var(--text-color-red);
}
</style>
