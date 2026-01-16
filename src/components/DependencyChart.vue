<template>
  <div class="dependency-chart">
    <div class="chart-header">
      <h4>Import Dependency by Energy Source</h4>
      <p class="chart-subtitle">Share of imports vs domestic production · <span class="chart-formula">(<em>Imports</em> − <em>Exports</em>) ÷ <em>Gross Available Energy</em></span></p>
    </div>

    <div v-if="!hasData" class="no-data">
      <span class="no-data-icon">?</span>
      <span>No dependency data available for this year</span>
    </div>

    <div v-else class="chart-wrapper">
      <div class="chart-container">
        <div ref="chartRef" class="chart-svg"></div>

        <!-- Electricity tooltip -->
        <div
          ref="tooltipRef"
          class="electricity-tooltip"
          :class="{ visible: tooltipVisible }"
        >
          <strong>Non-EU imports only.</strong> Eurostat doesn't calculate overall electricity dependency:
          <ul>
            <li><em>Origin:</em> Fuel dependency is counted at source (gas plant imports = gas dependency)</li>
            <li><em>Losses:</em> ~33% of energy lost converting to electricity makes tracking difficult</li>
            <li><em>Trade:</em> EU is near net-zero; grid constantly rebalances across borders</li>
            <li><em>Focus:</em> Eurostat measures primary fuels (oil, gas) not transformed energy</li>
            <li><em>Method:</em> Methodological complexities in how electricity trade interacts with primary fuels used to produce it</li>
          </ul>
        </div>

        <div class="chart-legend">
          <div class="legend-item">
            <span class="legend-color" style="background: #e8a87c;"></span>
            <span>Imports</span>
          </div>
          <div class="legend-item">
            <span class="legend-color" style="background: #81b29a;"></span>
            <span>Domestic</span>
          </div>
          <div class="legend-item">
            <span class="legend-color" style="background: #8b2500;"></span>
            <span>Reserve draw (&gt;100%)</span>
          </div>
          <div class="legend-item">
            <span class="legend-color" style="background: #7b68ee;"></span>
            <span>Net exporter (&lt;0%)</span>
          </div>
        </div>
        <div class="chart-notes">
          <p class="chart-note">
            <span class="note-icon">*</span>
            <span>Non-EU breakdown (hatched line) only available for main aggregates (Coal, Gas, Oil, Electricity). Subcategories (indented, lighter colors) show total import dependency only.</span>
          </p>
          <p class="chart-note" v-if="year === 2024 || year === '2024'">
            <span class="note-icon">*</span>
            <span>2024: Non-EU data not yet published by Eurostat.</span>
          </p>
          <p class="chart-note">
            <span class="note-icon electricity-mark">!</span>
            <span>Electricity: Eurostat does not calculate overall import dependency; showing non-EU imports only.</span>
          </p>
        </div>
      </div>

      <div class="chart-info">
        <!-- Electricity -->
        <div class="fuel-group">
          <div class="fuel-group-title">Electricity</div>
          <div class="fuel-group-content">
            <img :src="`${baseUrl}images/fuel-electricity.svg`" alt="Electricity" class="fuel-img-large" />
            <p class="fuel-text">
              Most versatile energy carrier for lighting, appliances, industry, and increasingly transport. Cannot be stored at scale, requiring real-time grid balancing. Non-EU dependency varies by geography (2022): Moldova (68%), Georgia (30%), Lithuania (25%) rely on non-EU sources; Western Europe imports almost exclusively from EU neighbors (Germany 6%, France 2%, non-EU). France is typically a net exporter thanks to its nuclear fleet.
            </p>
          </div>
        </div>

        <!-- Oil -->
        <div class="fuel-group">
          <div class="fuel-group-title">Oil &amp; Petroleum</div>
          <div class="fuel-group-content">
            <img :src="`${baseUrl}images/fuel-oil.svg`" alt="Oil" class="fuel-img-large" />
            <div class="fuel-text-wrapper">
              <p class="fuel-text">
                World's largest primary energy source (~30% of global consumption). Backbone of transportation and petrochemical feedstock. High energy density (45 MJ/kg). Nearly all European countries import 90%+ (2022): Germany (97%), France (99%), Italy (93%). Norway is a major net exporter. Non-EU dependency typically 75-90% across the EU (2022).
              </p>
            </div>
          </div>
          <div class="fuel-subresources">
            <div class="fuel-subresource">
              <img :src="`${baseUrl}images/fuel-crude-oil.svg`" alt="Crude Oil" class="fuel-img-small" />
              <div class="subresource-content">
                <span class="subresource-name">Crude Oil</span>
                <span class="subresource-desc">Unrefined petroleum sent to refineries for gasoline, diesel, jet fuel. Quality varies by sulfur (sweet/sour) and density (light/heavy). ~98% imported in most EU countries (2022).</span>
              </div>
            </div>
            <div class="fuel-subresource">
              <img :src="`${baseUrl}images/fuel-ngl.svg`" alt="NGL" class="fuel-img-small" />
              <div class="subresource-content">
                <span class="subresource-name">NGL</span>
                <span class="subresource-desc">Natural Gas Liquids (propane, butane, ethane). Extracted during gas processing. Typically 0% import dependency (2022) as they're separated domestically from imported gas.</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Gas -->
        <div class="fuel-group">
          <div class="fuel-group-title">Natural Gas</div>
          <div class="fuel-group-content">
            <img :src="`${baseUrl}images/fuel-gas.svg`" alt="Gas" class="fuel-img-large" />
            <p class="fuel-text">
              Primarily methane (CH₄). Burns 50% cleaner than coal. Critical for heating, electricity, and fertilizer production. Transported via pipelines or LNG tankers. Dependency above 100% indicates reserve drawdowns, observed during the 2022 energy crisis (Germany 106%, France 109%). In 2022: Netherlands (65%) has domestic production; Poland (78%) diversified via Baltic LNG. Norway is Europe's largest non-Russian supplier.
            </p>
          </div>
        </div>

        <!-- Coal -->
        <div class="fuel-group">
          <div class="fuel-group-title">Coal</div>
          <div class="fuel-group-content">
            <img :src="`${baseUrl}images/fuel-coal.svg`" alt="Coal" class="fuel-img-large" />
            <p class="fuel-text">
              Most carbon-intensive fossil fuel. Ranked by age: lignite → sub-bituminous → bituminous → anthracite. Still important for power and steel. Import dependency (2022): Germany ~50%; Poland (8%) and Czechia (14%) rely on domestic production. Values above 100% indicate stock usage. Being phased out across Europe due to climate commitments.
            </p>
          </div>
          <div class="fuel-subresources">
            <div class="fuel-subresource">
              <img :src="`${baseUrl}images/fuel-anthracite.svg`" alt="Anthracite" class="fuel-img-small" />
              <div class="subresource-content">
                <span class="subresource-name">Anthracite</span>
                <span class="subresource-desc">Highest grade (86-97% carbon, 30-35 MJ/kg). Burns hot and clean. Geologically rare. Most countries import 100% (2022), but Poland (79%), Slovakia (56%), and Czechia (96%) retain some domestic production.</span>
              </div>
            </div>
            <div class="fuel-subresource">
              <img :src="`${baseUrl}images/fuel-coking-coal.svg`" alt="Coking Coal" class="fuel-img-small" />
              <div class="subresource-content">
                <span class="subresource-name">Coking Coal</span>
                <span class="subresource-desc">Essential for blast furnace steel production. Must have low ash/sulfur. ~100% imported in most EU countries (2022) from Australia, USA, Canada.</span>
              </div>
            </div>
            <div class="fuel-subresource">
              <img :src="`${baseUrl}images/fuel-bituminous.svg`" alt="Other Bituminous" class="fuel-img-small" />
              <div class="subresource-content">
                <span class="subresource-name">Other Bituminous</span>
                <span class="subresource-desc">Steam coal for power plants (45-86% carbon, 24-35 MJ/kg). Highest trade volume. Poland/Czechia have domestic reserves.</span>
              </div>
            </div>
            <div class="fuel-subresource">
              <img :src="`${baseUrl}images/fuel-sub-bituminous.svg`" alt="Sub-bituminous" class="fuel-img-small" />
              <div class="subresource-content">
                <span class="subresource-name">Sub-bituminous</span>
                <span class="subresource-desc">Grade between lignite and bituminous (35-45% carbon, 17-23 MJ/kg). Used mainly for power generation. Limited trade in Europe; most countries show 0% or no data (2013-2022).</span>
              </div>
            </div>
            <div class="fuel-subresource">
              <img :src="`${baseUrl}images/fuel-lignite.svg`" alt="Lignite" class="fuel-img-small" />
              <div class="subresource-content">
                <span class="subresource-name">Lignite</span>
                <span class="subresource-desc">Brown coal (25-35% carbon, up to 75% moisture). Rarely traded due to low energy density and crumbling when dried. Usually 0% import (2022), but Austria (100%), Slovenia, Hungary, and Lithuania import from neighbors. Germany is Europe's largest producer.</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Peat -->
        <div class="fuel-group">
          <div class="fuel-group-title">Peat</div>
          <div class="fuel-group-content">
            <img :src="`${baseUrl}images/fuel-peat.svg`" alt="Peat" class="fuel-img-large" />
            <p class="fuel-text">
              Partially decomposed organic matter from bogs. Lowest energy density (8-12 MJ/kg). Pre-coal stage fuel used historically in northern Europe for heating and power. Almost always sourced locally (0% import dependency, 2023) due to low energy density. Finland is the exception (~1%). Being phased out due to CO₂ emissions and ecosystem destruction. Most countries show no peat data.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import * as d3 from 'd3'

