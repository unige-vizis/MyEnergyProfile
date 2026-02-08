<template>
  <div class="prices-focus-chart" ref="containerRef" style="width:100%;">
    <div class="chart-header">
      <div class="kpi">
        <!-- show KPI for the currently selected series; do not fall back to the other series' value -->
        <div v-if="focusedPoint && props.activeSeries === 'electricity'">
          <div class="kpi-value" v-if="focusedPoint.electricity != null">
            {{ focusedPoint.electricity }} <span class="unit">US¢/kWh</span>
          </div>
          <div class="kpi-value" v-else>No electricity data</div>
        </div>

        <div v-else-if="focusedPoint && props.activeSeries === 'energy'">
          <div class="kpi-value" v-if="mean(focusedPoint.CPI0450) != null">
            Energy CPI: {{ mean(focusedPoint.CPI0450).toFixed(1) }}
          </div>
          <div class="kpi-value" v-else>No CPI data</div>
        </div>

        <div class="kpi-sub" v-if="focusedPoint">{{ props.focusYear || focusedPoint.year }}</div>
      </div>
    </div>

    <div class="chart-area" ref="chartRef" tabindex="0" role="img" :aria-label="ariaLabel"></div>

    <!-- live region for accessibility -->
    <div class="sr-only" ref="liveRef" aria-live="polite"></div>
  </div>
</template>

<script setup>
import * as d3 from 'd3'
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'

const props = defineProps({
  data: { type: Array, default: () => [] }, // [{year: 1996, electricity: 12.3, CPI0450: [60.3, 60.5, 57.9, 59.5]},...]
  focusYear: { type: [Number, null], default: null },
  series: { type: String, default: 'energy' },
  view: { type: String, default: 'annual' },
  width: { type: Number, default: null },
  height: { type: Number, default: 320 },
  activeSeries: { type: String, default: 'energy' } // 'electricity' | 'energy'
})

const emits = defineEmits(['update:focusYear', 'rangeChange', 'update:series'])

const containerRef = ref(null)
const chartRef = ref(null)
const liveRef = ref(null)
let svg = null
let zoomBehavior = null
let currentZoom = null
let focusOnYear = null
// runtime hook: set inside draw() so watchers and external helpers can update focus visuals
let updateFocusVisuals = null

const M = { top: 20, right: 14, bottom: 40, left: 56 }
const TRANSITION_MS = 300

const data = computed(() => (props.data || []).slice().sort((a, b) => a.year - b.year))
const years = computed(() => data.value.map(d => d.year))
const electricity_values = computed(() => data.value.map(d => d.electricity))

// Helper: compute mean of an array (safe)
function mean(arr) {
  if (!Array.isArray(arr)) return arr == null ? null : Number(arr)
  const nums = arr.filter(v => v != null).map(Number)
  return nums.length ? nums.reduce((s, v) => s + v, 0) / nums.length : null
}

// Annualised energy CPI (CPI0450 is stored as quarterly arrays) — used with a separate y-axis
const energy_values_annual = computed(() => data.value.map(d => mean(d.CPI0450)))
const latest = computed(() => (data.value.length ? data.value[data.value.length - 1] : null))
const focusedPoint = computed(() => {
  // If caller explicitly set a focus year, use it (fall back to latest if missing)
  if (props.focusYear) return data.value.find(d => d.year === props.focusYear) || latest.value

  // No explicit focus year — prefer the most recent point that contains data for the
  // currently active series so the KPI and focus visuals reflect the selected series.
  if (props.activeSeries === 'electricity') {
    for (let i = data.value.length - 1; i >= 0; i--) {
      const d = data.value[i]
      if (d && d.electricity != null) return d
    }
    return latest.value
  }

  // default: most recent (works for energy / CPI which is usually present on latest)
  return latest.value
})

