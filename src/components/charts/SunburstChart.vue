<template>
  <div class="chart" ref="containerRef" style="width:100%;">
    <svg ref="svgRef" preserveAspectRatio="xMidYMid meet"></svg>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import * as d3 from 'd3'

const props = defineProps({
  data: {
    type: Object,
    default: () => ({})
  },
  year: {
    type: [String, Number],
    default: null
  },
  country: {
    type: Object,
    default: null
  }
})

const svgRef = ref(null)
const containerRef = ref(null)
const margin = { top: 60, right: 20, bottom: 20, left: 60 }
const svgWidth = ref(500)
const svgHeight = ref(500)

function computedRadius(width, height) {
  return Math.min(width, height) / 2 - Math.max(margin.top, margin.right, margin.bottom, margin.left)
}
const sectorColors = {
  residential: '#63b3df',
  service: '#76d76b',
  industry: '#898989',
  transport: '#ffb56b'
};

function drawChart() {
  if (!props.data || !props.data.children || props.data.children.length === 0) return

  // determine current size
  const width = svgWidth.value
  const height = svgHeight.value
  const radius = computedRadius(width, height)

  const svg = d3.select(svgRef.value)
  svg.selectAll('*').remove()
  svg.attr('width', width).attr('height', height).attr('viewBox', `0 0 ${width} ${height}`)

  const g = svg.append('g')
    .attr('transform', `translate(${width / 2},${height / 2})`)

  // Create partition layout
  const partition = d3.partition()
    .size([2 * Math.PI, radius * 1.2])

  // Create arc generator
  const arc = d3.arc()
    .startAngle(d => d.x0)
    .endAngle(d => d.x1)
    .innerRadius(d => d.y0)
    .outerRadius(d => d.y1);

  // Convert data to hierarchy
  const root = d3.hierarchy(props.data)
    .sum(d => d.children ? 0 : d.value)
    .sort((a, b) => b.value - a.value);

  partition(root);

  // Precompute max depth once
  const maxDepth = d3.max(root.descendants(), d => d.depth);

  // Ensure single tooltip container
  d3.selectAll('.tooltip-container').remove()
  const tooltipDiv = d3.select('body').append('div')
    .attr('class', 'tooltip-container')

  const segments = g.selectAll('path')
  .data(root.descendants())
  .enter()
  .append('path')
  .attr('d', arc)
  .style('fill', d => d.depth === 2 ? sectorColors[d.parent.data.name.toLowerCase()] : (d.depth === 1 ? sectorColors[d.data.name.toLowerCase()] : "none"))
  .style('stroke', '#fff')
  .style('stroke-width', '1px')
  .style('cursor', 'pointer')
  .on('mouseover', function(event, d) {
    d3.select(this).style('opacity', 0.7);
    tooltipDiv
      .style('display', 'block')
      .html(`
        <div style="font-weight:bold">
          ${d.data.name || 'Unknown'}
        </div>
        <div>
          ${(d.value || 0).toFixed(2)} PJ
        </div>
      `);
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

  g.selectAll('text')
  .data(root.descendants().filter(d => d.depth > 0 && d.x1 - d.x0 > 0.05))
  .enter()
  .append('text')
  .attr('transform', d => {
    const midAngleRad = (d.x0 + d.x1) / 2;
    const midRadius = (d.y0 + d.y1) / 2;
    const midAngleDeg = midAngleRad * 180 / Math.PI;

    return `
      rotate(${midAngleDeg - 90})
      translate(${midRadius}, 0)
      rotate(${midAngleDeg < 180 ? 0 : 180})
    `;
  })
  .attr('text-anchor', 'middle')
  .attr('dy', '0.35em')
  .style('font-size', d => d.depth === 2 ? '10px' : '13px')
  .style('fill', '#333')
  .style('font-weight', 'bold')
  .text(d => d.data.name.length > 15 ? d.data.name.substring(0, 12) + '...' : d.data.name);
}

onMounted(() => {
  nextTick(() => {
    // initial sizing based on container
    const rect = containerRef.value ? containerRef.value.getBoundingClientRect() : { width: 500, height: 500 }
    const size = Math.max(200, Math.min(rect.width, 500))
    svgWidth.value = size
    svgHeight.value = size

    // observe container resize
    const ro = new ResizeObserver(entries => {
      for (const entry of entries) {
        const r = entry.contentRect
        const s = Math.max(200, Math.min(r.width, 500))
        svgWidth.value = s
        svgHeight.value = s
        nextTick(() => drawChart())
      }
    })
    if (containerRef.value) ro.observe(containerRef.value)
    // keep ref for cleanup
    resizeObserverRef.value = ro

    drawChart()
  })
})

watch(() => [props.data, props.year, props.country], () => {
  nextTick(() => {
    drawChart()
  })
}, { deep: true })

// Keep a reference to the observer so we can disconnect it
const resizeObserverRef = ref(null)

onUnmounted(() => {
  if (resizeObserverRef.value) {
    try { resizeObserverRef.value.disconnect() } catch (e) {}
  }
  d3.selectAll('.tooltip-container').remove()
})
</script>
