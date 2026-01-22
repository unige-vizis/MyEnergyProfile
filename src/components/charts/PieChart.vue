<template>
  <div class="chart">
    <svg ref="svgRef" width="400" height="400"></svg>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import * as d3 from 'd3'

const props = defineProps({
  data: {
    type: Object,
    default: () => ({})
  },
  year: {
    type: [String, Number],
    default: null
  }
})

const svgRef = ref(null)

const margin = { top: 20, right: 20, bottom: 20, left: 20 }
const width = 400
const height = 400
const radius = Math.min(width, height) / 2 - Math.max(margin.top, margin.right, margin.bottom, margin.left)
const sectorColors = {
  residential: '#63b3df',
  service: '#76d76b',
  industry: '#898989',
  transport: '#ffb56b'
}

function drawChart() {
  if (!props.data || !props.data.children || props.data.children.length === 0) return

  const svg = d3.select(svgRef.value)
  svg.selectAll('*').remove()

  const g = svg.append('g')
    .attr('transform', `translate(${width / 2},${height / 2})`)

  // Create color scale
  const color = d3.scaleOrdinal(d3.schemeCategory10)

  // Create pie layout
  const pie = d3.pie()
    .value(d => d.value)
    .sort(null)

  // Create arc generator
  const arc = d3.arc()
    .innerRadius(0)
    .outerRadius(radius)

  // Convert data to pie data
  const pieData = pie(props.data.children)

  // Create tooltip container outside SVG
  const tooltipDiv = d3.select('body').append('div')
    .attr('class', 'tooltip-container')

  // Draw segments
  const segments = g.selectAll('path')
    .data(pieData)
    .enter()
    .append('path')
    .attr('d', arc)
    .style('fill', (d, i) => sectorColors[d.data.name.toLowerCase()])
    .style('stroke', '#fff')
    .style('stroke-width', '2px')
    .style('cursor', 'pointer')
    .on('mouseover', function(event, d) {
      d3.select(this).style('opacity', 0.7)

      // Show tooltip following mouse
      tooltipDiv.style('display', 'block')
        .html(`
          <div style="font-weight: bold;">${d.data.name}</div>
          <div>${d.data.value ? d.data.value.toFixed(2) + ' PJ' : ''}</div>
        `)
    })
    .on('mousemove', function(event) {
      tooltipDiv
        .style('left', (event.pageX + 12) + 'px')
        .style('top', (event.pageY - 28) + 'px')
    })
    .on('mouseout', function() {
      d3.select(this).style('opacity', 1)
      tooltipDiv.style('display', 'none')
    })

  // Add labels
  const labelArc = d3.arc()
  .innerRadius(radius * 0.7)
  .outerRadius(radius * 0.7)

  g.selectAll('text')
    .data(pieData)
    .enter()
    .append('text')
    .attr('transform', d => `translate(${labelArc.centroid(d)})`)
    .attr('text-anchor', 'middle')
    .attr('dy', '0.35em')
    .style('font-size', '15px')
    .style('fill', '#fff')
    .style('font-weight', 'bold')
    .text(d => d.data.name)
}

onMounted(() => {
  nextTick(() => {
    drawChart()
  })
})

watch(() => [props.data, props.year], () => {
  nextTick(() => {
    drawChart()
  })
}, { deep: true })
</script>