const baseUrl = import.meta.env.BASE_URL

const props = defineProps({
  dependencyData: {
    type: Object,
    default: null
  },
  year: {
    type: [String, Number],
    default: null
  }
})

const chartRef = ref(null)
const tooltipRef = ref(null)
const tooltipVisible = ref(false)
let resizeObserver = null

function showElectricityTooltip(event, svgX, svgY) {
  tooltipVisible.value = true
  if (tooltipRef.value && chartRef.value) {
    const chartRect = chartRef.value.getBoundingClientRect()
    const tooltip = tooltipRef.value
    // Position tooltip near the warning icon
    tooltip.style.left = `${svgX + 120}px`  // Account for left margin
    tooltip.style.top = `${svgY - 10}px`
  }
}

function hideElectricityTooltip() {
  tooltipVisible.value = false
}

// Fuel type display names mapping
const fuelDisplayNames = {
  coal: 'Coal',
  anthracite: 'Anthracite',
  coking_coal: 'Coking Coal',
  other_bituminous: 'Other Bituminous',
  other_bituminous_coal: 'Other Bituminous',
  lignite: 'Lignite',
  sub_bituminous_coal: 'Sub-bituminous',
  gas: 'Natural Gas',
  natural_gas: 'Natural Gas',
  oil: 'Oil',
  crude_oil: 'Crude Oil',
  ngl: 'NGL',
  peat: 'Peat',
  nuclear_fuels: 'Nuclear',
  renewable_fuels: 'Renewables',
  electricity: 'Electricity',
  // Fallback for SIEC codes
  C0110: 'Anthracite',
  C0121: 'Coking Coal',
  C0129: 'Other Bituminous',
  C0210: 'Lignite',
  C0220: 'Sub-bituminous',
  G3000: 'Natural Gas',
  O4000XBIO: 'Oil',
  O4100_TOT: 'Crude Oil',
  O4200: 'NGL',
  P1100: 'Oil Shale',
  S2000: 'Nuclear',
  CF_R: 'Renewables',
  E7000: 'Electricity',
  SFF_OTH: 'Other Solid Fuels'
}