const ariaLabel = computed(() => {
  if (!latest.value) return 'No price data available'
  return `Electricity price ${latest.value} US cents per kilowatt hour in ${latest.year}. Use controls to zoom and focus.`
})

const svgWidth = ref(500)
const svgHeight = ref(500)

function draw() {
  if (!chartRef.value) return
  d3.select(chartRef.value).selectAll('*').remove()

  const containerWidth = svgWidth.value || Math.max(420, (containerRef.value?.clientWidth || 720) - 0)
  const height = svgHeight.value
  const innerW = containerWidth - M.left - M.right
  const innerH = height - M.top - M.bottom - 12

  svg = d3.select(chartRef.value)
    .append('svg')
    .attr('width', containerWidth)
    .attr('height', height)
    .attr('viewBox', `0 0 ${containerWidth} ${height}`)
    .attr('preserveAspectRatio', 'xMidYMid meet')

  const main = svg.append('g').attr('class', 'main').attr('transform', `translate(${M.left},${M.top})`)

  // Scales
  const x = d3.scaleLinear()
    .domain(d3.extent(years.value.length ? years.value : [new Date().getFullYear() - 5, new Date().getFullYear()]))
    .range([0, innerW])
    .nice()

  // Single Y scale — domain selected based on activeSeries
  // robust numeric min/max (ignore null/undefined)
  function numericExtent(arr, fallbackMin = 0, fallbackMax = 1) {
    const nums = (arr || []).filter(v => v != null && Number.isFinite(Number(v))).map(Number)
    if (!nums.length) return [fallbackMin, fallbackMax]
    return [d3.min(nums), d3.max(nums)]
  }

  const [yMin, yMax] = props.activeSeries === 'energy'
    ? numericExtent(energy_values_annual.value, 0, 1)
    : numericExtent(electricity_values.value, 0, 1)

  const y = d3.scaleLinear()
    .domain([yMin, yMax])
    .nice()
    .range([innerH, 0])

  // Axes
  // helper to format x ticks; if fractional year present show quarter
  function formatXT(t) {
    const year = Math.floor(t)
    const frac = t - year
    if (Math.abs(frac) < 1e-6) return d3.format('d')(year)
  }
  const xAxis = d3.axisBottom(x).ticks(Math.min(10, Math.max(4, years.value.length))).tickFormat(formatXT)
  const yAxis = d3.axisLeft(y).ticks(4)

  main.append('g').attr('class', 'y axis').call(yAxis)
  const xAxisG = main.append('g').attr('class', 'x axis').attr('transform', `translate(0,${innerH})`).call(xAxis)

  // axis label (contextual)
  const yLabelText = props.activeSeries === 'energy' ? 'Energy CPI (index)' : 'US cents / kWh'
  main.append('text').attr('class', 'y-label').attr('transform', 'rotate(-90)').attr('y', -54).attr('x', -innerH/2).attr('dy', '1em').style('text-anchor','middle').text(yLabelText)

  // Helpers for quarterly expansion (for CPI)
  function expandCPIQuarterly(rows) {
    const out = []
    rows.forEach((d) => {
      const q = d.CPI0450
      if (!Array.isArray(q)) return
      for (let i = 0; i < q.length; i++) {
        out.push({ year: d.year + i / 4, qIndex: i + 1, value: Number(q[i]) })
      }
    })
    return out
  }

  // Base line generators (use provided xScale when redrawing)
  function lineForSeries(xScale) {
    if (props.activeSeries === 'electricity') {
      return d3.line()
        .defined(d => d.electricity != null)
        .x(d => xScale(d.year))
        .y(d => y(d.electricity))
        .curve(d3.curveMonotoneX)
    }
    return d3.line()
      .defined(d => mean(d.CPI0450) != null)
      .x(d => xScale(d.year))
      .y(d => y(mean(d.CPI0450)))
      .curve(d3.curveMonotoneX)
  }

  // Draw initial paths (will be updated by zoom handler)
  const mainLine = main.append('path').attr('class', 'line main-line').attr('fill', 'none')
  const annualLine = main.append('path').attr('class', 'line annual-line')
  const quarterlyLine = main.append('path').attr('class', 'line quarterly-line')
  const pointsG = main.append('g').attr('class', 'points')
  const cpiQuarterG = main.append('g').attr('class', 'cpi-quarter')
  // focused-year annual marker (for electricity) — ensures the selected year's annual point remains visible when zoomed to quarters
  const focusedAnnualG = main.append('g').attr('class', 'focused-annual')

  // render function used by draw and zoom handler
  function renderWithXScale(xScale, showQuarterly = false) {
    const line = lineForSeries(xScale)
    if (props.activeSeries === 'electricity') {
      mainLine.attr('stroke', '#2c7be5').attr('stroke-width', 2).attr('opacity', 1)
      annualLine
        .attr('stroke', '#ffb86b')
        .attr('stroke-width', 2)
        .attr('fill', 'none')
        .datum(data.value)
        .attr('d',
            d3.line()
            .defined(d => mean(d.CPI0450) != null)
            .x(d => xScale(d.year))
            .y(d => y(mean(d.CPI0450)))
            .curve(d3.curveMonotoneX)
        )

      mainLine.datum(data.value).attr('d', line)

      // If the rendered path is effectively empty (viewport contains ≤1 annual point), draw a visible fallback
      const node = mainLine.node()
      const pathLength = node && node.getTotalLength ? node.getTotalLength() : 0
      if (pathLength < 2) {
        const sorted = data.value.filter(d => d.electricity != null).slice().sort((a,b)=>a.year-b.year)
        // prefer focused year + neighbor, else nearest two
        let a = null, b = null
        if (props.focusYear != null) {
          const idx = sorted.findIndex(d => d.year === props.focusYear)
          if (idx >= 0) {
            a = sorted[idx]
            b = sorted[idx+1] || sorted[idx-1] || null
          }
        }
        if (!a) {
          const center = (xScale.domain ? (xScale.domain()[0] + xScale.domain()[1]) / 2 : null)
          const nearest = sorted.map(d=>({d,dist:Math.abs(d.year - (center||0))})).sort((p,q)=>p.dist-q.dist)
          a = nearest[0] ? nearest[0].d : null
          b = nearest[1] ? nearest[1].d : nearest[0] ? nearest[0].d : null
        }
        if (a && b) {
          const fallbackLine = d3.line().defined(d => d && d.electricity != null).x(d => xScale(d.year)).y(d => y(d.electricity))
          mainLine.datum([a,b]).attr('d', fallbackLine).attr('stroke-width', 3)
        }
      }

      const pts = pointsG.selectAll('circle').data(data.value.filter(d => d.electricity != null), d => d.year)
      pts.join(
        enter => enter.append('circle')
          .attr('cx', d => xScale(d.year))
          .attr('cy', d => y(d.electricity))
          .attr('r', d => (props.focusYear === d.year ? 6 : 3.5))
          .attr('fill', d => (props.focusYear === d.year ? '#ff7b54' : '#fff'))
          .attr('stroke', d => (props.focusYear === d.year ? '#ff7b54' : '#2c7be5'))
          .attr('stroke-width', 1.5)
          .style('cursor', 'pointer')
          .on('click', (event, d) => emits('update:focusYear', d.year))
          .on('mouseenter', (event, d) => showTooltip(event, d))
          .on('mouseleave', hideTooltip),
        update => update.call(u => u.attr('cx', d => xScale(d.year)).attr('cy', d => y(d.electricity)).attr('r', d => (props.focusYear === d.year ? 6 : 3.5))),
        exit => exit.remove()
      )
      cpiQuarterG.selectAll('*').remove()
    } else {
      mainLine.attr('stroke', '#ffb86b').attr('stroke-width', 2).attr('stroke-dasharray', '3 0')
      if (!showQuarterly) {
        mainLine.datum(data.value).attr('d', line)
        const pts = pointsG.selectAll('circle').data(data.value.filter(d => mean(d.CPI0450) != null), d => d.year)
        pts.join(
          enter => enter.append('circle')
            .attr('cx', d => xScale(d.year))
            .attr('cy', d => y(mean(d.CPI0450)))
            .attr('r', d => (props.focusYear === d.year ? 5 : 3))
            .attr('fill', '#fff')
            .attr('stroke', '#ffb86b')
            .attr('stroke-width', 1.25)
            .style('cursor', 'pointer')
            .on('click', (event, d) => emits('update:focusYear', d.year))
            .on('mouseenter', (event, d) => showTooltip(event, d))
            .on('mouseleave', hideTooltip),
          update => update.call(u => u.attr('cx', d => xScale(d.year)).attr('cy', d => y(mean(d.CPI0450))).attr('r', d => (props.focusYear === d.year ? 5 : 3))),
          exit => exit.remove()
        )
        cpiQuarterG.selectAll('*').remove()
      } else {
        // show quarterly values as small connected dots
        const quarterly = expandCPIQuarterly(data.value)
        quarterlyLine
          .attr('stroke', '#ffb86b')
          .attr('stroke-width', 1.5)
          .attr('fill', 'none')
          .datum(quarterly)
          .attr('d',
              d3.line()
              .defined(d => d.value != null)
              .x(d => xScale(d.year))
              .y(d => y(d.value))
              .curve(d3.curveMonotoneX)
        )
        const qLine = d3.line().defined(d => d.value != null).x(d => xScale(d.year)).y(d => y(d.value)).curve(d3.curveMonotoneX)
        mainLine.datum(quarterly).attr('d', qLine)
        pointsG.selectAll('*').remove()
        const qpts = cpiQuarterG.selectAll('circle').data(quarterly, d => `${d.year}-${d.qIndex}`)
        qpts.join(
          enter => enter.append('circle')
            .attr('cx', d => xScale(d.year))
            .attr('cy', d => y(d.value))
            .attr('r', 2.5)
            .attr('fill', '#ffb86b')
            .on('mouseenter', (event, d) => showQuarterTooltip(event, d))
            .on('mouseleave', hideTooltip),
          update => update.call(u => u.attr('cx', d => xScale(d.year)).attr('cy', d => y(d.value))),
          exit => exit.remove()
        )
      }
    }

    // update y axis (already set by caller when computing visible domain)
    main.select('.y.axis').call(yAxis)
    xAxisG.call(xAxis.scale(xScale))

    // Ensure focus visuals follow the rescaled x (keeps the orange line anchored to data coordinates)
    if (typeof updateFocusVisuals === 'function') updateFocusVisuals(xScale)
  }

  // helper: update focus-line and annotations so they follow data coordinates (works with rescaled x)
  updateFocusVisuals = function(xScale) {
    const year = props.focusYear != null ? props.focusYear : (latest.value && latest.value.year)
    if (year == null) {
      main.selectAll('.focus-line,.focus-annotation').remove()
      return
    }
    const fy = data.value.find(d => d.year === year) || null
    const xPos = xScale(year)

    // focus line (always draw even if no point exists) — tied to data-space X
    const fl = main.selectAll('.focus-line').data([year])
    fl.join('line')
      .attr('class', 'focus-line')
      .attr('x1', xPos)
      .attr('x2', xPos)
      .attr('y1', 0)
      .attr('y2', innerH)
      .attr('stroke', '#ff7b54')
      .attr('stroke-dasharray', '3 3')
      .attr('stroke-width', 1)

    // annotation (only when a value exists for the active series)
    main.selectAll('.focus-annotation').remove()
    if (fy) {
      if (props.activeSeries === 'electricity' && fy.electricity != null) {
        const annY = Math.max(12, y(fy.electricity) - 12)
        main.append('text')
          .attr('x', xPos + 8)
          .attr('y', annY)
          .attr('class', 'focus-annotation')
          .text(`${fy.electricity} US¢/kWh · ${fy.year}`)
      } else if (props.activeSeries === 'energy') {
        const cpiVal = mean(fy.CPI0450)
        if (cpiVal != null) {
          const annYC = Math.min(innerH - 6, y(cpiVal) + 14)
          main.append('text')
            .attr('x', xPos + 8)
            .attr('y', annYC)
            .attr('class', 'focus-annotation')
            .style('fill', '#8a5b00')
            .text(`${cpiVal.toFixed(1)} CPI · ${fy.year}`)
        }
      }
    }

    // update KPI/focusedPoint related visuals (maintain aria/live)
    if (liveRef.value && year) liveRef.value.textContent = `Chart centered on ${year}`

    // --- focused annual marker (draw last so it sits on top) ---
    focusedAnnualG.selectAll('*').remove()
    if (props.focusYear != null && props.activeSeries === 'electricity') {
      const fyA = data.value.find(d => d.year === props.focusYear)
      if (fyA && fyA.electricity != null) {
        const cx = xScale(fyA.year)
        const cy = y(fyA.electricity)

        // pixel-stable stub width
        const pixelPerYear = Math.abs(xScale(fyA.year + 1) - xScale(fyA.year))
        const r = Math.max(6, Math.min(14, pixelPerYear * 0.08))

        focusedAnnualG.append('circle')
          .attr('cx', cx)
          .attr('cy', cy)
          .attr('r', r)
          .attr('fill', '#fff')
          .attr('stroke', '#2c7be5')
          .attr('stroke-width', 1.75)
          .style('cursor', 'pointer')
          .on('mouseenter', (event, d) => showTooltip(event, fyA))
          .on('mouseleave', hideTooltip)

        // raise to top so it cannot be obscured by other layers
        try { focusedAnnualG.raise() } catch (e) { /* ignore for older d3 */ }
      }
    }

  }


  // ensure focus visuals are present for the initial focusYear
  if (updateFocusVisuals) updateFocusVisuals(x)
  // initial render
  renderWithXScale(x, false)

  // Focus visuals are handled by the zoom-aware renderer (renderWithXScale + updateFocusVisuals)
  // — this prevents focus elements from becoming detached during transforms.

  // TOOLTIP
  const tooltip = d3.select(containerRef.value).selectAll('.chart-tooltip').data([null])
    .join('div')
    .attr('class', 'chart-tooltip')
    .style('position', 'absolute')
    .style('pointer-events', 'none')
    .style('opacity', 0)

  function showTooltip(event, d) {
    const rect = containerRef.value.getBoundingClientRect()
    const cpiVal = mean(d.CPI0450)
    let html = `<div class="tt-year">${d.year}</div>`
    if (props.activeSeries === 'electricity') html += d.electricity != null ? `<div class="tt-val">${d.electricity} US¢/kWh</div>` : `<div class="tt-val">No electricity data</div>`
    else html += cpiVal != null ? `<div class="tt-val">Energy CPI (annual mean): ${cpiVal.toFixed(1)}</div>` : '<div class="tt-val">No CPI data</div>'
    html += `<div class="tt-hint">Use header toggle to switch series</div>`
    tooltip.style('opacity', 1).html(html).style('left', `${(event.clientX - rect.left) + 12}px`).style('top', `${(event.clientY - rect.top) - 12}px`)
  }

  // Quarterly tooltip (used when zoomed to quarterly CPI points)
  function showQuarterTooltip(event, d) {
    const rect = containerRef.value.getBoundingClientRect()
    const year = Math.floor(d.year)
    const q = d.qIndex || Math.round((d.year - year) * 4) + 1
    const val = Number(d.value)
    const html = `<div class="tt-year">${year} Q${q}</div><div class="tt-val">Energy CPI: ${Number.isFinite(val) ? val.toFixed(2) : '—'}</div><div class="tt-hint">Quarterly detail — use zoom out to return to annual view</div>`
    tooltip.style('opacity', 1).html(html).style('left', `${(event.clientX - rect.left) + 12}px`).style('top', `${(event.clientY - rect.top) - 12}px`)
  }

  function hideTooltip() { tooltip.style('opacity', 0) }

  // overview/brush removed — chart is now focus-first. Use zoom or `focusOnYear(year, { span })` to navigate.

  // ZOOM (main pane)
  zoomBehavior = d3.zoom()
    .scaleExtent([1, 16])
    .translateExtent([[-50, -100], [innerW + 50, innerH + 100]])
    .on('zoom', (event) => {
      // rescale X and update visuals without applying group transform
      const zx = event.transform.rescaleX(x)
      currentZoom = event.transform

      // visible domain in data coordinates
      const [from, to] = zx.domain()

      // determine whether to show quarterly CPI detail: narrow visible window (<= 2 years)
      const showQuarterly = props.activeSeries === 'energy' && (to - from <= 1.5 || event.transform.k >= 6)

      // gather visible values for the active series — use quarterly values when showing quarterly detail
      let visibleVals = []
      if (props.activeSeries === 'electricity') {
        visibleVals = data.value.filter(d => d.electricity != null && d.year >= from && d.year <= to).map(d => d.electricity)
      } else {
        if (showQuarterly) {
          const quarterly = expandCPIQuarterly(data.value)
          visibleVals = quarterly.filter(d => d.value != null && d.year >= from && d.year <= to).map(d => d.value)
        } else {
          // for CPI use annual means (keep previous behavior for wider views)
          visibleVals = data.value.filter(d => mean(d.CPI0450) != null && d.year >= Math.floor(from) && d.year <= Math.ceil(to)).map(d => mean(d.CPI0450))
        }
      }

      const [vmin, vmax] = numericExtent(visibleVals, y.domain()[0], y.domain()[1])
      // expand a bit for breathing room
      const pad = (vmax - vmin) * 0.08 || 1
      y.domain([Math.max(0, vmin - pad), vmax + pad]).nice()

      if (showQuarterly) {
        annualLine.style('display', 'none')
        quarterlyLine.style('display', null)
      } else {
        annualLine.style('display', null)
        quarterlyLine.style('display', 'none')
      }

      // render with the rescaled x
      renderWithXScale(zx, showQuarterly)
    })

  svg.call(zoomBehavior)

  // If we have an existing transform (user zoomed before) restore it
  if (currentZoom) {
    svg.call(zoomBehavior.transform, currentZoom)
  } else {
    currentZoom = d3.zoomIdentity
  }

  // Helper: center on year while preserving scale
  function computeCenterTransform(targetYear, preserveScale = true) {
    const k = (preserveScale && currentZoom && currentZoom.k) ? currentZoom.k : 1
    const xCoord = x(targetYear)
    const translateX = (containerWidth / 2) - xCoord * k
    return d3.zoomIdentity.translate(translateX, 0).scale(k)
  }

  focusOnYear = function(year, opts = { span: null }) {
    if (year == null) return

    // determine scale: if span requested, compute scale to fit that span; otherwise preserve current scale
    const k = (opts && Number.isFinite(opts.span) && opts.span > 0)
      ? (function() {
          const span = Number(opts.span)
          const left = Math.max(x.domain()[0], year - span)
          const right = Math.min(x.domain()[1], year + span)
          const pixelWidth = Math.max(1, x(right) - x(left))
          return Math.max(1, Math.min(16, innerW / pixelWidth))
        })()
      : ((currentZoom && currentZoom.k) ? currentZoom.k : 1)

    const xCoord = x(year)
    const translateX = (containerWidth / 2) - xCoord * k
    const t = d3.zoomIdentity.translate(translateX, 0).scale(k)
    svg.transition().duration(TRANSITION_MS).call(zoomBehavior.transform, t)
    currentZoom = t

    // recompute visible domain and y-domain (same rules as zoom handler)
    const zx = t.rescaleX(x)
    const [fromZ, toZ] = zx.domain()
    const showQuarterly = (opts && Number.isFinite(opts.span) && opts.span <= 2) || (toZ - fromZ <= 1.5) || (t.k >= 6)

    let visibleVals = []
    if (props.activeSeries === 'electricity') {
      visibleVals = data.value.filter(d => d.electricity != null && d.year >= fromZ && d.year <= toZ).map(d => d.electricity)
    } else {
      if (showQuarterly) {
        const quarterly = expandCPIQuarterly(data.value)
        visibleVals = quarterly.filter(d => d.value != null && d.year >= fromZ && d.year <= toZ).map(d => d.value)
      } else {
        visibleVals = data.value.filter(d => mean(d.CPI0450) != null && d.year >= Math.floor(fromZ) && d.year <= Math.ceil(toZ)).map(d => mean(d.CPI0450))
      }
    }

    const [vmin, vmax] = numericExtent(visibleVals, y.domain()[0], y.domain()[1])
    const pad = (vmax - vmin) * 0.08 || 1
    y.domain([Math.max(0, vmin - pad), vmax + pad]).nice()

    try { renderWithXScale(zx, showQuarterly) } catch (e) { renderWithXScale(x, false) }
    if (typeof updateFocusVisuals === 'function') updateFocusVisuals(zx)

    if (liveRef.value) liveRef.value.textContent = `Chart centered on ${year}`
  }
}

