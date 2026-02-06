<template>
  <div class="small-multiples-chart">
    <div v-if="!hasData" class="no-data">
      No production/consumption data available
    </div>

    <div v-else class="chart-content">
      <div ref="chartRef" class="chart-grid"></div>

      <div class="chart-meta">
        <div class="meta-section">
          <span class="meta-label">Data Hints:</span>
          <div class="chart-notes">
            <p class="chart-note">
              <span class="note-icon">*</span>
              <span>Y-axis scales differ between production and consumption rows. This is necessary because production and consumption volumes can differ by orders of magnitude for most countries.</span>
            </p>
          </div>
        </div>
        <div class="meta-section">
          <span class="meta-label">Source:</span>
          <ul class="meta-list">
            <li><a href="https://github.com/owid/energy-data" target="_blank" rel="noopener">Our World in Data Energy Dataset</a> · Fields: <code>coal_production</code>, <code>oil_production</code>, <code>gas_production</code>, <code>electricity_generation</code>, <code>coal_consumption</code>, <code>oil_consumption</code>, <code>gas_consumption</code>, <code>biofuel_consumption</code>, <code>electricity_demand</code> (all in TWh)</li>
            <li>Underlying data compiled by the <a href="https://www.energyinst.org/statistical-review" target="_blank" rel="noopener">Energy Institute</a> Statistical Review of World Energy</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import * as d3 from 'd3'

const props = defineProps({
  productionConsumptionData: { type: Object, default: null },
  countryYears: { type: Object, default: null },
  selectedYear: { type: Number, default: null },
  countryName: { type: String, default: '' }
})

const chartRef = ref(null)
let resizeObserver = null

const resources = [
  { code: 'SFF', label: 'Coal', color: '#8b4513' },
  { code: 'OIL', label: 'Oil', color: '#1a1a1a' },
  { code: 'GAS', label: 'Gas', color: '#2980b9' },
  { code: 'BIO', label: 'Biofuels', color: '#27ae60' },
  { code: 'EH', label: 'Electricity', color: '#f1c40f' }
]

const hasData = computed(() => {
  return props.countryYears && Object.keys(props.countryYears).length > 0
})

const timeSeriesData = computed(() => {
  if (!props.countryYears) return { years: [], series: {} }

  const years = Object.keys(props.countryYears)
    .map(Number)
    .filter(y => !isNaN(y))
    .sort((a, b) => a - b)

  const series = {}
  for (const r of resources) {
    const prod = []
    const cons = []
    for (const year of years) {
      const yd = props.countryYears[year]
      prod.push({ year, value: yd?.production?.[r.code] ?? null })
      cons.push({ year, value: yd?.consumption?.[r.code] ?? null })
    }
    series[r.code] = { production: prod, consumption: cons }
  }

  return { years, series }
})

function formatTick(v) {
  if (v >= 1000) return `${(v / 1000).toFixed(1)}k`
  if (v >= 10) return v.toFixed(0)
  if (v >= 1) return v.toFixed(1)
  return v.toFixed(2)
}