// Priority order for display - matches text sections order
const fuelPriority = [
  // Electricity
  'electricity', 'E7000',
  // Oil & Petroleum group
  'oil', 'O4000XBIO',
  'crude_oil', 'O4100_TOT',
  'ngl', 'O4200',
  // Natural Gas
  'gas', 'natural_gas', 'G3000',
  // Coal group
  'coal', 'C0000X0350-0370',
  'anthracite', 'C0110',
  'coking_coal', 'C0121',
  'other_bituminous', 'other_bituminous_coal', 'C0129',
  'sub_bituminous_coal', 'C0220',
  'lignite', 'C0210',
  // Peat
  'peat', 'P1100'
]

// Fuels to exclude from display
const excludedFuels = ['nuclear_fuels', 'S2000', 'renewable_fuels', 'CF_R', 'SFF_OTH', 'other_solid_fossil_fuels']

// Subcategories that don't have third_countries data from Eurostat
// These will be visually offset and have softer colors
const subcategoriesNoThirdCountries = [
  'crude_oil', 'O4100_TOT',
  'ngl', 'O4200',
  'anthracite', 'C0110',
  'coking_coal', 'C0121',
  'other_bituminous_coal', 'other_bituminous', 'C0129',
  'sub_bituminous_coal', 'C0220',
  'lignite', 'C0210'
]

