<template>
  <div class="chart">
    <svg ref="svgRef" width="550" height="400"></svg>
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
  },
  selectedSector: {
    type: String,
    default: "Residential"
  }
})

const svgRef = ref(null)

const margin = { top: 50, right: 80, bottom: 80, left: 50 }
const width = 550
const height = 400
const radius = Math.min(width, height) / 2 - Math.max(margin.top, margin.right, margin.bottom, margin.left)
const sectorColors = {
  residential: '#63b3df',
  service: '#76d76b',
  industry: '#898989',
  transport: '#ffb56b'
}

function drawChart() {
  const selected = props.data.find(s => s?.name === props.selectedSector)?.energyType

  if (!props.data || !selected || selected.length === 0) return

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
  // children = props.data
  const pieData = pie(selected)

  // Create tooltip container outside SVG
  const tooltipDiv = d3.select('body').append('div')
    .attr('class', 'tooltip-container')

  // Draw segments
  const segments = g.selectAll('path')
    .data(pieData)
    .enter()
    .append('path')
    .attr('d', arc)
    .style('fill', (d, i) => {
      const baseColor = sectorColors[props.selectedSector.toLowerCase()];
      const colorScale = d3.scaleSequential()
          .domain([0, selected.length - 1])
          .interpolator(d3.interpolateRgb(d3.color(baseColor).brighter(1), baseColor));
      return colorScale(i);
    })
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

  const outerRadius = radius; // same as used for the pie slices
  const labelOffset = 20;     // distance from the slice edge

    g.selectAll('text')
  .data(pieData)
  .enter()
  .append('text')
  .attr('transform', d => {
    const [x, y] = labelArc.centroid(d);  // centroid of slice
    const angle = Math.atan2(y, x);
    const r = outerRadius + labelOffset;  // move text outside the pie
    const newX = r * Math.cos(angle);
    const newY = r * Math.sin(angle);
    return `translate(${newX}, ${newY})`;
  })
  .attr('text-anchor', d => {
    const [x, y] = labelArc.centroid(d);
    return x >= 0 ? 'start' : 'end'; // left/right alignment
  })
  .attr('dy', '0.35em')
  .style('font-size', '15px')
  .text(d => d.data.name);

  g.selectAll('polyline')
  .data(pieData)
  .enter()
  .append('polyline')
  .attr('points', d => {
    const [x, y] = labelArc.centroid(d); // slice centroid
    const angle = Math.atan2(y, x);

    const x1 = outerRadius * Math.cos(angle); // start at slice edge
    const y1 = outerRadius * Math.sin(angle);

    const x2 = (outerRadius + labelOffset / 2) * Math.cos(angle); // optional midpoint
    const y2 = (outerRadius + labelOffset / 2) * Math.sin(angle);

    const x3 = (outerRadius + labelOffset) * Math.cos(angle); // text position
    const y3 = (outerRadius + labelOffset) * Math.sin(angle);

    return [[x1, y1], [x2, y2], [x3, y3]];
  })
  .style('fill', 'none')
  .style('stroke', 'black');

}

onMounted(() => {
  nextTick(() => {
    drawChart()
  })
})

watch(() => [props.data, props.year, props.selectedSector], () => {
  nextTick(() => {
    drawChart()
  })
}, { deep: true })
</script>
