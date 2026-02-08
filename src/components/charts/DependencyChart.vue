<template>
  <div v-if="!hasData" class="no-data">
    <span class="no-data-icon">?</span>
    <span>No dependency data available for this year</span>
  </div>

  <div v-else class="chart-wrapper">
    <div class="chart-container">
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
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import * as d3 from 'd3'


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
  border-radius: 8px;
}

.chart-header {
  margin-bottom: 1rem;
}

.source-link {
  display: block;
  margin-top: 0.2rem;
  color: var(--text-color-dark-green);
  text-decoration: none;
  font-size: 0.7rem;
}

.source-link:hover {
  text-decoration: underline;
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

.chart-legend {
  display: flex;
  gap: 1.5rem;
  justify-content: flex-start;
  flex-wrap: wrap;
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
</style>