// Special case: electricity has third_countries but no overall
const electricityKeys = ['electricity', 'E7000']

// Define fuel groups for spacing - first item in each group gets extra top margin
const fuelGroups = {
  electricity: ['electricity', 'E7000'],
  oil: ['oil', 'O4000XBIO', 'crude_oil', 'O4100_TOT', 'ngl', 'O4200'],
  gas: ['gas', 'natural_gas', 'G3000'],
  coal: ['coal', 'C0000X0350-0370', 'anthracite', 'C0110', 'coking_coal', 'C0121',
         'other_bituminous', 'other_bituminous_coal', 'C0129', 'sub_bituminous_coal', 'C0220', 'lignite', 'C0210'],
  peat: ['peat', 'P1100']
}

// First fuel of each group (excluding electricity which is always first)
const groupStarters = ['oil', 'O4000XBIO', 'gas', 'natural_gas', 'G3000', 'coal', 'C0000X0350-0370', 'peat', 'P1100']

const hasData = computed(() => {
  return props.dependencyData &&
    (props.dependencyData.overall != null ||
     (props.dependencyData.by_fuel && Object.keys(props.dependencyData.by_fuel).length > 0))
})

const chartData = computed(() => {
  if (!props.dependencyData) return []

  const data = []

  // Add overall dependency first
  data.push({
    key: 'overall',
    name: 'Overall',
    overall: props.dependencyData.overall,
    thirdCountries: props.dependencyData.third_countries,
    isOverall: true
  })

  // Add by_fuel breakdown
  if (props.dependencyData.by_fuel) {
    const fuels = Object.entries(props.dependencyData.by_fuel)

    // Sort by priority, then alphabetically
    fuels.sort((a, b) => {
      const aPriority = fuelPriority.indexOf(a[0])
      const bPriority = fuelPriority.indexOf(b[0])

      if (aPriority !== -1 && bPriority !== -1) return aPriority - bPriority
      if (aPriority !== -1) return -1
      if (bPriority !== -1) return 1

      return (fuelDisplayNames[a[0]] || a[0]).localeCompare(fuelDisplayNames[b[0]] || b[0])
    })

    for (const [key, value] of fuels) {
      if (!value || typeof value !== 'object') continue
      if (excludedFuels.includes(key)) continue

      data.push({
        key,
        name: fuelDisplayNames[key] || formatKey(key),
        overall: value.overall,
        thirdCountries: value.third_countries,
        isOverall: false,
        isSubcategory: subcategoriesNoThirdCountries.includes(key),
        isElectricity: electricityKeys.includes(key),
        isGroupStarter: groupStarters.includes(key)
      })
    }
  }

  return data
})

function formatKey(key) {
  return key
    .replace(/_/g, ' ')
    .replace(/([A-Z])/g, ' $1')
    .split(' ')
    .map(w => w.charAt(0).toUpperCase() + w.slice(1).toLowerCase())
    .join(' ')
    .trim()
}

