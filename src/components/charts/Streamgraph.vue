<template>
  <div class="violin-chart">
    <svg :width="width" :height="height" ref="svgRef"></svg>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import * as d3 from 'd3'

const props = defineProps({
  data: {
    type: Array,
    default: () => []
  },
  width: {
    type: Number,
    default: 1000
  },
  height: {
    type: Number,
    default: 400
  }
})

const svgRef = ref(null)

const margin = { top: 20, right: 300, bottom: 40, left: 90 }
const innerWidth = props.width - margin.left - margin.right
const innerHeight = props.height - margin.top - margin.bottom

function drawChart() {
  if (!svgRef.value || !props.data.length) return

  const svg = d3.select(svgRef.value)
  svg.selectAll('*').remove()

  const g = svg.append('g')
    .attr('transform', `translate(${margin.left},${margin.top})`)

  // Define custom colors for end uses (add or modify as needed)
  const colorMap = {
    'Cooking': '#FF6B6B',
    'Lighting': '#4ECDC4',
    'Space heating': '#45B7D1',
    'Water heating': '#96CEB4',
    'Space cooling': '#FFEAA7',
    'Other': '#DDA0DD',
    'Total final use': '#98D8C8',
    'Iron and steel': '#FF9999',
    'Chemical and petrochemical': '#66B3FF',
    'Non-ferrous metals': '#99FF99',
    'Non-metallic minerals': '#FFCC99',
    'Transport equipment': '#FF99CC',
    'Machinery': '#CC99FF',
    'Food and tobacco': '#99FFFF',
    'Paper, pulp and printing': '#FFFF99',
    'Wood and wood products': '#FF6666',
    'Construction': '#66FF66',
    'Textile and leather': '#6666FF',
    'Passenger cars': '#FFB366',
    'Freight trucks': '#66FFB3',
    'Light trucks': '#B366FF',
    'Motorcycles': '#FF66B3',
    'Buses': '#66FF66',
    'Rail transport': '#FFB3B3',
    'Domestic aviation': '#B3FFB3',
    'Road freight': '#B3B3FF',
    'Inland waterways': '#FFFFB3',
    'Sea transport': '#FFB3FF'
  }

  // Prepare data: each item has name and years object
  const data = props.data.map(d => ({
    name: d.name,
    years: d.years || {}
  })).filter(d => Object.keys(d.years).length > 0)

  if (!data.length) return

  // Get all years
  const allYears = Array.from(new Set(data.flatMap(d => Object.keys(d.years)))).sort()

  // Get all end uses
  const endUses = data.map(d => d.name)

  // Prepare data for stack: array of objects, each with year and values for each end use
  const stackData = allYears.map(year => {
    const obj = { year }
    endUses.forEach(endUse => {
      const d = data.find(d => d.name === endUse)
      obj[endUse] = d && d.years[year] !== null && !isNaN(d.years[year]) ? d.years[year] : 0
    })
    return obj
  })

  // Stack the data
  const stack = d3.stack()
    .keys(endUses)
    .offset(d3.stackOffsetWiggle)
    .order(d3.stackOrderInsideOut)

  const layers = stack(stackData)

  // Scales
  const x = d3.scalePoint()
    .domain(allYears)
    .range([0, innerWidth])

  const y = d3.scaleLinear()
    .domain(d3.extent(layers.flat().flat()))
    .range([innerHeight, 0])
    .nice()

  // Area generator
  const area = d3.area()
    .x(d => x(d.data.year))
    .y0(d => y(d[0]))
    .y1(d => y(d[1]))
    .curve(d3.curveCatmullRom)

  // Add X axis
  g.append('g')
    .attr('transform', `translate(0,${innerHeight})`)
    .call(d3.axisBottom(x))

  // Add Y axis
  g.append('g')
    .call(d3.axisLeft(y))

  // Draw layers
  g.selectAll('path')
    .data(layers)
    .enter().append('path')
    .attr('d', area)
    .style('fill', d => colorMap[d.key] || d3.schemeCategory10[endUses.indexOf(d.key) % 10])
    .style('opacity', 0.8)
    .style('stroke', 'white')
    .style('stroke-width', 0.5)

  // Add legend
  const legend = g.append('g')
    .attr('transform', `translate(0, ${innerHeight + 40})`)

  const legendItems = legend.selectAll('.legend-item')
    .data(layers)
    .enter().append('g')
    .attr('class', 'legend-item')
    .attr('transform', (d, i) => {
      return `translate(${props.width - margin.right - 80}, ${i * 25 - 350})`
    })

  legendItems.append('rect')
    .attr('width', 18)
    .attr('height', 18)
    .style('fill', d => colorMap[d.key] || d3.schemeCategory10[endUses.indexOf(d.key) % 10])

  legendItems.append('text')
    .attr('x', 24)
    .attr('y', 9)
    .attr('dy', '0.35em')
    .style('font-size', '12px')
    .text(d => d.key)
}

onMounted(() => {
  nextTick(() => {
    drawChart()
  })
})

watch(() => props.data, () => {
  nextTick(() => {
    drawChart()
  })
}, { deep: true })
</script>

<style scoped>
.violin-chart {
  display: flex;
  justify-content: center;
}
</style>
