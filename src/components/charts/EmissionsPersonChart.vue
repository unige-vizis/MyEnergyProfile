<template>
  <div v-if="!hasData" class="no-data">
    <span class="material-symbols-outlined">cloud_off</span>
    <p>No per-capita emissions data available for this country.</p>
  </div>
  <div v-else class="chart-wrapper">
    <div class="chart-container">
      <div ref="chartRef" class="chart-svg"></div>
      <div class="chart-meta">
        <div class="meta-section">
          <span class="meta-label">Source</span>
          <ul>
            <li>
              <strong>IEA</strong>
              <a href="https://www.iea.org/data-and-statistics" target="_blank" rel="noopener">
                Energy End-Uses &amp; Efficiency Indicators
              </a>
              (per-capita carbon intensity by sector). Indicator:
              <code>Carbon intensity per capita (t CO2/capita)</code>. End uses: <code>Total residential</code>,
              <code>Total services</code>, <code>Cars/light trucks</code> + <code>Freight trucks</code> (transport)
            </li>
            <li>
              Industry per-capita derived from IEA total emissions (indicator: <code>Total final use (kt CO2)</code>,
              end use containing <code>Manufacturing</code>) divided by
              <strong>OWID</strong>
              <a href="https://github.com/owid/energy-data" target="_blank" rel="noopener"> Energy Data </a>
              <code>population</code> column
            </li>
          </ul>
        </div>
        <div class="meta-section">
          <span class="meta-label">Data Hints:</span>
          <ul>
            <li>Transport includes cars/light trucks and freight trucks only (road transport).</li>
            <li>Sector data years may differ slightly. The latest available year per sector is used.</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import * as d3 from 'd3'

const props = defineProps({
  emissionsData: { type: Object, default: null },
  countryName: { type: String, default: '' }
})

const chartRef = ref(null)
let resizeObserver = null

const hasData = computed(() => {
  if (!props.emissionsData) return false
  const d = props.emissionsData
  return d.residential != null || d.services != null || d.transport != null || d.industry != null
})

const SECTORS = [
  { key: 'residential', label: 'Residential', color: '#63b3df', position: 'top-left' },
  { key: 'transport', label: 'Transport', color: '#ffb56b', position: 'top-right' },
  { key: 'industry', label: 'Industry', color: '#898989', position: 'bottom-left' },
  { key: 'services', label: 'Services', color: '#76d76b', position: 'bottom-right' }
]

// Deterministic hash for stable cloud shapes
function hashCode(str) {
  let hash = 0
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i)
    hash = ((hash << 5) - hash) + char
    hash |= 0
  }
  return Math.abs(hash)
}

// Generate cloud blob points
function generateCloudPoints(cx, cy, baseRadius, seed, numPoints = 12) {
  const points = []
  const h = hashCode(String(seed))
  for (let i = 0; i < numPoints; i++) {
    const angle = (i / numPoints) * Math.PI * 2
    // Deterministic jitter based on seed and point index
    const jitter = 0.7 + 0.6 * (((h * (i + 1) * 7919) % 1000) / 1000)
    const r = baseRadius * jitter
    points.push([cx + r * Math.cos(angle), cy + r * Math.sin(angle)])
  }
  return points
}

// Person silhouette SVG path (centered at 0,0, roughly 200px tall)
const PERSON_PATH = 'M0,-85 C-15,-85 -25,-75 -25,-60 C-25,-45 -15,-35 0,-35 C15,-35 25,-45 25,-60 C25,-75 15,-85 0,-85 Z M0,-30 C-5,-30 -35,-20 -40,-5 L-45,30 C-45,35 -40,38 -35,35 L-20,20 L-25,80 C-25,85 -20,90 -15,90 L-5,90 L0,90 L5,90 L15,90 C20,90 25,85 25,80 L20,20 L35,35 C40,38 45,35 45,30 L40,-5 C35,-20 5,-30 0,-30 Z'