function renderChart() {
  if (!chartRef.value || chartData.value.length === 0) return

  // Clear previous chart
  d3.select(chartRef.value).selectAll('*').remove()

  const container = chartRef.value
  const containerWidth = container.clientWidth || 600

  const barHeight = 20
  const barGap = 4
  const numBars = chartData.value.length
  const maxWidth = Math.min(containerWidth, 500)
  const margin = { top: 20, right: 45, bottom: 10, left: 100 }
  const width = maxWidth - margin.left - margin.right
  const height = numBars * (barHeight + barGap)
  const subcategoryOffset = 45 // Pixels to offset subcategory bars from the left

  const svg = d3.select(chartRef.value)
    .append('svg')
    .attr('width', maxWidth)
    .attr('height', height + margin.top + margin.bottom)
    .append('g')
    .attr('transform', `translate(${margin.left},${margin.top})`)

  // Calculate maximum value for dynamic scale
  const maxOverall = Math.max(100, ...chartData.value.map(d => d.overall ?? 0))
  const scaleMax = Math.ceil(maxOverall / 10) * 10 // Round up to nearest 10

  // Scales
  const x = d3.scaleLinear()
    .domain([0, scaleMax])
    .range([0, width])

  const y = d3.scaleBand()
    .domain(chartData.value.map(d => d.name))
    .range([0, height])
    .padding(0.2)

  // Draw 100% reference line if scale exceeds 100
  if (scaleMax > 100) {
    svg.append('line')
      .attr('x1', x(100))
      .attr('x2', x(100))
      .attr('y1', 0)
      .attr('y2', height)
      .attr('stroke', '#666')
      .attr('stroke-width', 1)
      .attr('stroke-dasharray', '4,2')

    svg.append('text')
      .attr('x', x(100))
      .attr('y', -4)
      .attr('text-anchor', 'middle')
      .attr('fill', '#666')
      .attr('font-size', '9px')
      .text('100%')
  }

  // Color definitions - normal and softened versions for subcategories
  const colors = {
    third: { normal: '#c44536', soft: '#d4847a' },
    eu: { normal: '#e8a87c', soft: '#f0c9b0' },
    domestic: { normal: '#81b29a', soft: '#aed0be' },
    reserve: { normal: '#8b2500', soft: '#b86347' },
    reserveEu: { normal: '#b86b3a', soft: '#d4a07a' },
    exporter: { normal: '#7b68ee', soft: '#a99cf3' }
  }

  // Define crosshatch pattern for non-EU marker
  const defs = svg.append('defs')
  defs.append('pattern')
    .attr('id', 'crosshatch')
    .attr('width', 4)
    .attr('height', 4)
    .attr('patternUnits', 'userSpaceOnUse')
    .attr('patternTransform', 'rotate(45)')
    .append('line')
    .attr('x1', 0)
    .attr('y1', 0)
    .attr('x2', 0)
    .attr('y2', 4)
    .attr('stroke', '#c44536')
    .attr('stroke-width', 2)

  // Draw horizontal bars for each fuel type
  chartData.value.forEach(d => {
    const yPos = y(d.name)
    const barH = y.bandwidth()
    const isSubcat = d.isSubcategory
    const barOffset = isSubcat ? subcategoryOffset : 0

    // Get appropriate colors based on whether this is a subcategory
    const getColor = (colorKey) => isSubcat ? colors[colorKey].soft : colors[colorKey].normal

    // For electricity, use third_countries as the overall value
    const effectiveOverall = d.isElectricity && d.overall == null && d.thirdCountries != null
      ? d.thirdCountries
      : d.overall

    if (effectiveOverall != null) {
      const rawOverall = effectiveOverall
      const isNetExporter = rawOverall < 0
      const overallPct = Math.max(0, rawOverall)
      const thirdCountriesPct = d.thirdCountries != null ? Math.max(0, d.thirdCountries) : null

      if (isNetExporter) {
        // Net exporter: show full bar in purple
        svg.append('rect')
          .attr('class', 'bar-exporter')
          .attr('x', barOffset)
          .attr('y', yPos)
          .attr('width', x(100) - barOffset)
          .attr('height', barH)
          .attr('fill', getColor('exporter'))

        // Label inside bar showing "Net Exporter"
        svg.append('text')
          .attr('x', barOffset + (x(100) - barOffset) / 2)
          .attr('y', yPos + barH / 2)
          .attr('dy', '0.35em')
          .attr('text-anchor', 'middle')
          .attr('fill', '#fff')
          .attr('font-size', '9px')
          .attr('font-weight', '600')
          .text('Net Exporter')

        // Label showing negative percentage at end
        svg.append('text')
          .attr('x', x(100) + 4)
          .attr('y', yPos + barH / 2)
          .attr('dy', '0.35em')
          .attr('text-anchor', 'start')
          .attr('fill', isSubcat ? '#8a7fd4' : '#5a4fcf')
          .attr('font-size', '9px')
          .attr('font-weight', '700')
          .text(`${rawOverall.toFixed(0)}%`)
      } else {
        // Normal case: import dependency >= 0
        // Domestic only exists when overall is below 100%
        const domesticPct = overallPct < 100 ? 100 - overallPct : 0
        // Reserve draw (imports exceeding consumption) when overall > 100%
        const reserveDrawPct = overallPct > 100 ? overallPct - 100 : 0

        // Draw import portion as a single bar (up to 100%)
        if (overallPct > 0) {
          const importBelow100 = Math.min(overallPct, 100)
          const importWidth = x(importBelow100) - barOffset
          svg.append('rect')
            .attr('class', 'bar-import')
            .attr('x', barOffset)
            .attr('y', yPos)
            .attr('width', importWidth)
            .attr('height', barH)
            .attr('fill', getColor('eu'))
        }

        // Portion above 100% (reserve draw)
        if (reserveDrawPct > 0) {
          const reserveWidth = x(overallPct) - x(100)
          svg.append('rect')
            .attr('class', 'bar-reserve')
            .attr('x', x(100))
            .attr('y', yPos)
            .attr('width', reserveWidth)
            .attr('height', barH)
            .attr('fill', getColor('reserve'))
            .attr('opacity', 0.85)
        }

        // Domestic portion (right, green) - only if below 100%
        if (domesticPct > 0) {
          // For subcategories with 0% imports, domestic starts at offset
          const domesticStartX = Math.max(barOffset, x(overallPct))
          const domesticWidth = x(100) - domesticStartX
          svg.append('rect')
            .attr('class', 'bar-domestic')
            .attr('x', domesticStartX)
            .attr('y', yPos)
            .attr('width', domesticWidth)
            .attr('height', barH)
            .attr('fill', getColor('domestic'))
        }

        // Add non-EU crosshatch overlay on left portion of bar if third_countries data exists
        // (but not for electricity since we're using third_countries as the overall)
        if (thirdCountriesPct != null && thirdCountriesPct > 0 && !d.isElectricity && !isSubcat) {
          const nonEuWidth = x(thirdCountriesPct) - barOffset

          // Overlay crosshatch pattern on the non-EU portion (left side of bar)
          if (nonEuWidth > 0) {
            svg.append('rect')
              .attr('x', barOffset)
              .attr('y', yPos)
              .attr('width', nonEuWidth)
              .attr('height', barH)
              .attr('fill', 'url(#crosshatch)')
              .attr('opacity', 0.4)

            // Add vertical line at the boundary between non-EU and EU
            svg.append('line')
              .attr('x1', x(thirdCountriesPct))
              .attr('y1', yPos)
              .attr('x2', x(thirdCountriesPct))
              .attr('y2', yPos + barH)
              .attr('stroke', '#8b2500')
              .attr('stroke-width', 2)

            // Add "non-EU" label inside the crosshatched area if wide enough
            if (nonEuWidth >= 35) {
              svg.append('text')
                .attr('x', barOffset + nonEuWidth / 2)
                .attr('y', yPos + barH / 2)
                .attr('dy', '0.35em')
                .attr('text-anchor', 'middle')
                .attr('fill', '#8b2500')
                .attr('font-size', '7px')
                .attr('font-weight', '700')
                .text('non-EU')
            }
          }
        }

        // Labels showing actual percentage at end of bar
        const labelX = x(Math.max(overallPct, domesticPct > 0 ? 100 : overallPct)) + 4
        const pctLabel = svg.append('text')
          .attr('x', labelX)
          .attr('y', yPos + barH / 2)
          .attr('dy', '0.35em')
          .attr('text-anchor', 'start')
          .attr('fill', overallPct > 100 ? (isSubcat ? '#b86347' : '#8b2500') : '#666')
          .attr('font-size', '9px')
          .attr('font-weight', overallPct > 100 ? '700' : '500')
          .text(`${overallPct.toFixed(0)}%`)

        // Add red circle with exclamation mark after percentage for electricity
        if (d.isElectricity) {
          const pctWidth = pctLabel.node().getBBox().width
          const warningX = labelX + pctWidth + 10

          // Group for hover effect
          const warningGroup = svg.append('g')
            .attr('class', 'electricity-warning-group')
            .style('cursor', 'help')

          // Red circle background
          warningGroup.append('circle')
            .attr('cx', warningX)
            .attr('cy', yPos + barH / 2)
            .attr('r', 6)
            .attr('fill', '#c44536')

          // White exclamation mark
          warningGroup.append('text')
            .attr('x', warningX)
            .attr('y', yPos + barH / 2)
            .attr('dy', '0.35em')
            .attr('text-anchor', 'middle')
            .attr('fill', '#fff')
            .attr('font-size', '9px')
            .attr('font-weight', '700')
            .style('pointer-events', 'none')
            .text('!')

          // Invisible larger circle for easier hover target
          warningGroup.append('circle')
            .attr('cx', warningX)
            .attr('cy', yPos + barH / 2)
            .attr('r', 10)
            .attr('fill', 'transparent')
            .on('mouseenter', function(event) {
              showElectricityTooltip(event, warningX, yPos)
            })
            .on('mouseleave', hideElectricityTooltip)
        }
      }
    } else {
      // No data - grey bar (stops at 100% mark)
      svg.append('rect')
        .attr('class', 'bar-nodata')
        .attr('x', barOffset)
        .attr('y', yPos)
        .attr('width', x(100) - barOffset)
        .attr('height', barH)
        .attr('fill', isSubcat ? '#f0f0f0' : '#e8e8e8')
        .attr('rx', 3)

      svg.append('text')
        .attr('class', 'no-data-label')
        .attr('x', barOffset + (x(100) - barOffset) / 2)
        .attr('y', yPos + barH / 2)
        .attr('dy', '0.35em')
        .attr('text-anchor', 'middle')
        .attr('fill', '#999')
        .attr('font-size', '10px')
        .text('No data')

      // Add electricity warning even for no-data case
      if (d.isElectricity) {
        const warningX = x(100) + 14

        const warningGroup = svg.append('g')
          .attr('class', 'electricity-warning-group')
          .style('cursor', 'help')

        warningGroup.append('circle')
          .attr('cx', warningX)
          .attr('cy', yPos + barH / 2)
          .attr('r', 6)
          .attr('fill', '#c44536')

        warningGroup.append('text')
          .attr('x', warningX)
          .attr('y', yPos + barH / 2)
          .attr('dy', '0.35em')
          .attr('text-anchor', 'middle')
          .attr('fill', '#fff')
          .attr('font-size', '9px')
          .attr('font-weight', '700')
          .style('pointer-events', 'none')
          .text('!')

        warningGroup.append('circle')
          .attr('cx', warningX)
          .attr('cy', yPos + barH / 2)
          .attr('r', 10)
          .attr('fill', 'transparent')
          .on('mouseenter', function(event) {
            showElectricityTooltip(event, warningX, yPos)
          })
          .on('mouseleave', hideElectricityTooltip)
      }
    }

  })

  // Y axis (fuel type labels) - with offset for subcategories
  const yAxis = svg.append('g')
    .call(d3.axisLeft(y))

  // Get subcategory display names for matching
  const subcatDisplayNames = subcategoriesNoThirdCountries.map(key => fuelDisplayNames[key] || formatKey(key))

  yAxis.selectAll('.tick')
    .each(function(d) {
      const isSubcat = subcatDisplayNames.includes(d)
      const text = d3.select(this).select('text')
      text
        .attr('fill', isSubcat ? '#666' : '#333')
        .attr('font-size', '11px')
        .attr('font-style', isSubcat ? 'italic' : 'normal')
      if (isSubcat) {
        // Offset the entire tick group to the right
        d3.select(this).attr('transform', function() {
          const currentTransform = d3.select(this).attr('transform') || ''
          const match = currentTransform.match(/translate\(([^,]*),([^)]*)\)/)
          if (match) {
            return `translate(${parseFloat(match[1]) + 45},${match[2]})`
          }
          return currentTransform
        })
      }
    })

  svg.selectAll('.domain').remove()
  svg.selectAll('.tick line').remove()
}

