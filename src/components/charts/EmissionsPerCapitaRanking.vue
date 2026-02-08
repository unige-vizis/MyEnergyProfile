<template>
  <div v-if="!hasData" class="no-data">
    <span class="material-symbols-outlined">bar_chart_off</span>
    <p>No emissions per capita ranking data available.</p>
  </div>
  <div v-else class="chart-wrapper">
    <h3>CO2 Emissions - Europe Comparison</h3>
    <p>Total CO2 emissions per person from energy use across all sectors, measured in tonnes per year.</p>

    <div class="chart-container scroll-container">
      <div class="chart-scroll-outer">
        <div ref="scrollContainer" class="chart-scroll">
          <div ref="chartRef" class="chart-svg"></div>
        </div>
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

  let totalRowsHeight = 0
  data.forEach(d => {
    totalRowsHeight += (d.code === props.selectedCountryCode ? selectedBarHeight : barHeight) + gap
  })
  const height = margin.top + margin.bottom + totalRowsHeight
  const width = containerWidth
  const innerWidth = width - margin.left - margin.right

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

  // Color scale for bars (green for low emissions, red for high)
  const colorScale = d3.scaleLinear()
    .domain([0, 3, 6, maxVal])
    .range(['#27ae60', '#8fce00', '#f39c12', '#e74c3c'])
    .clamp(true)

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

    // Highlight for selected country
    if (isSelected) {
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
      .text(isSelected ? `${d.value.toFixed(1)} tCO\u2082/cap` : `${d.value.toFixed(1)}`)

    yOffset += h + gap
  })

  scrollToSelected(data, margin.top, barHeight, selectedBarHeight, gap)
}

function scrollToSelected(data, marginTop, bh, sbh, gap) {
  if (!scrollContainer.value) return
  const idx = data.findIndex(d => d.code === props.selectedCountryCode)
  if (idx === -1) return

  let selectedY = marginTop
  for (let i = 0; i < idx; i++) {
    selectedY += (data[i].code === props.selectedCountryCode ? sbh : bh) + gap
  }
  const containerH = scrollContainer.value.clientHeight
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
</style>
