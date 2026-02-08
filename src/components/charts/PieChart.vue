<template>
  <div class="chart" ref="containerRef" style="width:100%;">
    <svg ref="svgRef" preserveAspectRatio="xMidYMid meet"></svg>
  </div>
  <!-- TODO - Matteo: Data Sources -->
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
  selectedSector: {
    type: String,
    default: "Residential"
  },
  country:{
    type: Object,
    default: null
  },
})

const svgRef = ref(null)
const containerRef = ref(null)
const svgWidth = ref(500)
const svgHeight = ref(500)
const margin = { top: 60, right: 20, bottom: 20, left: 60 }
// Keep a reference to the observer so we can disconnect it
const resizeObserverRef = ref(null)

function computedRadius(width, height) {
  return Math.min(width, height) / 2 - Math.max(margin.top, margin.right, margin.bottom, margin.left)
}

const energyColors = {
  // Gasoline family - yellow/orange progression
  motor: 'rgb(162, 158, 162)',                   // Your orange ✓
  jet: 'rgb(109, 151, 214)',                     // Lighter yellow-orange
  lpg: 'rgb(240, 220, 120)',

  electricity: 'rgb(99, 179, 223)',     // Cool blue ✓
  heat: 'rgb(255, 130, 130)',           // Pure coral red ✓
  biofuel: 'rgb(144, 210, 125)',        // Fresh green ✓
  gas: 'rgb(128, 128, 128)',            // Mid gray ✓
  coal: 'rgb(70, 70, 70)',              // Darker charcoal (vs gas)
  other: 'rgb(150, 180, 220)',          // Slate blue ✓

  // Oil family - brown/orange progression
  'Oil and oil products': 'rgb(236, 154, 111)',    // Rich brown
  'Heavy fuel oil': 'rgb(139, 99, 11)',           // Darker brown
  diesel: 'rgb(205, 149, 88)',                   // Saddle brown
}

function drawChart() {
  const selected = props.data.find(s => s?.name === props.selectedSector)?.energyType

  // determine current size
  const width = svgWidth.value
  const height = svgHeight.value
  const radius = computedRadius(width, height)

  if (!props.data || !selected || selected.length === 0) return

  const svg = d3.select(svgRef.value)
  svg.selectAll('*').remove()
  svg.attr('width', width).attr('height', height).attr('viewBox', `0 0 ${width} ${height}`)

  const g = svg.append('g')
    .attr('transform', `translate(${width / 2},${height / 2})`)

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
    .style('fill', (d) => {
      const colorMatch = Object.entries(energyColors).find(([colorLabel]) =>
        d.data.name.toLowerCase().includes(colorLabel.toLowerCase())
      );
      return colorMatch ? colorMatch[1] : '#fff';
    })
    .style('stroke', '#fff')
    .style('stroke-width', '1px')
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

  // Array to track occupied label positions
  const labelPositions = [];

  // TEXT LABELS - Smart collision detection
  g.selectAll('text')
    .data(pieData)
    .enter()
    .append('text')
    .attr('class', 'pie-label')
    .attr('transform', function(d, i) {
      const [x, y] = labelArc.centroid(d);
      const angle = Math.atan2(y, x);
      let r = outerRadius + labelOffset;

      // Find best position avoiding collisions
      let attempts = 0;
      let newX, newY;
      while (attempts < 5) { // max 5 reposition attempts
        newX = r * Math.cos(angle);
        newY = r * Math.sin(angle);

        // Check if too close to existing labels (within 25px)
        const tooClose = labelPositions.some(pos =>
          Math.hypot(pos.x - newX, pos.y - newY) < 25
        );

        if (!tooClose) break;
        // Nudge outward if collision
        r += 12;
        attempts++;
      }

      // Save this position
      labelPositions.push({x: newX, y: newY});
      return `translate(${newX}, ${newY})`;
    })
    .attr('text-anchor', d => {
      const [x, y] = labelArc.centroid(d);
      return x >= 0 ? 'start' : 'end';
    })
    .attr('dy', '0.35em')
    .style('font-size', '15px')
    .text(d => d.data.name);

  // POLYLINES - Match adjusted text positions
  g.selectAll('polyline')
    .data(pieData)
    .enter()
    .append('polyline')
    .attr('points', function(d, i) {
      const pos = labelPositions[i]; // Use saved position
      if (!pos) return '';

      const [x, y] = labelArc.centroid(d);
      const angle = Math.atan2(y, x);

      const x1 = outerRadius * Math.cos(angle);
      const y1 = outerRadius * Math.sin(angle);
      const x2 = (outerRadius + labelOffset / 2) * Math.cos(angle);
      const y2 = (outerRadius + labelOffset / 2) * Math.sin(angle);

      // Polyline ends 15px BEFORE text position for bigger gap
      const gap = 5;
      const x3 = pos.x - gap * Math.cos(angle);
      const y3 = pos.y - gap * Math.sin(angle);

      return [[x1, y1], [x2, y2], [x3, y3]];
    })
    .style('fill', 'none')
    .style('stroke', 'black')
    .style('stroke-width', '1');
}

onMounted(() => {
  nextTick(() => {
    // initial sizing based on container
    const rect = containerRef.value ? containerRef.value.getBoundingClientRect() : { width: 500, height: 500 }
    const size = Math.max(200, Math.min(rect.width, 400))
    svgWidth.value = size * 1.5
    svgHeight.value = size * 0.8

    // observe container resize
    const ro = new ResizeObserver(entries => {
      for (const entry of entries) {
        const r = entry.contentRect
        const s = Math.max(200, Math.min(r.width, 400))
        svgWidth.value = s * 1.5
        svgHeight.value = s * 0.8
        nextTick(() => drawChart())
      }
    })
    if (containerRef.value) ro.observe(containerRef.value)
    // keep ref for cleanup
    resizeObserverRef.value = ro

    drawChart()
  })
})

watch(() => [props.data, props.year, props.selectedSector, props.country], () => {
  nextTick(() => {
    drawChart()
  })
}, { deep: true })

onUnmounted(() => {
  if (resizeObserverRef.value) {
    try { resizeObserverRef.value.disconnect() } catch (e) {}
  }
  d3.selectAll('.tooltip-container').remove()
})
</script>