watch(() => [props.dependencyData, props.year], () => {
  renderChart()
}, { deep: true })

onMounted(() => {
  renderChart()

  resizeObserver = new ResizeObserver(() => {
    renderChart()
  })

  if (chartRef.value) {
    resizeObserver.observe(chartRef.value)
  }
})

onUnmounted(() => {
  if (resizeObserver) {
    resizeObserver.disconnect()
  }
})
</script>

<style scoped>
.dependency-chart {
  background: #fff;
  border-radius: 8px;
  padding: 1.5rem;
  border: 1px solid #e8e8e8;
}

.chart-header {
  margin-bottom: 1rem;
}

.chart-header h4 {
  margin: 0 0 0.25rem 0;
  color: #333;
  font-size: 1rem;
}

.chart-subtitle {
  margin: 0;
  color: #666;
  font-size: 0.85rem;
}

.chart-formula {
  color: #777;
  font-family: 'Times New Roman', 'Georgia', serif;
  font-style: italic;
}

.chart-formula em {
  font-style: italic;
  letter-spacing: 0.02em;
}

.no-data {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 3rem;
  color: #999;
  background: #f8f8f8;
  border-radius: 6px;
}

.no-data-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  background: #e0e0e0;
  border-radius: 50%;
  font-weight: bold;
  font-size: 14px;
}

