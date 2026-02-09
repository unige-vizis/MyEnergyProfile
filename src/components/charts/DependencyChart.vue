<template>
  <div v-if="!hasData" class="no-data">
    <span class="no-data-icon">?</span>
    <span>No dependency data available for this year</span>
  </div>

  <div v-else class="chart-wrapper">
    <div class="chart-container">
      <div class="chart-heading">
        <div class="formula-stack">
          <code class="formula" :style="upperCellStyle">Production + Imports − Exports ± Stock Changes</code>
          <svg class="curly-brace" :style="upperBraceStyle" viewBox="0 0 100 12" preserveAspectRatio="none">
            <path
              d="M 0,12 Q 0,5 10,5 L 44,5 Q 50,5 50,0 Q 50,5 56,5 L 90,5 Q 100,5 100,12"
              fill="none"
              stroke="var(--text-color-gray, #666)"
              stroke-width="1.5"
            />
          </svg>
          <code class="formula" :style="lowerCellStyle">(Imports − Exports) / Gross Available Energy</code>
          <svg class="curly-brace" :style="lowerBraceStyle" viewBox="0 0 100 12" preserveAspectRatio="none">
            <path
              d="M 0,12 Q 0,5 10,5 L 44,5 Q 50,5 50,0 Q 50,5 56,5 L 90,5 Q 100,5 100,12"
              fill="none"
              stroke="var(--text-color-gray, #666)"
              stroke-width="1.5"
            />
          </svg>
        </div>
        <h3 v-if="countryName">
          <span ref="countryNameRef">{{ countryName }}</span
          >'s <span class="highlight-import">Import Dependency</span> as Percentage by Fuel Type (<a
            class="heading-link"
            href="https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Glossary:Energy_dependency_rate"
            target="_blank"
            rel="noopener"
            >Eurostat methodology</a
          >)
        </h3>
        <h3 v-else>
          <span class="highlight-import">Import Dependency</span> by Fuel Type (<a
            class="heading-link"
            href="https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Glossary:Energy_dependency_rate"
            target="_blank"
            rel="noopener"
            >Eurostat methodology</a
          >)
        </h3>
      </div>
      <div ref="chartRef" class="chart-svg"></div>

      <!-- Electricity tooltip -->
      <div ref="tooltipRef" class="electricity-tooltip" :class="{ visible: tooltipVisible }">
        <strong>Non-EU imports only.</strong> Eurostat doesn't calculate overall electricity dependency:
        <ul>
          <li><em>Origin:</em> Fuel dependency is counted at source (gas plant imports = gas dependency)</li>
          <li><em>Losses:</em> ~33% of energy lost converting to electricity makes tracking difficult</li>
          <li><em>Trade:</em> EU is near net-zero; grid constantly rebalances across borders</li>
          <li><em>Focus:</em> Eurostat measures primary fuels (oil, gas) not transformed energy</li>
          <li>
            <em>Method:</em> Methodological complexities in how electricity trade interacts with primary fuels used to
            produce it
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import * as d3 from 'd3'

// ─── Formula diagram positioning config ───
// All offsets are px from the left container border.
// countryNameWidth is measured automatically and added to each leftOffset.
const formulaConfig = reactive({
  lowerBrace:  { width: 170, leftOffset: 20, yOffset: 0 },  // bracket above title
  upperBrace:  { width: 150, leftOffset: 120, yOffset: 0 },  // bracket above lower cell
  lowerCell:   { leftOffset: -50, yOffset: 0 },               // "(Imports − Exports) / GAE"
  upperCell:   { leftOffset: 20, yOffset: 0 },               // "Production + Imports − ..."
})

const props = defineProps({
  dependencyData: {
    type: Object,
    default: null
  },
  year: {
    type: [String, Number],
    default: null
  },
  countryName: {
    type: String,
    default: ''
  }
})

const chartRef = ref(null)
const tooltipRef = ref(null)
const tooltipVisible = ref(false)
const countryNameRef = ref(null)
const countryNameWidth = ref(0)
let resizeObserver = null

function measureCountryName() {
  countryNameWidth.value = countryNameRef.value?.offsetWidth ?? 0
}