function renderChart() {
  if (!chartRef.value || !hasData.value) return

  d3.select(chartRef.value).selectAll('*').remove()

  const containerWidth = chartRef.value.clientWidth || 500
  const width = Math.min(containerWidth, 500)
  const height = 420
  const cx = width / 2
  const cy = height / 2

  const svg = d3.select(chartRef.value)
    .append('svg')
    .attr('width', width)
    .attr('height', height)
    .attr('viewBox', `0 0 ${width} ${height}`)

  const data = props.emissionsData
  const sectors = SECTORS.filter(s => data[s.key] != null && data[s.key] > 0)

  // Scale: cloud radius proportional to sqrt of value (area scales linearly)
  const maxVal = d3.max(sectors, s => data[s.key]) || 1
  const radiusScale = d3.scaleSqrt()
    .domain([0, maxVal])
    .range([20, 70])

  // Cloud line generator
  const cloudLine = d3.line().curve(d3.curveBasisClosed)

  // Position offsets for each quadrant
  const offsets = {
    'top-left': [-100, -85],
    'top-right': [100, -85],
    'bottom-left': [-100, 95],
    'bottom-right': [100, 95]
  }

  // Draw clouds
  sectors.forEach(sector => {
    const value = data[sector.key]
    const radius = radiusScale(value)
    const offset = offsets[sector.position]
    const cloudCx = cx + offset[0]
    const cloudCy = cy + offset[1]

    const seed = `${sector.key}-${props.countryName}`
    const points = generateCloudPoints(cloudCx, cloudCy, radius, seed)

    // Cloud shape
    svg.append('path')
      .datum(points)
      .attr('d', cloudLine)
      .attr('fill', sector.color)
      .attr('fill-opacity', 0.25)
      .attr('stroke', sector.color)
      .attr('stroke-width', 2)
      .attr('stroke-opacity', 0.6)

    // Second smaller cloud for depth
    const innerPoints = generateCloudPoints(cloudCx, cloudCy, radius * 0.65, seed + '-inner', 10)
    svg.append('path')
      .datum(innerPoints)
      .attr('d', cloudLine)
      .attr('fill', sector.color)
      .attr('fill-opacity', 0.15)
      .attr('stroke', 'none')

    // Label
    const labelY = sector.position.startsWith('top') ? cloudCy - radius - 12 : cloudCy + radius + 18
    svg.append('text')
      .attr('x', cloudCx)
      .attr('y', labelY)
      .attr('text-anchor', 'middle')
      .attr('font-size', '12px')
      .attr('font-weight', '600')
      .attr('fill', sector.color)
      .text(sector.label)

    svg.append('text')
      .attr('x', cloudCx)
      .attr('y', labelY + 15)
      .attr('text-anchor', 'middle')
      .attr('font-size', '11px')
      .attr('fill', '#666')
      .text(`${value.toFixed(2)} tCO\u2082/cap`)
  })

  // Person silhouette (centered)
  svg.append('path')
    .attr('d', PERSON_PATH)
    .attr('transform', `translate(${cx}, ${cy})`)
    .attr('fill', '#555')
    .attr('fill-opacity', 0.8)

  // Year label
  if (data.year) {
    svg.append('text')
      .attr('x', cx)
      .attr('y', height - 8)
      .attr('text-anchor', 'middle')
      .attr('font-size', '12px')
      .attr('fill', '#999')
      .text(`Data year: ${data.year}`)
  }

  // Total
  const total = sectors.reduce((sum, s) => sum + (data[s.key] || 0), 0)
  svg.append('text')
    .attr('x', cx)
    .attr('y', 18)
    .attr('text-anchor', 'middle')
    .attr('font-size', '14px')
    .attr('font-weight', '700')
    .attr('fill', '#333')
    .text(`Total: ${total.toFixed(2)} tCO\u2082 per capita`)
}

watch(() => [props.emissionsData, props.countryName], () => {
  renderChart()
}, { deep: true })

onMounted(() => {
  renderChart()
  resizeObserver = new ResizeObserver(() => { renderChart() })
  if (chartRef.value) resizeObserver.observe(chartRef.value)
})

onUnmounted(() => {
  if (resizeObserver) resizeObserver.disconnect()
})
</script>

<style scoped>
.no-data {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  color: var(--placeholder-color);
  gap: 0.5rem;
}
.no-data .material-symbols-outlined {
  font-size: 48px;
}
.chart-wrapper {
  width: 100%;
}
.chart-container {
  width: 100%;
}
.chart-svg {
  width: 100%;
  display: flex;
  justify-content: center;
}
</style>
