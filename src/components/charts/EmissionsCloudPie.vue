<template>
  <div v-if="!hasData" class="no-data">
    <span class="material-symbols-outlined">cloud_off</span>
    <p>No per-capita emissions data available for this country.</p>
  </div>
  <div v-else class="chart-wrapper">
    <div class="chart-container">
      <div ref="chartRef" class="chart-svg"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
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
  { key: 'residential', label: 'Residential', color: '#63b3df' },
  { key: 'transport', label: 'Transport', color: '#ffb56b' },
  { key: 'industry', label: 'Industry', color: '#898989' },
  { key: 'services', label: 'Services', color: '#76d76b' }
]

function renderChart() {
  if (!chartRef.value || !hasData.value) return

  d3.select(chartRef.value).selectAll('*').remove()

  const containerWidth = chartRef.value.clientWidth || 460
  const width = Math.min(containerWidth, 460)
  const height = 450
  const cx = width / 2
  const pieCy = 180

  const svg = d3.select(chartRef.value)
    .append('svg')
    .attr('width', width)
    .attr('height', height)
    .attr('viewBox', `0 0 ${width} ${height}`)

  const data = props.emissionsData
  const sectors = SECTORS.filter(s => data[s.key] != null && data[s.key] > 0)
  if (sectors.length === 0) return

  const total = sectors.reduce((sum, s) => sum + data[s.key], 0)

  const outerRadius = 95
  const innerRadius = outerRadius * 0.38

  // ─── DEFS ───
  const defs = svg.append('defs')

  const cloudFilter = defs.append('filter')
    .attr('id', 'cloud-soft')
    .attr('x', '-30%').attr('y', '-30%')
    .attr('width', '160%').attr('height', '160%')
  cloudFilter.append('feGaussianBlur')
    .attr('in', 'SourceGraphic').attr('stdDeviation', '6')

  const smokeFilter = defs.append('filter')
    .attr('id', 'smoke-soft')
    .attr('x', '-50%').attr('y', '-50%')
    .attr('width', '200%').attr('height', '200%')
  smokeFilter.append('feGaussianBlur')
    .attr('in', 'SourceGraphic').attr('stdDeviation', '4')

  // ─── LAYER 1: Large CO2 cloud backdrop ───
  const cloudBg = svg.append('g').attr('filter', 'url(#cloud-soft)')

  const puffs = [
    { x: 0, y: 0, r: outerRadius + 40 },
    { x: -70, y: 12, r: 58 },
    { x: 70, y: 12, r: 58 },
    { x: -45, y: -42, r: 52 },
    { x: 45, y: -42, r: 52 },
    { x: 0, y: -58, r: 46 },
    { x: -90, y: -2, r: 40 },
    { x: 90, y: -2, r: 40 },
    { x: -30, y: 52, r: 44 },
    { x: 30, y: 52, r: 44 },
    { x: 0, y: 60, r: 38 },
    { x: -60, y: 45, r: 32 },
    { x: 60, y: 45, r: 32 },
  ]

  puffs.forEach(p => {
    cloudBg.append('circle')
      .attr('cx', cx + p.x)
      .attr('cy', pieCy + p.y)
      .attr('r', p.r)
      .attr('fill', '#90a4ae')
      .attr('fill-opacity', 0.10)
  })

  // CO2 label floating above the pie in the cloud
  svg.append('text')
    .attr('x', cx)
    .attr('y', pieCy - outerRadius - 28)
    .attr('text-anchor', 'middle')
    .attr('font-size', '15px')
    .attr('font-weight', '700')
    .attr('letter-spacing', '2px')
    .attr('fill', '#78909c')
    .attr('fill-opacity', 0.45)
    .text('CO\u2082')

  // ─── LAYER 2: Smoke trails rising from sources to cloud ───
  const groundY = 395
  const smokeGroup = svg.append('g').attr('filter', 'url(#smoke-soft)')

  // Left trail (car exhaust -> cloud)
  const leftBaseX = cx - 80
  for (let i = 0; i < 8; i++) {
    const t = i / 7
    const y = groundY - 50 - t * (groundY - 50 - (pieCy + outerRadius + 15))
    const drift = Math.sin(t * Math.PI * 1.5) * 18
    const x = leftBaseX + t * 50 + drift
    const r = 6 + t * 22
    smokeGroup.append('circle')
      .attr('cx', x).attr('cy', y).attr('r', r)
      .attr('fill', '#90a4ae')
      .attr('fill-opacity', 0.04 + t * 0.05)
  }

  // Right trail (factory chimney -> cloud)
  const rightBaseX = cx + 80
  for (let i = 0; i < 8; i++) {
    const t = i / 7
    const y = groundY - 65 - t * (groundY - 65 - (pieCy + outerRadius + 15))
    const drift = Math.sin(t * Math.PI * 1.5 + 1) * 15
    const x = rightBaseX - t * 50 + drift
    const r = 5 + t * 20
    smokeGroup.append('circle')
      .attr('cx', x).attr('cy', y).attr('r', r)
      .attr('fill', '#90a4ae')
      .attr('fill-opacity', 0.04 + t * 0.05)
  }

  // ─── LAYER 3: Pie chart ───
  const pieData = sectors.map(s => ({ ...s, value: data[s.key] }))
  const pie = d3.pie().value(d => d.value).padAngle(0.03).sort(null)
  const arcs = pie(pieData)

  const arcGen = d3.arc().innerRadius(innerRadius).outerRadius(outerRadius)
  const labelArcGen = d3.arc()
    .innerRadius(outerRadius + 32)
    .outerRadius(outerRadius + 32)

  arcs.forEach((arcData) => {
    const si = arcData.data

    svg.append('path')
      .attr('d', arcGen(arcData))
      .attr('transform', `translate(${cx}, ${pieCy})`)
      .attr('fill', si.color)
      .attr('stroke', si.color)
      .attr('stroke-width', 1.5)

    const centroid = labelArcGen.centroid(arcData)
    const labelX = cx + centroid[0]
    const labelY = pieCy + centroid[1]
    const midAngle = (arcData.startAngle + arcData.endAngle) / 2
    const textAnchor = midAngle < Math.PI ? 'start' : 'end'

    svg.append('text')
      .attr('x', labelX).attr('y', labelY - 7)
      .attr('text-anchor', textAnchor)
      .attr('font-size', '12px')
      .attr('font-weight', '600')
      .attr('fill', si.color)
      .text(si.label)

    svg.append('text')
      .attr('x', labelX).attr('y', labelY + 8)
      .attr('text-anchor', textAnchor)
      .attr('font-size', '11px')
      .attr('fill', '#666')
      .text(`${si.value.toFixed(2)} tCO\u2082/cap`)
  })

  // Center total
  svg.append('text')
    .attr('x', cx).attr('y', pieCy - 6)
    .attr('text-anchor', 'middle')
    .attr('font-size', '20px')
    .attr('font-weight', '700')
    .attr('fill', '#333')
    .text(`${total.toFixed(1)}`)

  svg.append('text')
    .attr('x', cx).attr('y', pieCy + 14)
    .attr('text-anchor', 'middle')
    .attr('font-size', '11px')
    .attr('font-weight', '500')
    .attr('fill', '#666')
    .text('tCO\u2082/cap')

  // ─── LAYER 4: Ground scene ───

  // Subtle ground line
  svg.append('line')
    .attr('x1', 30).attr('y1', groundY)
    .attr('x2', width - 30).attr('y2', groundY)
    .attr('stroke', '#b0bec5')
    .attr('stroke-width', 1)
    .attr('stroke-opacity', 0.4)
    .attr('stroke-dasharray', '6,4')

  // ── Car (left side) ──
  const carG = svg.append('g')
    .attr('transform', `translate(${cx - 115}, ${groundY})`)

  // Body
  carG.append('path')
    .attr('d', 'M3,-3 L3,-11 L14,-11 L20,-21 L38,-21 L44,-11 L52,-11 L52,-3 Z')
    .attr('fill', '#546e7a').attr('fill-opacity', 0.55)
    .attr('stroke', '#37474f').attr('stroke-width', 0.8).attr('stroke-opacity', 0.3)

  // Windshield
  carG.append('path')
    .attr('d', 'M16,-11 L21,-19 L27,-19 L27,-11 Z')
    .attr('fill', '#b0bec5').attr('fill-opacity', 0.35)

  // Rear window
  carG.append('path')
    .attr('d', 'M29,-19 L36,-19 L41,-11 L29,-11 Z')
    .attr('fill', '#b0bec5').attr('fill-opacity', 0.3)

  // Wheels
  carG.append('circle').attr('cx', 16).attr('cy', -1).attr('r', 5)
    .attr('fill', '#263238').attr('fill-opacity', 0.6)
  carG.append('circle').attr('cx', 16).attr('cy', -1).attr('r', 2.5)
    .attr('fill', '#546e7a').attr('fill-opacity', 0.4)
  carG.append('circle').attr('cx', 40).attr('cy', -1).attr('r', 5)
    .attr('fill', '#263238').attr('fill-opacity', 0.6)
  carG.append('circle').attr('cx', 40).attr('cy', -1).attr('r', 2.5)
    .attr('fill', '#546e7a').attr('fill-opacity', 0.4)

  // Tailpipe
  carG.append('rect')
    .attr('x', 50).attr('y', -5).attr('width', 6).attr('height', 3).attr('rx', 1)
    .attr('fill', '#455a64').attr('fill-opacity', 0.5)

  // Exhaust puffs (small, immediate)
  ;[
    { x: 59, y: -6, r: 3.5 },
    { x: 64, y: -9, r: 5 },
    { x: 67, y: -14, r: 4.5 },
    { x: 70, y: -20, r: 4 },
  ].forEach((p, i) => {
    carG.append('circle')
      .attr('cx', p.x).attr('cy', p.y).attr('r', p.r)
      .attr('fill', '#78909c').attr('fill-opacity', 0.15 - i * 0.02)
  })

  // Headlight glow
  carG.append('circle')
    .attr('cx', 4).attr('cy', -7).attr('r', 2)
    .attr('fill', '#ffcc02').attr('fill-opacity', 0.4)

  // ── Factory (right side) ──
  const facG = svg.append('g')
    .attr('transform', `translate(${cx + 55}, ${groundY})`)

  // Main building
  facG.append('rect')
    .attr('x', 0).attr('y', -32).attr('width', 45).attr('height', 32).attr('rx', 2)
    .attr('fill', '#455a64').attr('fill-opacity', 0.45)
    .attr('stroke', '#37474f').attr('stroke-width', 0.8).attr('stroke-opacity', 0.25)

  // Tall chimney
  facG.append('rect')
    .attr('x', 7).attr('y', -60).attr('width', 10).attr('height', 28).attr('rx', 1)
    .attr('fill', '#37474f').attr('fill-opacity', 0.5)

  // Chimney cap
  facG.append('rect')
    .attr('x', 5).attr('y', -62).attr('width', 14).attr('height', 3).attr('rx', 1)
    .attr('fill', '#37474f').attr('fill-opacity', 0.55)

  // Second shorter chimney
  facG.append('rect')
    .attr('x', 30).attr('y', -48).attr('width', 7).attr('height', 16).attr('rx', 1)
    .attr('fill', '#37474f').attr('fill-opacity', 0.45)

  // Windows (two rows)
  ;[
    { x: 4, y: -26, w: 8, h: 6 },
    { x: 15, y: -26, w: 8, h: 6 },
    { x: 26, y: -26, w: 8, h: 6 },
    { x: 4, y: -16, w: 8, h: 6 },
    { x: 15, y: -16, w: 8, h: 6 },
    { x: 26, y: -16, w: 8, h: 6 },
  ].forEach(w => {
    facG.append('rect')
      .attr('x', w.x).attr('y', w.y).attr('width', w.w).attr('height', w.h).attr('rx', 1)
      .attr('fill', '#ffc107').attr('fill-opacity', 0.3)
  })

  // Door
  facG.append('rect')
    .attr('x', 18).attr('y', -9).attr('width', 9).attr('height', 9).attr('rx', 1)
    .attr('fill', '#37474f').attr('fill-opacity', 0.3)

  // Chimney smoke puffs (small, immediate above chimney)
  ;[
    { x: 12, y: -67, r: 5 },
    { x: 14, y: -75, r: 6 },
    { x: 11, y: -83, r: 5.5 },
    { x: 34, y: -53, r: 4 },
    { x: 36, y: -60, r: 5 },
  ].forEach((p, i) => {
    facG.append('circle')
      .attr('cx', p.x).attr('cy', p.y).attr('r', p.r)
      .attr('fill', '#78909c').attr('fill-opacity', 0.14 - i * 0.015)
  })

  // ── Flames (between car and factory, near ground) ──
  const flameG = svg.append('g')
    .attr('transform', `translate(${cx + 42}, ${groundY})`)

  ;[
    { x: -4, s: 0.9, fill: '#e74c3c', op: 0.30 },
    { x: 3, s: 1.2, fill: '#e67e22', op: 0.35 },
    { x: 9, s: 0.7, fill: '#f39c12', op: 0.28 },
    { x: -9, s: 0.6, fill: '#f39c12', op: 0.22 },
  ].forEach(f => {
    flameG.append('path')
      .attr('d', 'M0,0 C-3,-6 -5,-13 -2,-19 C-1,-21 1,-21 2,-19 C5,-13 3,-6 0,0 Z')
      .attr('transform', `translate(${f.x}, 0) scale(${f.s})`)
      .attr('fill', f.fill).attr('fill-opacity', f.op)
  })

  // Inner bright core of the main flame
  flameG.append('path')
    .attr('d', 'M0,0 C-1.5,-4 -2,-8 -0.5,-12 C0,-13 0.5,-13 1,-12 C2,-8 1.5,-4 0,0 Z')
    .attr('transform', 'translate(3, 0) scale(1.1)')
    .attr('fill', '#fff176').attr('fill-opacity', 0.3)

  // Year label
  if (data.year) {
    svg.append('text')
      .attr('x', cx).attr('y', height - 8)
      .attr('text-anchor', 'middle')
      .attr('font-size', '11px')
      .attr('fill', '#999')
      .text(`Data year: ${data.year}`)
  }
}

watch(() => [props.emissionsData, props.countryName], async () => {
  await nextTick()
  renderChart()
  if (chartRef.value && !resizeObserver) {
    resizeObserver = new ResizeObserver(() => { renderChart() })
    resizeObserver.observe(chartRef.value)
  }
}, { deep: true })

onMounted(() => {
  renderChart()
  if (chartRef.value) {
    resizeObserver = new ResizeObserver(() => { renderChart() })
    resizeObserver.observe(chartRef.value)
  }
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
  min-height: 200px;
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