function renderChart() {
  if (!chartRef.value || !hasData.value) return
  d3.select(chartRef.value).selectAll('*').remove()

  const { years, series } = timeSeriesData.value
  if (years.length === 0) return

  const container = chartRef.value
  const totalWidth = container.clientWidth || 700

  const nCols = resources.length
  const nRows = 2
  const rowLabels = ['Production', 'Consumption']
  const rowKeys = ['production', 'consumption']

  // Compute x-domain from actual data (first/last year with any prod/cons value)
  let dataMinYear = Infinity
  let dataMaxYear = -Infinity
  for (const r of resources) {
    for (const key of rowKeys) {
      const vals = series[r.code][key].filter(d => d.value != null)
      if (vals.length > 0) {
        dataMinYear = Math.min(dataMinYear, vals[0].year)
        dataMaxYear = Math.max(dataMaxYear, vals[vals.length - 1].year)
      }
    }
  }
  if (!isFinite(dataMinYear)) { dataMinYear = years[0]; dataMaxYear = years[years.length - 1] }
  const xDomain = [dataMinYear, dataMaxYear]

  // Dimensions — squarish cells, tight spacing
  const margin = { top: 18, right: 10, bottom: 30, left: 46 }
  const rowLabelWidth = 20 // space to the left of each row for rotated label
  const colGap = 4
  const rowGap = 8
  const cellWidth = Math.max(100, (totalWidth - rowLabelWidth - colGap * (nCols - 1)) / nCols)
  const cellHeight = cellWidth * 0.85
  const plotW = cellWidth - margin.left - margin.right
  const plotH = cellHeight - margin.top - margin.bottom

  const svgWidth = rowLabelWidth + nCols * cellWidth + (nCols - 1) * colGap
  const svgHeight = nRows * cellHeight + (nRows - 1) * rowGap

  const svg = d3.select(container)
    .append('svg')
    .attr('width', svgWidth)
    .attr('height', svgHeight)

  for (let row = 0; row < nRows; row++) {
    const rowKey = rowKeys[row]
    const cy = row * (cellHeight + rowGap)

    // Row label — rotated 90° on the left side
    svg.append('text')
      .attr('transform', `translate(${12}, ${cy + cellHeight / 2}) rotate(-90)`)
      .attr('text-anchor', 'middle')
      .attr('fill', '#222')
      .attr('font-size', '12px')
      .attr('font-weight', '700')
      .text(rowLabels[row])

    for (let col = 0; col < nCols; col++) {
      const r = resources[col]
      const cx = rowLabelWidth + col * (cellWidth + colGap)
      const data = series[r.code][rowKey]
      const validData = data.filter(d => d.value != null)
      const isBioProd = r.code === 'BIO' && rowKey === 'production'

      const g = svg.append('g')
        .attr('transform', `translate(${cx + margin.left}, ${cy + margin.top})`)

      // Top border line
      g.append('line')
        .attr('x1', 0).attr('x2', plotW)
        .attr('y1', 0).attr('y2', 0)
        .attr('stroke', '#222').attr('stroke-width', 1)

      // Right border line
      g.append('line')
        .attr('x1', plotW).attr('x2', plotW)
        .attr('y1', 0).attr('y2', plotH)
        .attr('stroke', '#222').attr('stroke-width', 1)

      // Column header on top row only
      if (row === 0) {
        svg.append('text')
          .attr('x', cx + cellWidth / 2)
          .attr('y', cy + 14)
          .attr('text-anchor', 'middle')
          .attr('fill', r.color)
          .attr('font-size', '12px')
          .attr('font-weight', '700')
          .text(r.label)
      }

      // X scale
      const x = d3.scaleLinear().domain(xDomain).range([0, plotW])

      // Y scale
      const yMax = d3.max(validData, d => d.value) || 1
      const y = d3.scaleLinear().domain([0, yMax * 1.1]).range([plotH, 0])

      // Y axis — append TWh to the topmost tick label
      const yAxis = d3.axisLeft(y).ticks(3).tickSize(-plotW).tickFormat(d => formatTick(d))
      const yAxisG = g.append('g').call(yAxis)
      yAxisG.selectAll('.domain').remove()
      // Manual left axis line
      g.append('line')
        .attr('x1', 0).attr('x2', 0)
        .attr('y1', 0).attr('y2', plotH)
        .attr('stroke', '#222').attr('stroke-width', 1)
      yAxisG.selectAll('.tick line').remove()
      yAxisG.selectAll('.tick text').attr('fill', '#222').attr('font-size', '9px')
      // Add TWh suffix to the topmost tick
      const yTicks = yAxisG.selectAll('.tick text')
      if (!yTicks.empty()) {
        const lastTick = yTicks.nodes()[yTicks.size() - 1]
        const cur = d3.select(lastTick).text()
        d3.select(lastTick).text(cur + ' TWh')
      }

      // X axis on both rows
      const xAxis = d3.axisBottom(x).ticks(4).tickFormat(d3.format('d'))
      const xAxisG = g.append('g').attr('transform', `translate(0, ${plotH})`).call(xAxis)
      xAxisG.selectAll('.domain').attr('stroke', '#222')
      xAxisG.selectAll('.tick line').remove()
      xAxisG.selectAll('.tick text').attr('fill', '#222').attr('font-size', '9px')

      // No data messages
      if (isBioProd || validData.length === 0) {
        g.append('text')
          .attr('x', plotW / 2)
          .attr('y', plotH / 2)
          .attr('text-anchor', 'middle')
          .attr('fill', '#bbb')
          .attr('font-size', '10px')
          .attr('font-style', 'italic')
          .text(isBioProd ? 'No production data' : 'No data')
        continue
      }

      // Line
      const line = d3.line()
        .defined(d => d.value != null)
        .x(d => x(d.year))
        .y(d => y(d.value))
      g.append('path')
        .datum(data)
        .attr('d', line)
        .attr('fill', 'none')
        .attr('stroke', r.color)
        .attr('stroke-width', 1.5)

      // Markers
      g.selectAll('.dot')
        .data(validData)
        .join('circle')
        .attr('cx', d => x(d.year))
        .attr('cy', d => y(d.value))
        .attr('r', validData.length > 40 ? 1 : validData.length > 20 ? 1.5 : 2.5)
        .attr('fill', r.color)

      // Selected year red circle
      if (props.selectedYear != null) {
        const datum = data.find(d => d.year === props.selectedYear && d.value != null)
        if (datum) {
          g.append('circle')
            .attr('cx', x(datum.year))
            .attr('cy', y(datum.value))
            .attr('r', 4)
            .attr('fill', 'none')
            .attr('stroke', '#e74c3c')
            .attr('stroke-width', 1.5)
        }
      }
    }
  }
}

watch(
  () => [props.countryYears, props.selectedYear, props.countryName],
  () => nextTick(() => renderChart()),
  { deep: true }
)

onMounted(() => {
  renderChart()
  resizeObserver = new ResizeObserver(() => renderChart())
  if (chartRef.value) resizeObserver.observe(chartRef.value)
})

onUnmounted(() => {
  if (resizeObserver) resizeObserver.disconnect()
})
</script>

<style scoped>
.small-multiples-chart {
  padding: 1rem;
}

.no-data {
  padding: 2rem;
  text-align: center;
  color: #999;
}

.chart-content {
  display: flex;
  flex-direction: column;
}

.chart-grid {
  width: 100%;
  overflow-x: auto;
}

.chart-grid :deep(svg) {
  display: block;
}

.chart-meta {
  margin-top: 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  padding-top: 0.5rem;
  border-top: 1px solid #eee;
}

.meta-section {
  display: flex;
  flex-wrap: wrap;
  gap: 0.3rem;
  font-size: 0.7rem;
  line-height: 1.4;
}

.meta-label {
  font-weight: 600;
  color: #555;
  flex-shrink: 0;
}

.meta-list {
  margin: 0.2rem 0 0 0;
  padding-left: 1.2rem;
  color: #666;
}

.meta-list li {
  margin-bottom: 0.15rem;
}

.chart-notes {
  margin-top: 0.2rem;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
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
</style>