.chart-wrapper {
  display: flex;
  gap: 2.5rem;
  align-items: flex-start;
  width: 100%;
}

.chart-container {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  width: 45%;
  min-width: 350px;
  max-width: 500px;
  flex-shrink: 0;
}

.chart-svg :deep(svg) {
  display: block;
}

.electricity-tooltip {
  position: absolute;
  background: #fff;
  border: 1px solid #c44536;
  border-radius: 6px;
  padding: 0.5rem 0.75rem;
  width: 400px;
  font-size: 0.72rem;
  line-height: 1.4;
  color: #555;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  z-index: 100;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.15s, visibility 0.15s;
  pointer-events: none;
}

.electricity-tooltip.visible {
  opacity: 1;
  visibility: visible;
}

.electricity-tooltip strong {
  color: #c44536;
}

.electricity-tooltip ul {
  margin: 0.3rem 0 0 0;
  padding-left: 1.1rem;
}

.electricity-tooltip li {
  margin-bottom: 0.15rem;
}

.electricity-tooltip li:last-child {
  margin-bottom: 0;
}

.electricity-tooltip em {
  color: #333;
  font-style: normal;
  font-weight: 600;
}

.chart-legend {
  display: flex;
  gap: 1.5rem;
  justify-content: flex-start;
  flex-wrap: wrap;
  padding-left: 100px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.8rem;
  color: #666;
}

