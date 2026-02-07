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

        <!-- Electricity -->
        <div class="fuel-group">
          <div class="fuel-group-title">Electricity</div>
          <div class="fuel-group-content">
            <img :src="`${baseUrl}img/fuel-electricity.jpg`" alt="Electricity" class="fuel-img-large" />
            <p>
              Most versatile energy carrier for lighting, appliances, industry, and increasingly transport. Cannot be
              stored at scale, requiring real-time grid balancing. Non-EU dependency varies by geography (2022): Moldova
              (68%), Georgia (30%), Lithuania (25%) rely on non-EU sources; Western Europe imports almost exclusively
              from EU neighbors (Germany 6%, France 2%, non-EU). France is typically a net exporter thanks to its
              nuclear fleet.
            </p>
          </div>
        </div>

        <!-- Oil -->
        <div class="fuel-group">
          <div class="fuel-group-title">Oil &amp; Petroleum</div>
          <div class="fuel-group-content">
            <img :src="`${baseUrl}img/fuel-oil.jpg`" alt="Oil" class="fuel-img-large" />
            <p>
              World's largest primary energy source (~30% of global consumption). Backbone of transportation and
              petrochemical feedstock. High energy density (45 MJ/kg). Nearly all European countries import 90%+ (2022):
              Germany (97%), France (99%), Italy (93%). Norway is a major net exporter. Non-EU dependency typically
              75-90% across the EU (2022).
            </p>
          </div>
          <div class="fuel-subresources">
            <div class="fuel-subresource">
              <img :src="`${baseUrl}img/fuel-crude-oil.jpg`" alt="Crude Oil" class="fuel-img-small" />
              <div class="subresource-content">
                <strong>Crude Oil </strong>
                <span class="subresource-desc"
                  >Unrefined petroleum sent to refineries for gasoline, diesel, jet fuel. Quality varies by sulfur
                  (sweet/sour) and density (light/heavy). ~98% imported in most EU countries (2022).</span
                >
              </div>
            </div>
            <div class="fuel-subresource">
              <img :src="`${baseUrl}img/fuel-ngl.jpg`" alt="NGL" class="fuel-img-small" />
              <div class="subresource-content">
                <strong>NGL </strong>
                <span class="subresource-desc"
                  >Natural Gas Liquids (propane, butane, ethane). Extracted during gas processing. Typically 0% import
                  dependency (2022) as they're separated domestically from imported gas.</span
                >
              </div>
            </div>
          </div>
        </div>

        <!-- Gas -->
        <div class="fuel-group">
          <div class="fuel-group-title">Natural Gas</div>
          <div class="fuel-group-content">
            <img :src="`${baseUrl}img/fuel-gas.jpg`" alt="Gas" class="fuel-img-large" />
            <p>
              Primarily methane (CH₄). Burns 50% cleaner than coal. Critical for heating, electricity, and fertilizer
              production. Transported via pipelines or LNG tankers. Dependency above 100% indicates reserve drawdowns,
              observed during the 2022 energy crisis (Germany 106%, France 109%). In 2022: Netherlands (65%) has
              domestic production; Poland (78%) diversified via Baltic LNG. Norway is Europe's largest non-Russian
              supplier.
            </p>
          </div>
        </div>

        <!-- Coal -->
        <div class="fuel-group">
          <div class="fuel-group-title">Coal</div>
          <div class="fuel-group-content">
            <img :src="`${baseUrl}img/fuel-coal.jpg`" alt="Coal" class="fuel-img-large" />
            <p>
              Most carbon-intensive fossil fuel. Ranked by age: lignite → sub-bituminous → bituminous → anthracite.
              Still important for power and steel. Import dependency (2022): Germany ~50%; Poland (8%) and Czechia (14%)
              rely on domestic production. Values above 100% indicate stock usage. Being phased out across Europe due to
              climate commitments.
            </p>
          </div>
          <div class="fuel-subresources">
            <div class="fuel-subresource">
              <img :src="`${baseUrl}img/fuel-anthracite.jpg`" alt="Anthracite" class="fuel-img-small" />
              <div class="subresource-content">
                <strong>Anthracite </strong>
                <span class="subresource-desc"
                  >Highest grade (86-97% carbon, 30-35 MJ/kg). Burns hot and clean. Geologically rare. Most countries
                  import 100% (2022), but Poland (79%), Slovakia (56%), and Czechia (96%) retain some domestic
                  production.</span
                >
              </div>
            </div>
            <div class="fuel-subresource">
              <img :src="`${baseUrl}img/fuel-coking-coal.jpg`" alt="Coking Coal" class="fuel-img-small" />
              <div class="subresource-content">
                <strong>Coking Coal </strong>
                <span class="subresource-desc"
                  >Essential for blast furnace steel production. Must have low ash/sulfur. ~100% imported in most EU
                  countries (2022) from Australia, USA, Canada.</span
                >
              </div>
            </div>
            <div class="fuel-subresource">
              <img :src="`${baseUrl}img/fuel-bituminous.jpg`" alt="Other Bituminous" class="fuel-img-small" />
              <div class="subresource-content">
                <strong>Other Bituminous </strong>
                <span class="subresource-desc"
                  >Steam coal for power plants (45-86% carbon, 24-35 MJ/kg). Highest trade volume. Poland/Czechia have
                  domestic reserves.</span
                >
              </div>
            </div>
            <div class="fuel-subresource">
              <img :src="`${baseUrl}img/fuel-sub-bituminous.jpg`" alt="Sub-bituminous" class="fuel-img-small" />
              <div class="subresource-content">
                <strong>Sub-bituminous </strong>
                <span class="subresource-desc"
                  >Grade between lignite and bituminous (35-45% carbon, 17-23 MJ/kg). Used mainly for power generation.
                  Limited trade in Europe; most countries show 0% or no data (2013-2022).</span
                >
              </div>
            </div>
            <div class="fuel-subresource">
              <img :src="`${baseUrl}img/fuel-lignite.jpg`" alt="Lignite" class="fuel-img-small" />
              <div class="subresource-content">
                <strong>Lignite </strong>
                <span class="subresource-desc"
                  >Brown coal (25-35% carbon, up to 75% moisture). Rarely traded due to low energy density and crumbling
                  when dried. Usually 0% import (2022), but Austria (100%), Slovenia, Hungary, and Lithuania import from
                  neighbors. Germany is Europe's largest producer.</span
                >
              </div>
            </div>
          </div>
        </div>

        <!-- Peat -->
        <div class="fuel-group">
          <div class="fuel-group-title">Peat</div>
          <div class="fuel-group-content">
            <img :src="`${baseUrl}img/fuel-peat.jpg`" alt="Peat" class="fuel-img-large" />
            <p>
              Partially decomposed organic matter from bogs. Lowest energy density (8-12 MJ/kg). Pre-coal stage fuel
              used historically in northern Europe for heating and power. Almost always sourced locally (0% import
              dependency, 2023) due to low energy density. Finland is the exception (~1%). Being phased out due to CO₂
              emissions and ecosystem destruction. Most countries show no peat data.
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { useEnergyDataStore } from '@/stores/energyData'
import DependencyChart from '../charts/DependencyChart.vue'

const baseUrl = import.meta.env.BASE_URL + "src/assets/"
const store = useEnergyDataStore()
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
  color: #c44536;
}

.fuel-group {
  margin-bottom: 0.6rem;
  padding-bottom: 0.6rem;
  border-bottom: 1px solid #eee;
}

.fuel-group p {
  margin: 0;
}

.fuel-group:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.fuel-group-title {
  font-weight: 600;
  font-size: 0.9rem;
  color: #333;
  margin-bottom: 0.3rem;
}

.fuel-group-content {
  display: flex;
  gap: 0.6rem;
  align-items: flex-start;
}

.fuel-img-large {
  width: 72px;
  height: 72px;
  object-fit: contain;
  background: #f5f5f5;
  border-radius: 4px;
  padding: 4px;
  flex-shrink: 0;
}

.fuel-subresources {
  margin-top: 0.4rem;
  margin-left: 78px;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.fuel-subresource {
  display: flex;
  gap: 0.4rem;
  align-items: flex-start;
  padding: 0.3rem 0;
}

.fuel-img-small {
  width: 72px;
  height: 72px;
  object-fit: contain;
  background: #f8f8f8;
  border-radius: 3px;
  padding: 4px;
  flex-shrink: 0;
}
</style>
