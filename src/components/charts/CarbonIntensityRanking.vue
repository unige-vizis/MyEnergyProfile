<template>
  <div v-if="!hasData" class="no-data">
    <span class="material-symbols-outlined">bar_chart_off</span>
    <p>No carbon intensity ranking data available.</p>
  </div>
  <div v-else class="chart-wrapper">
    <h3>Carbon Intensity of the Energy Grid - Europe Comparison</h3>
    <p>
      Now lets look through the lens of carbon intensity, which relates electricity to carbon emissions. The chart below
      shows the average CO2 emitted per kilowatt-hour of electricity generated from all sources, indicating how clean
      the power grid is in terms of emissions. Heavy reliance on nuclear power contributes to low carbon intensity
      levels for electricity, as in the case of France for example, but referring to it as "clean energy" remains a
      topic of discussion.
    </p>
    <div class="chart-container scroll-container">
      <div v-if="thresholdLeft != null" class="threshold-label" :style="{ left: thresholdLeft + 'px' }">
        IEA / EU sustainable energy threshold (100 gCO&#x2082;/kWh)
      </div>
      <div class="chart-scroll-outer">
        <div v-if="thresholdLeft != null" class="threshold-line-overlay" :style="{ left: thresholdLeft + 'px' }"></div>
        <div ref="scrollContainer" class="chart-scroll">
          <div ref="chartRef" class="chart-svg"></div>
        </div>
      </div>
      <div class="chart-meta">
        <div class="meta-section">
          <span class="meta-label">Source</span>
          <ul>
            <li>
              <strong>OWID</strong>
              <a href="https://github.com/owid/energy-data" target="_blank" rel="noopener"> Energy Data </a>
              . Column: <code>carbon_intensity_elec</code> (gCO2/kWh)
            </li>
          </ul>
        </div>
        <div class="meta-section"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import * as d3 from 'd3'
import { useEnergyDataStore } from '@/stores/energyData'

const store = useEnergyDataStore()

const props = defineProps({
  rankingData: { type: Array, default: () => [] },
  selectedCountryCode: { type: String, default: '' }
})

const chartRef = ref(null)
const scrollContainer = ref(null)
const thresholdLeft = ref(null)
let resizeObserver = null

const hasData = computed(() => props.rankingData && props.rankingData.length > 0)

function renderChart() {
  if (!chartRef.value || !hasData.value) return

  d3.select(chartRef.value).selectAll('*').remove()

  const data = props.rankingData
  const containerWidth = chartRef.value.clientWidth || 500
  const margin = { top: 10, right: 120, bottom: 5, left: 175 }
  const barHeight = 26
  const selectedBarHeight = 42
  const gap = 3

  // Calculate total height accounting for the taller selected bar
  let totalRowsHeight = 0
  data.forEach(d => {
    totalRowsHeight += (d.code === props.selectedCountryCode ? selectedBarHeight : barHeight) + gap
  })
  const height = margin.top + margin.bottom + totalRowsHeight
  const width = containerWidth
  const innerWidth = width - margin.left - margin.right
  const innerHeight = height - margin.top - margin.bottom

  const svg = d3.select(chartRef.value)
    .append('svg')
    .attr('width', width)
    .attr('height', height)

  const g = svg.append('g')
    .attr('transform', `translate(${margin.left}, ${margin.top})`)

  const maxVal = d3.max(data, d => d.value) || 1

  const xScale = d3.scaleLinear()
    .domain([0, maxVal * 1.05])
    .range([0, innerWidth])

  // Color scale for bars (green up to 100, transition to red beyond)
  const colorScale = d3.scaleLinear()
    .domain([0, 100, 300, maxVal])
    .range(['#27ae60', '#8fce00', '#f39c12', '#e74c3c'])
    .clamp(true)

  // Bars with variable height for selected country
  let yOffset = 0
  data.forEach((d) => {
    const isSelected = d.code === props.selectedCountryCode
    const h = isSelected ? selectedBarHeight : barHeight
    const y = yOffset

    // Clickable row group
    const row = g.append('g')
      .attr('class', 'bar-row')
      .style('cursor', isSelected ? 'default' : 'pointer')
      .on('click', () => {
        if (!isSelected) store.setSelectedCountry(d.code)
      })

    // Invisible hit area covering the full row width
    row.append('rect')
      .attr('x', -margin.left)
      .attr('y', y)
      .attr('width', width)
      .attr('height', h)
      .attr('fill', 'transparent')

    // Bar
    const bar = row.append('rect')
      .attr('x', 0)
      .attr('y', y)
      .attr('width', xScale(d.value))
      .attr('height', h)
      .attr('fill', colorScale(d.value))
      .attr('fill-opacity', isSelected ? 1 : 0.65)
      .attr('stroke', isSelected ? '#222' : 'none')
      .attr('stroke-width', isSelected ? 2.5 : 0)
      .attr('rx', 3)

    // Hover effect for non-selected bars
    if (!isSelected) {
      row.on('mouseenter', () => { bar.attr('fill-opacity', 0.9) })
         .on('mouseleave', () => { bar.attr('fill-opacity', 0.65) })
    }

    // Strong highlight for selected country
    if (isSelected) {
      // Outer glow
      g.append('rect')
        .attr('x', -4)
        .attr('y', y - 4)
        .attr('width', xScale(d.value) + 8)
        .attr('height', h + 8)
        .attr('fill', 'none')
        .attr('stroke', colorScale(d.value))
        .attr('stroke-width', 2.5)
        .attr('stroke-opacity', 0.35)
        .attr('rx', 6)
    }

    // Country name label (left side)
    row.append('text')
      .attr('x', -8)
      .attr('y', y + h / 2)
      .attr('text-anchor', 'end')
      .attr('dominant-baseline', 'central')
      .attr('font-size', isSelected ? '15px' : '10px')
      .attr('font-weight', isSelected ? '900' : '400')
      .attr('fill', isSelected ? '#000' : '#666')
      .text(d.name)

    // Value label (right of bar)
    row.append('text')
      .attr('x', xScale(d.value) + 8)
      .attr('y', y + h / 2)
      .attr('dominant-baseline', 'central')
      .attr('font-size', isSelected ? '17px' : '10px')
      .attr('font-weight', isSelected ? '900' : '400')
      .attr('fill', isSelected ? '#000' : '#666')
      .text(isSelected ? `${Math.round(d.value)} gCO\u2082/kWh` : `${Math.round(d.value)}`)

    yOffset += h + gap
  })

  // Position the fixed HTML threshold line + label
  const thresholdX = xScale(100)
  if (thresholdX > 0 && thresholdX < innerWidth) {
    thresholdLeft.value = margin.left + thresholdX
  } else {
    thresholdLeft.value = null
  }

  // Scroll to center the selected country in the visible window
  scrollToSelected(data, margin.top, barHeight, selectedBarHeight, gap)
}

function scrollToSelected(data, marginTop, bh, sbh, gap) {
  if (!scrollContainer.value) return
  const idx = data.findIndex(d => d.code === props.selectedCountryCode)
  if (idx === -1) return

  // Compute pixel offset of the selected bar
  let selectedY = marginTop
  for (let i = 0; i < idx; i++) {
    selectedY += (data[i].code === props.selectedCountryCode ? sbh : bh) + gap
  }
  const containerH = scrollContainer.value.clientHeight
  // Place selected bar roughly in the upper third
  const targetScroll = selectedY - containerH * 0.35
  scrollContainer.value.scrollTop = Math.max(0, targetScroll)
}

watch(() => [props.rankingData, props.selectedCountryCode], () => {
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
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
}
.chart-svg {
  width: 100%;
}
.threshold-label {
  position: relative;
  font-size: 11px;
  color: var(--text-color-gray);
  margin-bottom: 4px;
  white-space: nowrap;
  transform: translateX(-50%);
  text-align: center;
  z-index: 3;
}
.threshold-line-overlay {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 0;
  border-left: 1.5px dashed rgba(100, 100, 100, 0.55);
  z-index: 3;
  pointer-events: none;
}
</style>
