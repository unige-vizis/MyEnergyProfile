<template>
  <section id="eco" class="page-section">
    <div class="chart-header">
      <h2>Ecological Footprint of Energy Use</h2>
      <p>
        Of course no project about energy can be considered complete without a section dedicated to the
        ecological aspects of energy use. While there are other important environmental impacts to consider,
        we will focus on the most fundamental one: carbon emissions. First in a broad per capita breakdown, and
        then through the lens of carbon intensity, which relates electricity to carbon emissions. This is a key
        factor determining how much impact measures, that we consider as sustainable, will have in practice.
      </p>
    </div>

    <!-- Subsection 1: CO2 Emissions -->
    <div class="eco-subsection">
      <h3>CO2 Emissions - Europe Comparison</h3>
      <p>
        Total CO2 emissions per person from energy use across all sectors, measured in tonnes per year.
      </p>
      <div class="section-container">
        <div v-if="store.isLoading" class="loading">Loading energy data...</div>
        <div v-else-if="store.error" class="error">{{ store.error }}</div>
        <template v-else>
          <div v-if="!store.ecoLoaded" class="no-data">Eco data not available.</div>
          <div v-else class="charts-container">
            <div class="charts-fill">
              <EmissionsPerCapitaRanking
                :rankingData="store.emissionsPerCapitaRanking"
                :selectedCountryCode="store.selectedCountryCode"
              />
            </div>
          </div>
        </template>
        <div class="text-container">
          <h4 v-if="totalEmissionsPerCapita != null">
            Where are the
            <span class="highlight-value">{{ totalEmissionsPerCapita }} tCO&#x2082;</span>
            emissions in
            <span class="highlight-value">{{ store.selectedCountry?.name }}</span>
            emitted?
          </h4>
          <h4 v-else>Where are the emissions in your country emitted?</h4>
          <p>
            The chart below breaks down how much CO2 each person causes through four major
            sectors: residential energy use (heating, appliances), services (commercial buildings, offices),
            transport (cars, trucks), and industry (manufacturing).
          </p>
          <EmissionsCloudPie
            :emissionsData="store.emissionsPerCapita"
            :countryName="store.selectedCountry?.name || ''"
          />
          <p>
            Transport tends to be the single largest contributor in most European countries, reflecting
            heavy reliance on fossil fuels for road mobility. In Lithuania, transport accounts for
            roughly two-thirds of per-capita emissions. In Denmark, Spain, and Portugal it exceeds half.
            At the other extreme, industry dominates in Slovakia and Czechia, where steel production,
            automotive manufacturing, and a heavy reliance on coal for heating, industry, and electricity
            generation push totals above 4 tCO&#x2082; per person. Residential emissions vary depending on
            climate, insulation standards, and the fuel mix for heating. Norway stands out with
            residential emissions near zero (0.08 tCO&#x2082;/cap), thanks to a grid that is 98%
            renewable (almost entirely hydropower), widespread use of heat pumps for heating, and
            the world's highest EV adoption rate, keeping its overall footprint remarkably low for
            a country with such a high standard of living.
          </p>
        </div>
      </div>

      <div class="chart-meta">
        <div class="meta-section">
          <span class="meta-label">Source</span>
          <ul>
            <li>
              <strong>IEA</strong>
              <a
                href="https://www.iea.org/data-and-statistics/data-product/energy-efficiency-indicators-highlights"
                target="_blank"
                rel="noopener"
              >
                Energy End-Uses &amp; Efficiency
              </a>
              (per-capita CO&#x2082; by sector). Indicator: <code>Carbon intensity per capita (t CO2/capita)</code>. End
              uses: <code>Total residential</code>, <code>Total services</code>, <code>Cars/light trucks</code> +
              <code>Freight trucks</code> (transport)
            </li>
            <li>
              Industry per-capita derived from IEA total emissions (indicator: <code>Total final use (kt CO2)</code>,
              end use containing <code>Manufacturing</code>) divided by
              <strong>OWID</strong>
              <a href="https://github.com/owid/energy-data" target="_blank" rel="noopener"> Energy Data </a>
              <code>population</code> column. IEA provides per-capita indicators for residential, services, and
              transport, but only per-value-added (gCO&#x2082;/USD) for industry.
            </li>
          </ul>
        </div>
        <div class="meta-section">
          <span class="meta-label">Data Hints</span>
          <ul>
            <li>Some countries may lack transport data. The total shown is the sum of available sectors.</li>
          </ul>
        </div>
      </div>

      <div class="chart-meta">
        <div class="meta-section">
          <span class="meta-label">Source</span>
          <ul>
            <li>
              <strong>IEA</strong>
              <a
                href="https://www.iea.org/data-and-statistics/data-product/energy-efficiency-indicators-highlights"
                target="_blank"
                rel="noopener"
              >
                Energy End-Uses &amp; Efficiency
              </a>
              (per-capita CO&#x2082; by sector). Indicator: <code>Carbon intensity per capita (t CO2/capita)</code>. End
              uses: <code>Total residential</code>, <code>Total services</code>, <code>Cars/light trucks</code> +
              <code>Freight trucks</code> (transport)
            </li>
            <li>
              Industry per-capita derived from IEA total emissions (indicator: <code>Total final use (kt CO2)</code>,
              end use containing <code>Manufacturing</code>) divided by
              <strong>OWID</strong>
              <a href="https://github.com/owid/energy-data" target="_blank" rel="noopener"> Energy Data </a>
              <code>population</code> column. IEA provides per-capita indicators for residential, services, and
              transport, but only per-value-added (gCO&#x2082;/USD) for industry.
            </li>
          </ul>
        </div>
        <div class="meta-section">
          <span class="meta-label">Data Hints</span>
          <ul>
            <li>Some countries may lack transport data. The total shown is the sum of available sectors.</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Subsection 2: Carbon Intensity -->
    <div class="eco-subsection">
      <h3>Carbon Intensity of the Energy Grid - Europe Comparison</h3>
      <p>
        Average CO2 emitted per kilowatt-hour of electricity generated from all sources, indicating how clean the power grid is in terms of emissions. Heavy reliance on nuclear 
        power contributes to low carbon intensity levels for electricity, as in the case of France for example, but referring to it as "clean energy" remains a topic of discussion. 
      </p>
      <div class="section-container">
        <div v-if="store.isLoading" class="loading">Loading energy data...</div>
        <div v-else-if="store.error" class="error">{{ store.error }}</div>
        <template v-else>
          <div v-if="!store.ecoLoaded" class="no-data">Eco data not available.</div>
          <div v-else class="charts-container">
            <div class="charts-fill">
              <CarbonIntensityRanking
                :rankingData="store.carbonIntensityRanking"
                :selectedCountryCode="store.selectedCountryCode"
              />
            </div>
          </div>
        </template>
        <div class="text-container">
          <h4 v-if="store.carbonIntensity?.latest_value != null">
            What does a carbon intensity of
            <span class="highlight-value">{{ Math.round(store.carbonIntensity.latest_value) }} gCO&#x2082;/kWh</span>
            for
            <span class="highlight-value">{{ store.selectedCountry?.name }}</span>
            mean in practice?
          </h4>
          <h4 v-else>What does your grid intensity mean in practice?</h4>
          <p>
            Most people are familiar with electrification as a fundamental part of decarbonization, 
            where processes directly reliant on fossil fuels, if they cannot be done without, are
            replaced by electric alternatives. The electric car being a prime example of this. A fact
            that can be lost in this though, is that any benefits in terms of emissions through often
            costly and disruptive switches, are only as beneficial as the electricity is clean. 
            The cards below (based on broad averages and approximations) demonstrate how impactful the effect can be,
            essentially highlighting the importance of electricity obtained from clean sources.
          </p>
          <StatCards :gridIntensity="store.carbonIntensity?.latest_value" />
          <details class="sources-details">
            <summary>Data sources and assumptions</summary>
            <ul class="sources-list">
              <li>
                <strong>Car, EV, Train &amp; Tram energy (MJ/pkm)</strong>:
                <a href="https://ptua.org.au/myths/energy/" target="_blank">PTUA – Myth: Public transport doesn't really save energy</a>.
                Total energy per passenger-km including vehicle manufacturing. Car (ICE): 3.0–4.4, EV: 1.2–2.0, Train: 0.05–0.2, Tram: 0.17–0.8 MJ/pkm. Ranges reflect occupancy assumptions (cars: 1.1–1.5 passengers; trains/trams: peak vs off-peak patronage).
              </li>
              <li>
                <strong>Heat pump SCOP (3.0)</strong>:
                <a href="https://www.iea.org/reports/the-future-of-heat-pumps" target="_blank"
                  >IEA The Future of Heat Pumps</a
                >, "How a heat pump works" section, opening paragraph states COP ~4. SCOP 3.0 is a conservative seasonal
                figure accounting for cold-climate performance drops.
              </li>
              <li>
                <strong>Gas heating (215 gCO&#x2082;/kWh_th)</strong>: Natural gas space heating. Based on emission factor ~205 gCO&#x2082;/kWh with typical boiler efficiency ~90%.
              </li>
              <li>
                <strong>Household electricity (3,600 kWh/yr)</strong>:
                <a href="https://www.odyssee-mure.eu/publications/efficiency-by-sector/households/electricity-consumption-dwelling.html" target="_blank">Odyssee-MURE – Electricity consumption per dwelling</a>.
                EU average of 3.6 MWh per dwelling, widely used as a median for medium-sized households. Varies greatly by country (from ~1.8 MWh in Romania to ~8.5 MWh in Sweden).
              </li>
              <li>
                <strong>Data center: NTT Frankfurt 1 (77.4 MW IT)</strong>:
                <a
                  href="https://services.global.ntt/en-us/services-and-products/global-data-centers/global-locations/emea/frankfurt-1-data-center"
                  target="_blank"
                  >NTT Frankfurt 1</a
                >, Overview section ("Secure and flexible space built to your specifications" paragraph) and
                Specifications > Power (70.1 MW operational + 7.3 MW under construction).
              </li>
              <li>
                <strong>Diesel truck (885 gCO&#x2082;/km)</strong>: Derived from 32.6 L/100 km (40t tractor-trailer, Long Haul cycle) x 2.68 kgCO&#x2082;/L.
                <a href="https://theicct.org/publication/lca-ghg-emissions-hdv-fuels-europe-feb23/" target="_blank">ICCT Feb 2023 LCA</a>, referencing the
                <a href="https://theicct.org/wp-content/uploads/2021/06/HDV_fuel-consumption_comparison_fs_20180418.pdf" target="_blank">ICCT April 2018 Fact Sheet</a>, average tractor-trailer fuel consumption figure.
              </li>
              <li>
                <strong>Electric truck (1.30 kWh/km)</strong>:
                <a
                  href="https://theicct.org/publication/rw-use-cases-for-zet-heavy-tractor-trailers-for-goods-transport-in-the-eu-aug25/"
                  target="_blank"
                  >ICCT Aug 2025</a
                >, Key Findings section: real-world range of 92 to 150 kWh/100 km for 40t tractor-trailers. 1.30 kWh/km
                (130 kWh/100 km) is within this range.
              </li>
              <li>
                <strong>PEM electrolysis (55 kWh/kgH&#x2082;)</strong>:
                <a
                  href="https://www.hydrogen.energy.gov/docs/hydrogenprogramlibraries/pdfs/24005-clean-hydrogen-production-cost-pem-electrolyzer.pdf"
                  target="_blank"
                  >DOE H2 Program Record #24005</a
                >
                (May 2024), main analysis section: beginning-of-life system electricity 55.2 kWh/kg (stack 51 +
                balance-of-plant 4.2). Lifetime average: 57.5 kWh/kg.
              </li>
              <li>
                <strong>Grey hydrogen SMR (9 kgCO&#x2082;/kgH&#x2082;)</strong>:
                <a href="https://www.iea.org/reports/global-hydrogen-review-2024" target="_blank"
                  >IEA Global Hydrogen Review 2024</a
                >, Ch. 8 "GHG emissions of hydrogen", Highlights, 1st bullet: unabated natural gas emits 10 to 12
                kgCO&#x2082;-eq/kgH&#x2082; (lifecycle). The value 9 represents direct combustion emissions only,
                excluding upstream methane.
              </li>
              <li>
                <strong>Blast furnace steel (2.2 tCO&#x2082;/t)</strong>:
                <a href="https://www.iea.org/energy-system/industry/steel" target="_blank">IEA Steel tracking page</a>,
                "Direct CO&#x2082; intensity of crude steel production" interactive chart. IEA reports ~2.0 to 2.3
                tCO&#x2082;/t for BF-BOF globally; 2.2 is within this range.
              </li>
              <li>
                <strong>EAF steel (400 kWh/t + 50 kgCO&#x2082;/t process)</strong>:
                <a href="https://www.iea.org/reports/iron-and-steel-technology-roadmap" target="_blank"
                  >IEA Iron &amp; Steel Roadmap</a
                >. Industry literature (AIST) commonly cites 300 to 400 kWh/t for scrap-based EAF electricity. The 50
                kgCO&#x2082;/t accounts for electrode and lime process emissions.
              </li>
            </ul>
          </details>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'
import { useEnergyDataStore } from '@/stores/energyData'
import EmissionsPerCapitaRanking from '../charts/EmissionsPerCapitaRanking.vue'
import EmissionsCloudPie from '../charts/EmissionsCloudPie.vue'
import CarbonIntensityRanking from '../charts/CarbonIntensityRanking.vue'
import StatCards from '../charts/StatCards.vue'

const store = useEnergyDataStore()

const totalEmissionsPerCapita = computed(() => {
  const epc = store.emissionsPerCapita
  if (!epc) return null
  const total = (epc.residential || 0) + (epc.services || 0)
              + (epc.transport || 0) + (epc.industry || 0)
  return total > 0 ? total.toFixed(1) : null
})
</script>

<style scoped>
.charts-fill {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.highlight-value {
  font-weight: 800;
  color: var(--text-color-dark-green, #2d3a0e);
  background: rgba(172, 194, 120, 0.25);
  padding: 0.05em 0.3em;
  border-radius: 4px;
}

.sources-details {
  margin-top: 1.25rem;
  color: var(--text-color-gray);
}

.sources-details summary {
  cursor: pointer;
  font-weight: 600;
  color: var(--text-color-gray);
  user-select: none;
}

.sources-details summary:hover {
  color: var(--text-color-basic);
}

.sources-list {
  margin: 0.5rem 0 0;
  padding-left: 1.25rem;
  line-height: 1.6;
}

.sources-list li {
  margin-bottom: 0.3rem;
}

.sources-list a {
  color: var(--text-color-gray);
  text-decoration: underline;
  text-decoration-style: dotted;
}

.sources-list a:hover {
  color: var(--text-color-basic);
}
</style>
