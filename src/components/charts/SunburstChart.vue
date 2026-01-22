<template>
  <div class="chart">
    <svg ref="svgRef" width="500" height="500"></svg>
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
const width = 500
const height = 500
const radius = Math.min(width, height) / 2 - Math.max(margin.top, margin.right, margin.bottom, margin.left)
const sectorColors = {
  residential: '#63b3df',
  service: '#76d76b',
  industry: '#898989',
  transport: '#ffb56b'
};

function drawChart() {
  if (!props.data || !props.data.children || props.data.children.length === 0) return

  const svg = d3.select(svgRef.value)
  svg.selectAll('*').remove()

  const g = svg.append('g')
    .attr('transform', `translate(${width / 2},${height / 2})`)

  // Create partition layout
  const partition = d3.partition()
    .size([2 * Math.PI, radius])

  // Create arc generator
  const arc = d3.arc()
    .startAngle(d => d.x0)
    .endAngle(d => d.x1)
    .innerRadius(d => d.y0)
    .outerRadius(d => d.y1)

  // Convert data to hierarchy
  const root = d3.hierarchy(props.data)
    .sum(d => d.value || 0)
    .sort((a, b) => b.value - a.value)

  const filteredRoot = root.descendants().filter(d => {
    if (d.depth > 1 && d.parent.children.length <= 1) {
      return false;
    }
    return true;
  })

  // Apply partition layout
  partition(root)

  // Precompute max depth once
  const maxDepth = d3.max(filteredRoot, d => d.depth);

  // Create tooltip container outside SVG
  const tooltipDiv = d3.select('body').append('div')
    .attr('class', 'tooltip-container')

  // Hash function based on numeric value -> 0..1
  function hashValue(val) {
    const num = val || 0;
    let h = 0;
    const str = num.toString(); // convert number to string for hashing
    for (let i = 0; i < str.length; i++) {
      h = ((h << 5) - h + str.charCodeAt(i)) | 0;
    }
    return (Math.abs(h) % 1000) / 1000; // 0..0.999
  }

  // Draw segments
  const segments = g.selectAll('path')
  .data(filteredRoot)
  .enter()
  .append('path')
  .attr('d', arc)
  .style('fill', (d, i) => {
    if (d.depth === 0) return '#ffffff';

    // find sector name
    const sectorName = d.parent && d.parent.parent
      ? d.parent.parent.data.name.toLowerCase()
      : d.parent.data.name.toLowerCase();

    const baseHex = sectorColors[sectorName] || '#cccccc';
    const base = d3.color(baseHex);

    // depth-based brightness
    const depthT = d.depth / maxDepth;

    // SMALLER hue offset: ±20 degrees keeps it in family
    const hueOffset = hashValue(i * 137.5) * 40 - 20;  // -20..+20 degrees

    // Light saturation variation for subtle distinction
    const satOffset = hashValue(i * 251) * 0.2;        // 0..0.2 boost

    // convert to HSL, subtle changes
    let hsl = d3.hsl(base);
    hsl.h = (hsl.h + hueOffset + 360) % 360;           // Subtle hue variation
    hsl.s = Math.min(1, hsl.s + satOffset);            // Slightly more vivid
    hsl.l = 0.25 + 0.5 * depthT;                       // Depth contrast

    return hsl.toString();
  })
  .style('stroke', '#fff')
  .style('stroke-width', '1px')
  .style('cursor', 'pointer')
  .on('mouseover', function(event, d) {
    d3.select(this).style('opacity', 0.7)

    // Tooltip
    tooltipDiv.style('display', 'block')
      .html(`
        <div style="font-weight: bold;">${d.data.name}</div>
        <div>${d.value ? d.value.toFixed(2) + ' PJ' : ''}</div>
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

  g.selectAll('text')
  .data(filteredRoot.filter(d => d.depth > 0 && d.x1 - d.x0 > 0.05))
  .enter()
  .append('text')
  .attr('transform', d => {
    const x = (d.x0 + d.x1) / 2 * 180 / Math.PI;
    const y = (d.y0 + d.y1) / 2;
    const angle = x - 90;

    return `rotate(${angle},0,0)translate(${y + 12},0)${angle > 90 ? 'rotate(180)' : ''}`;
  })
  .attr('text-anchor', d => {
    const angle = (d.x0 + d.x1) / 2 * 180 / Math.PI;
    return angle > 90 && angle < 270 ? 'end' : 'start';
  })
  .attr('dy', '.35em')
  .style('font-size', '13px')
  .style('fill', '#333')
  .style('font-weight', 'bold')
  .text(d => d.data.name.length > 15 ? d.data.name.substring(0, 12) + '...' : d.data.name);
}

function getBranch(d) {
  while (d.depth > 1) d = d.parent;
  return d
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