.legend-color {
  width: 14px;
  height: 14px;
  border-radius: 3px;
}

.chart-notes {
  margin-top: 0.75rem;
  padding-left: 100px;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.chart-note {
  display: flex;
  align-items: flex-start;
  gap: 0.35rem;
  margin: 0;
  font-size: 0.7rem;
  color: #777;
  line-height: 1.4;
}

.note-icon {
  flex-shrink: 0;
  font-weight: 600;
  color: #999;
}

.note-icon.electricity-mark {
  color: #c44536;
  font-weight: 700;
}

.chart-info {
  flex: 1;
  min-width: 0;
  font-size: 0.8rem;
  line-height: 1.5;
}

.fuel-group {
  margin-bottom: 0.6rem;
  padding-bottom: 0.6rem;
  border-bottom: 1px solid #eee;
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
  width: 36px;
  height: 36px;
  object-fit: contain;
  background: #f5f5f5;
  border-radius: 4px;
  padding: 4px;
  flex-shrink: 0;
}

.fuel-text {
  margin: 0;
  color: #555;
  font-size: 0.8rem;
  line-height: 1.5;
}

.fuel-text strong {
  color: #333;
}

.fuel-subresources {
  margin-top: 0.4rem;
  margin-left: 42px;
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
  width: 20px;
  height: 20px;
  object-fit: contain;
  background: #f8f8f8;
  border-radius: 3px;
  padding: 2px;
  flex-shrink: 0;
}

.subresource-content {
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem;
  align-items: baseline;
}

.subresource-name {
  font-weight: 600;
  font-size: 0.75rem;
  color: #333;
}

.subresource-name::after {
  content: ":";
  font-weight: 400;
  color: #999;
}

.subresource-desc {
  font-size: 0.75rem;
  line-height: 1.45;
  color: #666;
}
</style>