// Computed inline styles for brackets and cells
// marginLeft = countryNameWidth + fixed leftOffset (px from container left)
const lowerBraceStyle = computed(() => ({
  width: `${formulaConfig.lowerBrace.width}px`,
  marginLeft: `${countryNameWidth.value + formulaConfig.lowerBrace.leftOffset}px`,
  transform: `translateY(${formulaConfig.lowerBrace.yOffset}px)`,
}))

const upperBraceStyle = computed(() => ({
  width: `${formulaConfig.upperBrace.width}px`,
  marginLeft: `${countryNameWidth.value + formulaConfig.upperBrace.leftOffset}px`,
  transform: `translateY(${formulaConfig.upperBrace.yOffset}px)`,
}))

const lowerCellStyle = computed(() => ({
  marginLeft: `${countryNameWidth.value + formulaConfig.lowerCell.leftOffset}px`,
  transform: `translateY(${formulaConfig.lowerCell.yOffset}px)`,
}))

const upperCellStyle = computed(() => ({
  marginLeft: `${countryNameWidth.value + formulaConfig.upperCell.leftOffset}px`,
  transform: `translateY(${formulaConfig.upperCell.yOffset}px)`,
}))

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
        gaeShare: value.gae_share ?? null,
        isOverall: false,
        isSubcategory: subcategoriesNoThirdCountries.includes(key),
        isElectricity: electricityKeys.includes(key),
        isGroupStarter: groupStarters.includes(key)
      })
    }
  }

  // Check subcategory groups for "Other" remainder
  const coalKeys = ['anthracite', 'coking_coal', 'other_bituminous_coal', 'sub_bituminous_coal', 'lignite']
  const oilKeys = ['crude_oil', 'ngl']

  for (const [groupName, groupKeys] of [['coal', coalKeys], ['oil', oilKeys]]) {
    let totalGae = 0
    let lastIdx = -1

    for (let i = 0; i < data.length; i++) {
      if (groupKeys.includes(data[i].key)) {
        totalGae += (data[i].gaeShare ?? 0)
        lastIdx = i
      }
    }

    if (lastIdx >= 0 && totalGae < 99.5) {
      data.splice(lastIdx + 1, 0, {
        key: `${groupName}_other`,
        name: 'Other',
        overall: null,
        thirdCountries: null,
        gaeShare: Math.max(0, 100 - totalGae),
        isOverall: false,
        isSubcategory: true,
        isOtherRemainder: true,
        isElectricity: false,
        isGroupStarter: false
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

  const barHeight = 30
  const otherRowHeight = 10
  const barGap = 4
  const groupGap = 24
  const maxWidth = Math.min(containerWidth, 565)
  const margin = { top: 20, right: 110, bottom: 10, left: 100 }
  const width = maxWidth - margin.left - margin.right

  // Calculate y positions with group spacing
  const yPositions = []
  let currentY = 0
  chartData.value.forEach((d, i) => {
    if (i > 0) {
      currentY += (d.isGroupStarter || d.isElectricity) ? groupGap : barGap
    }
    yPositions.push(currentY)
    currentY += d.isOtherRemainder ? otherRowHeight : barHeight
  })
  const height = currentY

  // Helper: determine subcategory group
  const getSubcatGroup = (key) =>
    key.includes('coal') || key.includes('anthracite') || key.includes('coking') || key.includes('bituminous') || key.includes('lignite') ? 'coal' : 'oil'

  // First pass: compute total GAE per group so we can clamp to 100%
  const groupGaeTotals = {}
  chartData.value.forEach(d => {
    if (!d.isSubcategory) return
    const group = getSubcatGroup(d.key)
    groupGaeTotals[group] = (groupGaeTotals[group] ?? 0) + (d.gaeShare ?? 0)
  })

  // Normalized GAE shares: scale down proportionally if group total > 100
  const normalizedGae = []
  chartData.value.forEach((d, i) => {
    if (d.isSubcategory) {
      const group = getSubcatGroup(d.key)
      const total = groupGaeTotals[group] ?? 0
      const raw = d.gaeShare ?? 0
      normalizedGae[i] = total > 100 ? (raw / total) * 100 : raw
    } else {
      normalizedGae[i] = 0
    }
  })

  // Pre-compute subcategory x-offsets using normalized shares
  const subcatXOffset = []
  let cumulativeOffset = 0
  let lastParentGroup = null
  chartData.value.forEach((d, i) => {
    if (d.isSubcategory) {
      const group = getSubcatGroup(d.key)
      if (group !== lastParentGroup) {
        cumulativeOffset = 0
        lastParentGroup = group
      }
      subcatXOffset[i] = cumulativeOffset
      cumulativeOffset += Math.min(normalizedGae[i], 100)
    } else {
      subcatXOffset[i] = 0
      lastParentGroup = null
      cumulativeOffset = 0
    }
  })

  const svg = d3.select(chartRef.value)
    .append('svg')
    .attr('width', maxWidth)
    .attr('height', height + margin.top + margin.bottom)
    .append('g')
    .attr('transform', `translate(${margin.left},${margin.top})`)

  // Calculate maximum value for dynamic scale
  const maxOverall = Math.max(100, ...chartData.value.map(d => d.overall ?? 0))
  const scaleMax = Math.ceil(maxOverall / 10) * 10

  // Scales
  const x = d3.scaleLinear()
    .domain([0, scaleMax])
    .range([0, width])

  // Color definitions
  const colors = {
    third: { normal: '#c44536', soft: '#d4847a' },
    eu: { normal: '#e8a87c', soft: '#f0c9b0' },
    noneu: { normal: '#333', soft: '#666' },
    domestic: { normal: '#d9d9d9', soft: '#e8e8e8' },
    reserve: { normal: '#8b2500', soft: '#b86347' },
    reserveEu: { normal: '#b86b3a', soft: '#d4a07a' },
    exporter: { normal: '#4a90d9', soft: '#7ab3e8' }
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
    .attr('stroke', colors['noneu'].normal)
    .attr('stroke-width', 2)

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
      .attr('font-size', '11px')
      .text('100%')
  }

  // Draw alternating group backgrounds and overall outline
  const groupBounds = {}
  const groupOrder = []
  chartData.value.forEach((d, i) => {
    let group = null
    if (d.isOverall) {
      group = 'overall'
    } else {
      for (const [gName, gKeys] of Object.entries(fuelGroups)) {
        if (gKeys.includes(d.key)) { group = gName; break }
      }
      if (!group && d.key.endsWith('_other')) group = d.key.replace('_other', '')
    }
    if (!group) return
    const rowH = d.isOtherRemainder ? otherRowHeight : barHeight
    if (!groupBounds[group]) {
      groupBounds[group] = { minY: yPositions[i], maxY: yPositions[i] + rowH }
      groupOrder.push(group)
    } else {
      groupBounds[group].minY = Math.min(groupBounds[group].minY, yPositions[i])
      groupBounds[group].maxY = Math.max(groupBounds[group].maxY, yPositions[i] + rowH)
    }
  })

  const groupPad = { x: 8, y: 5 }
  const groupFills = ['rgba(0, 0, 0, 0.06)', 'rgba(0, 0, 0, 0)']
  groupOrder.forEach((gName, gi) => {
    const bounds = groupBounds[gName]
    svg.append('rect')
      .attr('class', 'group-bg')
      .attr('x', -margin.left + groupPad.x)
      .attr('y', bounds.minY - groupPad.y)
      .attr('width', maxWidth - groupPad.x * 2)
      .attr('height', bounds.maxY - bounds.minY + groupPad.y * 2)
      .attr('fill', groupFills[gi % 2])
      .attr('stroke', 'none')
  })

  // Overall outline around all groups
  const allMinY = Math.min(...groupOrder.map(g => groupBounds[g].minY))
  const allMaxY = Math.max(...groupOrder.map(g => groupBounds[g].maxY))
  svg.append('rect')
    .attr('class', 'chart-outline')
    .attr('x', -margin.left + groupPad.x)
    .attr('y', allMinY - groupPad.y)
    .attr('width', maxWidth - groupPad.x * 2)
    .attr('height', allMaxY - allMinY + groupPad.y * 2)
    .attr('fill', 'none')
    .attr('stroke', 'rgba(0, 0, 0, 0.2)')
    .attr('stroke-width', 1)
    .attr('rx', 6)

  // Draw horizontal bars for each fuel type
  chartData.value.forEach((d, i) => {
    const yPos = yPositions[i]
    const barH = d.isOtherRemainder ? otherRowHeight : barHeight
    const isSubcat = d.isSubcategory

    // "Other" remainder line: thin bar right-aligned to 100%
    if (d.isOtherRemainder) {
      const barFullWidth = x(100)
      const otherW = barFullWidth * (Math.min(normalizedGae[i], 100) / 100)
      const otherX = barFullWidth * (subcatXOffset[i] / 100)
      const lineH = 4
      const lineY = yPos + (barH - lineH) / 2

      svg.append('rect')
        .attr('x', otherX)
        .attr('y', lineY)
        .attr('width', otherW)
        .attr('height', lineH)
        .attr('fill', '#bbb')
        .attr('rx', 2)

      return
    }

    // Subcategories with near-zero GAE share: show "not used" at left edge (no offset)
    if (isSubcat && d.gaeShare != null && d.gaeShare < 0.5) {
      svg.append('text')
        .attr('x', 4)
        .attr('y', yPos + barH / 2)
        .attr('dy', '0.35em')
        .attr('text-anchor', 'start')
        .attr('fill', '#888')
        .attr('font-size', '11px')
        .attr('font-style', 'italic')
        .text('not used')
      return
    }

    const getColor = (colorKey) => colors[colorKey].normal

    // For electricity, use third_countries as the overall value
    const effectiveOverall = d.isElectricity && d.overall == null && d.thirdCountries != null
      ? d.thirdCountries
      : d.overall

    if (effectiveOverall != null) {
      const rawOverall = effectiveOverall
      const isNetExporter = rawOverall < 0
      const overallPct = Math.max(0, rawOverall)
      const thirdCountriesPct = d.thirdCountries != null ? Math.max(0, d.thirdCountries) : null

      // Common subcategory geometry
      const barFullWidth = x(100)
      const subcatShare = isSubcat ? Math.min(normalizedGae[i], 100) : 100
      const barW = isSubcat ? barFullWidth * (subcatShare / 100) : null
      const barXStart = isSubcat ? barFullWidth * (subcatXOffset[i] / 100) : 0

      if (isNetExporter) {
        if (isSubcat && barW != null && barW > 0) {
          // Subcategory net exporter: grey background + exporter overlay
          svg.append('rect')
            .attr('class', 'bar-domestic')
            .attr('x', barXStart)
            .attr('y', yPos)
            .attr('width', barW)
            .attr('height', barH)
            .attr('fill', getColor('domestic'))

          svg.append('rect')
            .attr('class', 'bar-exporter')
            .attr('x', barXStart)
            .attr('y', yPos)
            .attr('width', barW)
            .attr('height', barH)
            .attr('fill', getColor('exporter'))

          svg.append('text')
            .attr('x', barXStart + barW + 4)
            .attr('y', yPos + barH / 2)
            .attr('dy', '0.35em')
            .attr('text-anchor', 'start')
            .attr('fill', '#7ab3e8')
            .attr('font-size', '11px')
            .attr('font-weight', '700')
            .text(`${rawOverall.toFixed(0)}%`)

        } else {
          // Non-subcategory net exporter: full-width bar
          svg.append('rect')
            .attr('class', 'bar-exporter')
            .attr('x', 0)
            .attr('y', yPos)
            .attr('width', barFullWidth)
            .attr('height', barH)
            .attr('fill', getColor('exporter'))

          if (barFullWidth > 50) {
            svg.append('text')
              .attr('x', barFullWidth / 2)
              .attr('y', yPos + barH / 2)
              .attr('dy', '0.35em')
              .attr('text-anchor', 'middle')
              .attr('fill', '#fff')
              .attr('font-size', '11px')
              .attr('font-weight', '600')
              .text('Net Exporter')
          }

          svg.append('text')
            .attr('x', barFullWidth + 4)
            .attr('y', yPos + barH / 2)
            .attr('dy', '0.35em')
            .attr('text-anchor', 'start')
            .attr('fill', '#3a7bc8')
            .attr('font-size', '11px')
            .attr('font-weight', '700')
            .text(`${rawOverall.toFixed(0)}%`)
        }

      } else {
        // Normal case: import dependency >= 0
        const domesticPct = overallPct < 100 ? 100 - overallPct : 0
        const reserveDrawPct = overallPct > 100 ? overallPct - 100 : 0

        if (isSubcat && barW != null) {
          // Subcategory: grey background at full proportional width, import fill at correct %
          if (barW > 0) {
            // Grey domestic background spanning full proportional width
            svg.append('rect')
              .attr('class', 'bar-domestic')
              .attr('x', barXStart)
              .attr('y', yPos)
              .attr('width', barW)
              .attr('height', barH)
              .attr('fill', getColor('domestic'))

            // Import portion: overallPct% of the proportional width
            if (overallPct > 0) {
              const importW = barW * (Math.min(overallPct, 100) / 100)
              svg.append('rect')
                .attr('class', 'bar-import')
                .attr('x', barXStart)
                .attr('y', yPos)
                .attr('width', importW)
                .attr('height', barH)
                .attr('fill', getColor('eu'))
            }

            // Reserve draw: portion above 100% extends beyond the grey background
            if (reserveDrawPct > 0) {
              const reserveW = barW * (reserveDrawPct / 100)
              svg.append('rect')
                .attr('class', 'bar-reserve')
                .attr('x', barXStart + barW)
                .attr('y', yPos)
                .attr('width', reserveW)
                .attr('height', barH)
                .attr('fill', getColor('reserve'))
                .attr('opacity', 0.85)
            }
          }

        } else {
          // Non-subcategory: full-width bar as before
          if (overallPct > 0) {
            const importBelow100 = Math.min(overallPct, 100)
            svg.append('rect')
              .attr('class', 'bar-import')
              .attr('x', 0)
              .attr('y', yPos)
              .attr('width', x(importBelow100))
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

          // Domestic portion
          if (domesticPct > 0) {
            svg.append('rect')
              .attr('class', 'bar-domestic')
              .attr('x', x(overallPct))
              .attr('y', yPos)
              .attr('width', x(100) - x(overallPct))
              .attr('height', barH)
              .attr('fill', getColor('domestic'))
          }
        }

        // Non-EU crosshatch overlay (capped at overall import bar width)
        if (thirdCountriesPct != null && thirdCountriesPct > 0 && !d.isElectricity && !isSubcat) {
          const clampedThirdPct = Math.min(thirdCountriesPct, overallPct)
          const nonEuWidth = x(clampedThirdPct)

          if (nonEuWidth > 0) {
            svg.append('rect')
              .attr('x', 0)
              .attr('y', yPos)
              .attr('width', nonEuWidth)
              .attr('height', barH)
              .attr('fill', 'url(#crosshatch)')
              .attr('opacity', 0.4)

            svg.append('line')
              .attr('x1', x(clampedThirdPct))
              .attr('y1', yPos)
              .attr('x2', x(clampedThirdPct))
              .attr('y2', yPos + barH)
              .attr('stroke', getColor('noneu'))
              .attr('stroke-width', 2)

            if (nonEuWidth >= 35) {
              svg.append('text')
                .attr('x', nonEuWidth / 2)
                .attr('y', yPos + barH / 2)
                .attr('dy', '0.35em')
                .attr('text-anchor', 'middle')
                .attr('fill', getColor('noneu'))
                .attr('font-size', '11px')
                .attr('font-weight', '700')
                .text('non-EU')
            }
          }
        }

        // Percentage label after the bar (including reserve draw tip if present)
        const subcatReserveW = (isSubcat && reserveDrawPct > 0) ? barW * (reserveDrawPct / 100) : 0
        const labelX = isSubcat
          ? barXStart + barW + subcatReserveW + 4
          : x(overallPct) + 4
        const pctLabel = svg.append('text')
          .attr('x', labelX)
          .attr('y', yPos + barH / 2)
          .attr('dy', '0.35em')
          .attr('text-anchor', 'start')
          .attr('fill', overallPct > 100 ? (isSubcat ? '#b86347' : '#8b2500') : '#444')
          .attr('font-size', '11px')
          .attr('font-weight', overallPct > 100 ? '700' : '500')
          .text(`${overallPct.toFixed(0)}%${overallPct > 100 ? ' (reserve draw)' : ''}`)

        // Electricity warning icon
        if (d.isElectricity) {
          const pctWidth = pctLabel.node().getBBox().width
          const warningX = labelX + pctWidth + 10

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
            .attr('font-size', '11px')
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
    } else {
      // No data (same proportional width and offset as normal bars)
      const barFullWidth = x(100)
      const noDataShare = isSubcat ? Math.min(normalizedGae[i], 100) : 100
      const noDataW = isSubcat ? barFullWidth * (noDataShare / 100) : barFullWidth
      const noDataX = isSubcat ? barFullWidth * (subcatXOffset[i] / 100) : 0

      svg.append('rect')
        .attr('class', 'bar-nodata')
        .attr('x', noDataX)
        .attr('y', yPos)
        .attr('width', noDataW)
        .attr('height', barH)
        .attr('fill', isSubcat ? '#e4e4e4' : '#d9d9d9')
        .attr('rx', 3)

      if (noDataW > 30) {
        svg.append('text')
          .attr('class', 'no-data-label')
          .attr('x', noDataX + noDataW / 2)
          .attr('y', yPos + barH / 2)
          .attr('dy', '0.35em')
          .attr('text-anchor', 'middle')
          .attr('fill', '#777')
          .attr('font-size', '11px')
          .text('No data')
      }

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
          .attr('font-size', '11px')
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

  // Y axis labels (manually positioned to match group spacing)
  chartData.value.forEach((d, i) => {
    const isSubcat = d.isSubcategory
    const rowH = d.isOtherRemainder ? otherRowHeight : barHeight
    svg.append('text')
      .attr('x', -8)
      .attr('y', yPositions[i] + rowH / 2)
      .attr('dy', '0.35em')
      .attr('text-anchor', 'end')
      .attr('fill', d.isOtherRemainder ? '#777' : (isSubcat ? '#555' : '#222'))
      .attr('font-size', d.isOtherRemainder ? '11px' : '11px')
      .attr('font-style', (isSubcat || d.isOtherRemainder) ? 'italic' : 'normal')
      .text(d.name)
  })

}

watch(() => [props.dependencyData, props.year], () => {
  renderChart()
}, { deep: true })

watch(() => props.countryName, () => {
  nextTick(measureCountryName)
})

onMounted(() => {
  renderChart()
  nextTick(measureCountryName)

  resizeObserver = new ResizeObserver(() => {
    renderChart()
    measureCountryName()
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
  border-radius: 8px;
}

.no-data {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 3rem;
  color: #999;
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
  width: 100%;
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  flex-shrink: 0;
}

.chart-svg :deep(svg) {
  display: block;
}

.chart-heading {
  text-align: center;
}

.chart-heading h3 {
  margin: 0 0 0.25rem 0;
}

.heading-link {
  font-family: 'Fira Sans', sans-serif;
  font-weight: 400;
  font-size: 1rem;
}

.formula-stack {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.formula {
  display: block;
  background: rgba(0, 0, 0, 0.06);
  padding: 0.3em 0.5em;
  border-radius: 3px;
}

.curly-brace {
  height: 12px;
  margin: 2px 0;
}

.highlight-value {
  font-weight: 800;
  color: var(--text-color-dark-green, #2d3a0e);
  background: rgba(172, 194, 120, 0.25);
  padding: 0.05em 0.3em;
  border-radius: 4px;
}

h3 > *{
  font-size: inherit;
  font-family: inherit;
}

.highlight-import {
  color: #e8a87c;
}

.electricity-tooltip {
  position: absolute;
  background: var(--primary-color);
  border: 1px solid var(--text-color-red);
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
</style>