// REACTIVITY
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
        nextTick(() => draw())
      }
    })
    if (containerRef.value) ro.observe(containerRef.value)
    // keep ref for cleanup
    resizeObserverRef.value = ro

    draw()
  })

  window.addEventListener('resize', draw)
})

watch(() => props.data, () => {
  nextTick(draw)
}, { deep: true })

watch(() => props.focusYear, (ny) => {
  if (ny == null) return
  // center and zoom to ±2 years so the selected year is shown in context; show its quarterly detail when appropriate
  setTimeout(() => { if (typeof focusOnYear === 'function') focusOnYear(ny, { span: 2 }) }, 0)
}, { immediate: true })

// Keep a reference to the observer so we can disconnect it
const resizeObserverRef = ref(null)

onUnmounted(() => {
  if (resizeObserverRef.value) {
    try { resizeObserverRef.value.disconnect() } catch (e) {}
  }
  d3.selectAll('.tooltip-container').remove()
})
</script>

<style scoped>
.prices-focus-chart { width: 100%; }
.chart-header { display:flex; justify-content:space-between; align-items:center; gap:1rem }
.kpi { display:flex; flex-direction:column }
.kpi-value { font-size:1.6rem; font-weight:700 }
.kpi-sub { color: #666; font-size:0.9rem }
.chart-area { width:100%; min-height:220px; position:relative }
.chart-tooltip { background:rgba(0,0,0,0.8); color:white; padding:0.4rem 0.6rem; border-radius:6px; font-size:0.85rem }
.focus-annotation { font-size:0.8rem; font-weight:600; fill:#333 }
.line { stroke-linecap:round; stroke-linejoin:round }
.cpi-line { stroke-linecap:round; stroke-linejoin:round; opacity:0.95 }
.overview-line { stroke-opacity:0.9 }
.y-label { fill: #666; font-size: 11px }
.y-label.right { fill: #7a5600 }
.legend text { font-size: 11px; fill: #666 }
.sr-only { position: absolute !important; width:1px; height:1px; padding:0; margin:-1px; overflow:hidden; clip:rect(0,0,0,0); white-space:nowrap; border:0 }
.series-toggle {
    display: flex;
    gap: 0.5rem;
}
</style>
