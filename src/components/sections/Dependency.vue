<template>
  <section id="dependency" class="page-section">
    <div class="chart-header">
      <h2>Fuel by Fuel: Measuring The Energy Import Dependence</h2>
    </div>
    <div class="section-container">
      <div v-if="store.isLoading" class="loading">Loading energy data...</div>
      <div v-else-if="store.error" class="error">{{ store.error }}</div>
      <div v-if="store.dependencyData" class="charts-container">
        <DependencyChart :dependencyData="store.dependencyData" :year="store.selectedYear" :countryName="store.selectedCountry?.name || ''" />
      </div>
      <div class="text-container">
        <!-- Electricity: Non-EU dependency varies by geography (2022): Moldova (68%), Georgia (30%), Lithuania (25%) rely on non-EU sources; Western Europe imports almost exclusively from EU neighbors (Germany 6%, France 2%, non-EU). France is typically a net exporter thanks to its nuclear fleet. 
          Oil & Petroleum: Nearly all European countries import 90%+ (2022): Germany (97%), France (99%), Italy (93%). Norway is a major net exporter. Non-EU dependency typically 75-90% across the EU (2022)." },
          Oil & Petroleum - Crude Oil: ~98% imported in most EU countries (2022)." },
          Oil & Petroleum - NGL: Typically 0% import dependency (2022) as they're separated domestically from imported gas." },
          Natural Gas: Dependency above 100% indicates reserve drawdowns, observed during the 2022 energy crisis (Germany 106%, France 109%). In 2022: Netherlands (65%) has domestic production; Poland (78%) diversified via Baltic LNG. Norway is Europe's largest non-Russian supplier." },
          Coal: Import dependency (2022): Germany ~50%; Poland (8%) and Czechia (14%) rely on domestic production. Values above 100% indicate stock usage. Being phased out across Europe due to climate commitments.' },
          Coal - Anthracite: Most countries import 100% (2022), but Poland (79%), Slovakia (56%), and Czechia (96%) retain some domestic production.' },
          Coal - Coking Coal: ~100% imported in most EU countries (2022) from Australia, USA, Canada.' },
          Coal - Other Bituminous: Highest trade volume. Poland/Czechia have domestic reserves.' },
          Coal - Sub-bituminous: Limited trade in Europe; most countries show 0% or no data (2013-2022).' },
          Coal - Lignite: 0% import (2022), but Austria (100%), Slovenia, Hungary, and Lithuania import from neighbors. Germany is Europe's largest producer." },
          Peat: Almost always sourced locally (0% import dependency, 2023) due to low energy density. Finland is the exception (~1%). Being phased out due to CO₂ emissions and ecosystem destruction. Most countries show no peat data.' }, -->
        <p>
          The stacked bar chart shows how much of a country’s energy supply is produced
          <span style="color: #81b29a; font-weight: 600;">domestically</span> and how much is
          <span style="color: #e8a87c; font-weight: 600;">imported</span> from abroad. Import dependency highlights the
          degree to which national energy systems rely on foreign suppliers and therefore reflects vulnerability to
          geopolitical risks.
        </p>
        <p>
          Non‑EU neighbours such as Moldova (~68%) and Georgia (~30%) rely heavily on external
          <strong>electricity</strong> providers, while Western Europe trades mostly within the EU. France is typically
          a <span style="color: #7b68ee; font-weight: 600;">net exporter</span> thanks to its nuclear fleet.
          <strong>0il & petroleum</strong> are imported 90%+ (2022) by nearly all European countries. Dependence on
          <strong>natural gas</strong> increased rapidly during the 2022 crisis, with some countries even
          <span style="color: #8b2500; font-weight: 600;">drawing their reserves</span> from previous years, such as
          Germany (106%) and France (109%).
        </p>
        <p>
          Countries like Germany imported around half their needs of <strong>Coal</strong>, while Poland and Czechia
          still rely heavily on domestic hard coal. Nearly all EU countries depend almost entirely on imports for
          <strong>anthracite</strong> and <strong>coking coal</strong>. <strong>Lignite</strong> remains almost
          exclusively local due to poor transportability.
        </p>
        <p>
          Now that we know how reliant many countries are on imported energy, we can look at who they depend on.
          Europe’s fuel mix is shaped by a small set of major trading partners, from Norway for gas to Saudi Arabia and
          the U.S. for oil with Russia’s role sharply reduced after 2022.
        </p>
      </div>
    </div>
    <div class="chart-meta">
      <div class="meta-section">
        <span class="meta-label">Source</span>
        <ul class="meta-list">
          <li>
            Eurostat
            <a href="https://ec.europa.eu/eurostat/web/energy/database" target="_blank" rel="noopener"
              >Energy Database</a
            >
            (European Commission)
          </li>
          <li>
            Tables <code>nrg_ind_id</code> (ID, overall dependency) and <code>nrg_ind_id3cf</code> (ID3CF, third country
            dependency)
          </li>
          <li>
            Table <code>nrg_bal_c</code> (complete energy balances): Gross Available Energy by SIEC subcategory, used for
            subcategory bar width proportions
          </li>
          <li>Fuel breakdown via SIEC codes mapped to display names</li>
        </ul>
      </div>
      <div class="meta-section">
        <span class="meta-label">Data Hints</span>
        <ul class="meta-list">
          <li>
            Non-EU breakdown (hatched line) only available for main aggregates (Coal, Gas, Oil, Electricity).
            Subcategory bar widths are proportional to their share of the parent category's Gross Available Energy (GAE).
          </li>
          <li>Non-EU (third country) import dependency data is only available from 2010 to 2023.</li>
          <li>Electricity: Eurostat does not calculate overall import dependency; showing non-EU imports only.</li>
        </ul>
      </div>
    </div>
  </section>
</template>

<script setup>
import { useEnergyDataStore } from '@/stores/energyData'
import DependencyChart from '../charts/DependencyChart.vue'

const store = useEnergyDataStore()
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

.legend-color{
  border-radius: 3px;
  display: inline-block;
}
</style>
