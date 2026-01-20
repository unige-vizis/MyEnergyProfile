<template>
  <div class="trading-partners-map">
    <div class="chart-header">
      <h4>The Trading Partners</h4>
      <p class="chart-subtitle">Import and export partners by energy type</p>
    </div>

    <div v-if="!hasData" class="no-data">
      <span class="no-data-icon">?</span>
      <span>No trade data available for this year</span>
    </div>

    <div v-else class="map-wrapper">
      <div class="map-container">
        <!-- Trade Volume Summary with Toggle Buttons -->
        <div class="volume-summary">
          <div class="volume-grid">
            <div class="volume-row-label"></div>
            <button
              v-for="type in energyTypes"
              :key="type.code"
              :class="['volume-header-btn', { active: activeTypes.has(type.code) }]"
              :style="{
                '--type-color': type.color,
                backgroundColor: activeTypes.has(type.code) ? type.color : 'transparent',
                color: activeTypes.has(type.code) ? '#fff' : type.color
              }"
              @click="toggleType(type.code)"
            >
              {{ type.label }}
            </button>

            <button
              :class="['volume-row-label', 'imports-label', 'direction-toggle', { active: activeDirections.has('imports') }]"
              @click="toggleDirection('imports')"
            >
              <span class="checkbox-icon">{{ activeDirections.has('imports') ? '☑' : '☐' }}</span>
              Imports
            </button>
            <div
              v-for="type in energyTypes"
              :key="'imp-' + type.code"
              :class="['volume-cell', 'imports', { inactive: !activeTypes.has(type.code) }]"
            >
              <span class="volume-value">{{ formatVolume(getVolumeByType('imports', type.code)) }}</span>
              <span class="volume-unit">{{ type.unit }}</span>
            </div>

            <button
              :class="['volume-row-label', 'exports-label', 'direction-toggle', { active: activeDirections.has('exports') }]"
              @click="toggleDirection('exports')"
            >
              <span class="checkbox-icon">{{ activeDirections.has('exports') ? '☑' : '☐' }}</span>
              Exports
            </button>
            <div
              v-for="type in energyTypes"
              :key="'exp-' + type.code"
              :class="['volume-cell', 'exports', { inactive: !activeTypes.has(type.code) }]"
            >
              <span class="volume-value">{{ formatVolume(getVolumeByType('exports', type.code)) }}</span>
              <span class="volume-unit">{{ type.unit }}</span>
            </div>
          </div>
        </div>

        <!-- Map SVG Container -->
        <div ref="mapContainerRef" class="map-svg-container"></div>

        <!-- Map controls -->
        <div class="map-controls">
          <div class="controls-left">
            <button class="reset-zoom-btn" @click="resetZoom" title="Reset zoom">
              <span class="material-symbols-outlined">zoom_out_map</span>
            </button>
            <span class="map-hint">Scroll to zoom, drag to pan, double-click to reset</span>
          </div>
          <div class="cutoff-slider">
            <label class="cutoff-label">Min trade %</label>
            <input
              type="range"
              v-model.number="arrowCutoff"
              min="0"
              max="10"
              step="1"
              class="cutoff-range"
            />
            <span class="cutoff-value">{{ arrowCutoff }}%</span>
          </div>
        </div>

        <div class="chart-meta">
          <div class="meta-section">
            <span class="meta-label">Source:</span>
            <ul class="meta-list">
              <li>Eurostat <a href="https://ec.europa.eu/eurostat/web/energy/database" target="_blank" rel="noopener">Energy Database</a> (European Commission)</li>
              <li>Tables <code>nrg_ti_*</code> (imports) and <code>nrg_te_*</code> (exports) for sff, oil, gas, bio, eh</li>
              <li>Derived: <code>share_pct</code> = partner value ÷ total × 100</li>
            </ul>
          </div>
          <div class="meta-section">
            <span class="meta-label">Data Hints:</span>
            <div class="chart-notes">
              <p class="chart-note">
                <span class="note-icon">*</span>
                <span>EU-reported data only; non-EU partner volumes may be incomplete.</span>
              </p>
              <p class="chart-note">
                <span class="note-icon">*</span>
                <span>Regional aggregates (e.g., "Other Asian countries") excluded from map arrows but included in totals.</span>
              </p>
            </div>
          </div>
        </div>

      </div>

      <div class="map-info">
        <div class="info-section data-hint-note">
          <div class="info-title">Data Hint</div>
          <p class="info-text">
            Trade data is based on reports submitted by Eurostat member countries. As a result, data for non-EU trading partners may be incomplete or reflect only the EU perspective of the trade relationship.
          </p>
        </div>

        <div class="info-section placeholder-content">
          <div class="info-title placeholder-title">[Example] European Import Profile</div>
          <p class="info-text placeholder-text">
            Placeholder for general overview of European energy import patterns. Most EU nations are net importers of fossil fuels, relying on external suppliers for oil, gas, and coal.
          </p>
        </div>

        <div class="info-section placeholder-content">
          <div class="info-title placeholder-title">[Example] Notable Exceptions</div>
          <p class="info-text placeholder-text">
            Placeholder for countries that break the typical pattern. Norway as a major exporter, the Netherlands with its gas production, France with nuclear electricity exports.
          </p>
        </div>

        <div class="info-section placeholder-content">
          <div class="info-title placeholder-title">[Example] Global Players</div>
          <p class="info-text placeholder-text">
            Placeholder for dominant energy exporters by fuel type. Russia and Norway as Europe's main gas suppliers, Saudi Arabia and Iraq for crude oil, Australia and Indonesia for coal, Canada for uranium. Their market share and geopolitical influence.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch, onMounted, onUnmounted, nextTick } from 'vue'
import * as d3 from 'd3'
import {
  normalizeGeo,
  isRegionalAggregate as checkRegionalAggregate,
  getNumericCode,
  getAlpha2Code,
  countryNames
} from '@/utils/countryCodeMapping'

// Inline topojson.feature() to avoid external dependency
// Converts TopoJSON to GeoJSON FeatureCollection
function topojsonFeature(topology, o) {
  if (typeof o === 'string') o = topology.objects[o]
  return o.type === 'GeometryCollection'
    ? { type: 'FeatureCollection', features: o.geometries.map(g => toFeature(topology, g)) }
    : toFeature(topology, o)
}

function toFeature(topology, o) {
  const id = o.id
  const bbox = o.bbox
  const properties = o.properties || {}
  const geometry = toGeometry(topology, o)
  const feature = id == null && bbox == null
    ? { type: 'Feature', properties, geometry }
    : bbox == null
      ? { type: 'Feature', id, properties, geometry }
      : { type: 'Feature', id, bbox, properties, geometry }
  return feature
}

function toGeometry(topology, o) {
  const type = o.type
  if (type === 'GeometryCollection') {
    return { type, geometries: o.geometries.map(g => toGeometry(topology, g)) }
  }
  if (type === 'Point') {
    return { type, coordinates: transformPoint(topology, o.coordinates) }
  }
  if (type === 'MultiPoint') {
    return { type, coordinates: o.coordinates.map(c => transformPoint(topology, c)) }
  }
  // For arcs-based geometries
  const arcs = o.arcs
  if (type === 'LineString') {
    return { type, coordinates: decodeArc(topology, arcs) }
  }
  if (type === 'MultiLineString' || type === 'Polygon') {
    return { type, coordinates: arcs.map(a => decodeArc(topology, a)) }
  }
  if (type === 'MultiPolygon') {
    return { type, coordinates: arcs.map(polygon => polygon.map(ring => decodeArc(topology, ring))) }
  }
  return null
}

function transformPoint(topology, coordinates) {
  const transform = topology.transform
  if (!transform) return coordinates.slice()
  const scale = transform.scale
  const translate = transform.translate
  return [coordinates[0] * scale[0] + translate[0], coordinates[1] * scale[1] + translate[1]]
}

function decodeArc(topology, arcIndexes) {
  const coordinates = []
  const arcs = topology.arcs
  const transform = topology.transform

  for (let i = 0; i < arcIndexes.length; i++) {
    let arcIndex = arcIndexes[i]
    const reverse = arcIndex < 0
    if (reverse) arcIndex = ~arcIndex

    const arc = arcs[arcIndex]
    const arcCoords = []
    let x = 0, y = 0

    // Decode the entire arc to absolute coordinates first
    for (let j = 0; j < arc.length; j++) {
      x += arc[j][0]
      y += arc[j][1]

      const coord = transform
        ? [x * transform.scale[0] + transform.translate[0], y * transform.scale[1] + transform.translate[1]]
        : [x, y]
      arcCoords.push(coord)
    }

    // If reversed, reverse the decoded coordinates
    if (reverse) arcCoords.reverse()

    // Add to result, skipping first point if not the first arc (avoids duplicate at joins)
    const startIndex = (i === 0) ? 0 : 1
    for (let j = startIndex; j < arcCoords.length; j++) {
      coordinates.push(arcCoords[j])
    }
  }
  return coordinates
}

const props = defineProps({
  tradeData: {
    type: Object,
    default: null
  },
  country: {
    type: Object,
    default: null
  },
  year: {
    type: Number,
    default: null
  }
})

// Energy type definitions with colors
const energyTypes = [
  { code: 'SFF', label: 'Coal', unit: 'thousand tonnes', color: '#8b4513' },
  { code: 'OIL', label: 'Oil', unit: 'thousand tonnes', color: '#1a1a1a' },
  { code: 'GAS', label: 'Gas', unit: 'TJ', color: '#2980b9' },
  { code: 'BIO', label: 'Biofuels', unit: 'thousand tonnes', color: '#27ae60' },
  { code: 'EH', label: 'Electricity', unit: 'GWh', color: '#f1c40f' }
]

// Active types (toggle state) - start with electricity, oil, and gas active
const activeTypes = ref(new Set(['OIL', 'GAS', 'EH']))

// Active directions (toggle state) - start with only imports selected
const activeDirections = ref(new Set(['imports']))

// Arrow visibility cutoff percentage (0-10%, default 3%)
const arrowCutoff = ref(3)

const mapContainerRef = ref(null)
let resizeObserver = null
let worldData = null // Cache for TopoJSON data
let currentZoom = null // Store current zoom transform
let zoomBehavior = null // Store zoom behavior for reset

function resetZoom() {
  if (!mapContainerRef.value || !zoomBehavior) return
  // Re-render to recalculate zoom based on current selected country
  currentZoom = null
  renderMap()
}

function toggleType(code) {
  if (activeTypes.value.has(code)) {
    activeTypes.value.delete(code)
    activeTypes.value = new Set(activeTypes.value) // Trigger reactivity
  } else {
    activeTypes.value.add(code)
    activeTypes.value = new Set(activeTypes.value) // Trigger reactivity
  }
}

function toggleDirection(direction) {
  if (activeDirections.value.has(direction)) {
    activeDirections.value.delete(direction)
    activeDirections.value = new Set(activeDirections.value) // Trigger reactivity
  } else {
    activeDirections.value.add(direction)
    activeDirections.value = new Set(activeDirections.value) // Trigger reactivity
  }
}

const activeTypesCount = computed(() => activeTypes.value.size)

const selectedUnit = computed(() => {
  if (activeTypes.value.size === 1) {
    const activeCode = Array.from(activeTypes.value)[0]
    const type = energyTypes.find(t => t.code === activeCode)
    return type?.unit || ''
  }
  return ''
})

// Get the active energy types as an array (for grid display)
const activeEnergyTypes = computed(() => {
  return energyTypes.filter(t => activeTypes.value.has(t.code))
})

// Get volume for a specific type and direction
function getVolumeByType(direction, typeCode) {
  const data = direction === 'imports'
    ? props.tradeData?.imports?.total_by_type
    : props.tradeData?.exports?.total_by_type
  return data?.[typeCode]?.value ?? null
}

const hasData = computed(() => {
  return props.tradeData?.imports || props.tradeData?.exports
})

// Calculate total volumes for active types
const totalImportVolume = computed(() => {
  if (!props.tradeData?.imports?.total_by_type) return null
  let total = 0
  for (const code of activeTypes.value) {
    const val = props.tradeData.imports.total_by_type[code]?.value
    if (val != null) total += val
  }
  return total || null
})

const totalExportVolume = computed(() => {
  if (!props.tradeData?.exports?.total_by_type) return null
  let total = 0
  for (const code of activeTypes.value) {
    const val = props.tradeData.exports.total_by_type[code]?.value
    if (val != null) total += val
  }
  return total || null
})

function formatVolume(value) {
  if (value === null || value === undefined) return 'N/A'
  return String(Math.round(value)).replace(/\B(?=(\d{3})+(?!\d))/g, ' ')
}

// Helper to check regional aggregate
function isRegionalAggregate(code) {
  return checkRegionalAggregate(code)
}


// Get trade flows for map visualization (per energy type, excludes regional aggregates)
function getTradeFlows(direction) {
  const data = direction === 'imports'
    ? props.tradeData?.imports
    : props.tradeData?.exports

  if (!data?.partners_by_type) return []

  const flows = []

  // Iterate through each active energy type
  for (const typeCode of activeTypes.value) {
    const typePartners = data.partners_by_type[typeCode]
    if (!typePartners) continue

    // Get the color for this energy type
    const typeInfo = energyTypes.find(t => t.code === typeCode)
    const color = typeInfo?.color || '#666'

    for (const partner of typePartners) {
      // Skip if share is below cutoff threshold
      if (!partner.share_pct || partner.share_pct < arrowCutoff.value) continue

      // Skip regional aggregates - they can't be mapped
      if (isRegionalAggregate(partner.geo)) continue

      // Normalize the geo code
      const normalizedGeo = normalizeGeo(partner.geo)

      flows.push({
        partnerGeo: normalizedGeo,
        partnerName: countryNames[normalizedGeo] || partner.name || normalizedGeo,
        value: partner.value,
        sharePercent: partner.share_pct,
        color: color,
        typeCode: typeCode,
        typeName: typeInfo?.label || typeCode,
        direction
      })
    }
  }

  return flows
}

async function loadWorldData() {
  if (worldData) return worldData

  try {
    const response = await fetch(`${import.meta.env.BASE_URL}data/countries-110m.json`)
    worldData = await response.json()
    return worldData
  } catch (e) {
    console.error('Failed to load world map data:', e)
    return null
  }
}

async function renderMap() {
  if (!mapContainerRef.value || !hasData.value) return

  // Clear previous content
  d3.select(mapContainerRef.value).selectAll('*').remove()

  // Load world data
  const world = await loadWorldData()
  if (!world) {
    // Show error message
    d3.select(mapContainerRef.value)
      .append('div')
      .attr('class', 'map-error')
      .text('Failed to load map data')
    return
  }

  const container = mapContainerRef.value
  const containerWidth = container.clientWidth || 600
  const containerHeight = Math.min(containerWidth * 0.5, 400)

  // Create SVG
  const svg = d3.select(container)
    .append('svg')
    .attr('width', containerWidth)
    .attr('height', containerHeight)
    .attr('viewBox', `0 0 ${containerWidth} ${containerHeight}`)
    .style('cursor', 'grab')

  // Add defs for arrow markers
  const defs = svg.append('defs')

  // Create a main group for all zoomable content
  const mapGroup = svg.append('g').attr('class', 'map-group')

  // Setup zoom behavior with extended pan margins
  const panMargin = Math.max(containerWidth, containerHeight) * 0.5
  zoomBehavior = d3.zoom()
    .scaleExtent([1, 8]) // Min and max zoom levels
    .translateExtent([
      [-panMargin, -panMargin],
      [containerWidth + panMargin, containerHeight + panMargin]
    ]) // Extended pan boundaries for easier edge navigation
    .on('zoom', (event) => {
      mapGroup.attr('transform', event.transform)
      currentZoom = event.transform
    })
    .on('start', () => {
      svg.style('cursor', 'grabbing')
    })
    .on('end', () => {
      svg.style('cursor', 'grab')
    })

  // Apply zoom behavior to SVG
  svg.call(zoomBehavior)

  // Create arrow markers for each energy type and direction combination
  const directionColors = {
    imports: '#e53935',
    exports: '#43a047'
  }
  for (const type of energyTypes) {
    for (const direction of Object.keys(directionColors)) {
      // Main marker (energy type color) - arrowhead
      defs.append('marker')
        .attr('id', `arrow-${type.code}-${direction}`)
        .attr('viewBox', '0 0 10 10')
        .attr('refX', 0)
        .attr('refY', 5)
        .attr('markerWidth', 3)
        .attr('markerHeight', 3)
        .attr('markerUnits', 'strokeWidth')
        .attr('orient', 'auto')
        .append('path')
        .attr('d', 'M 0 2 L 6 5 L 0 8 z')
        .attr('fill', type.color)
    }
  }

  // Get country features from TopoJSON
  const countries = topojsonFeature(world, world.objects.countries)

  // Setup projection - Natural Earth for a nice world view
  const projection = d3.geoNaturalEarth1()
    .fitSize([containerWidth, containerHeight], countries)

  const pathGenerator = d3.geoPath().projection(projection)

  // Get selected country's numeric ID (needed early for zoom calculation)
  const selectedGeo = normalizeGeo(props.country?.code)
  const selectedNumericId = selectedGeo ? getNumericCode(selectedGeo) : null

  // Get all partner geo codes for highlighting (only for active directions)
  const importFlows = activeDirections.value.has('imports') ? getTradeFlows('imports') : []
  const exportFlows = activeDirections.value.has('exports') ? getTradeFlows('exports') : []
  const allFlows = [...importFlows, ...exportFlows]
  const allPartnerGeos = new Set(allFlows.map(f => f.partnerGeo))

  // Helper to create a light tint of a hex color
  function lightenColor(hex, lightness = 0.82) {
    const color = d3.color(hex)
    if (!color) return '#e0e8f0'
    const hsl = d3.hsl(color)
    hsl.l = lightness
    hsl.s = Math.min(hsl.s, 0.5) // Keep some saturation for visibility
    return hsl.formatHex()
  }

  // Build a map of partner geo -> proportional color stops for gradient
  const partnerColorStops = new Map()
  for (const geo of allPartnerGeos) {
    const partnerFlows = allFlows.filter(f => f.partnerGeo === geo)
    if (partnerFlows.length > 0) {
      // Aggregate by energy type (sum shares if same type appears in imports and exports)
      const typeShares = new Map()
      for (const flow of partnerFlows) {
        const current = typeShares.get(flow.typeCode) || { color: flow.color, share: 0 }
        current.share += flow.sharePercent || 0
        typeShares.set(flow.typeCode, current)
      }

      // Convert to array and sort by share descending
      const sorted = Array.from(typeShares.values())
        .sort((a, b) => b.share - a.share)
        .slice(0, 5) // Max 5 colors

      // Calculate proportional stops (normalize to 100%)
      const totalShare = sorted.reduce((sum, t) => sum + t.share, 0)
      let cumulative = 0
      const stops = []
      for (const type of sorted) {
        const proportion = (type.share / totalShare) * 100
        stops.push({
          color: lightenColor(type.color),
          start: cumulative,
          end: cumulative + proportion
        })
        cumulative += proportion
      }
      partnerColorStops.set(geo, stops)
    }
  }

  // Create gradient definitions for each partner country
  for (const [geo, stops] of partnerColorStops) {
    const gradient = defs.append('linearGradient')
      .attr('id', `partner-fill-${geo}`)
      .attr('x1', '0%')
      .attr('y1', '0%')
      .attr('x2', '100%')
      .attr('y2', '100%') // Diagonal gradient

    for (const stop of stops) {
      // Hard stops: add color at both start and end of its segment
      gradient.append('stop')
        .attr('offset', `${stop.start}%`)
        .attr('stop-color', stop.color)
      gradient.append('stop')
        .attr('offset', `${stop.end}%`)
        .attr('stop-color', stop.color)
    }
  }

  // Draw countries
  const countryPaths = mapGroup.append('g')
    .attr('class', 'countries')
    .selectAll('path')
    .data(countries.features)
    .join('path')
    .attr('d', pathGenerator)
    .attr('fill', d => {
      const numericId = String(d.id).padStart(3, '0')
      const alpha2 = getAlpha2Code(numericId)

      if (selectedNumericId && numericId === selectedNumericId) {
        return '#2c3e50' // Selected country - dark
      }
      if (alpha2 && allPartnerGeos.has(alpha2)) {
        // Use gradient if partner has color stops defined
        if (partnerColorStops.has(alpha2)) {
          return `url(#partner-fill-${alpha2})`
        }
        return '#e0e8f0'
      }
      return '#f0f0f0' // Default - light gray
    })
    .attr('stroke', '#999')
    .attr('stroke-width', 0.5)

  // Add tooltips to countries
  countryPaths
    .on('mouseenter', function(event, d) {
      const numericId = String(d.id).padStart(3, '0')
      const alpha2 = getAlpha2Code(numericId)
      const name = d.properties?.name || countryNames[alpha2] || alpha2

      // Check if this is a partner
      const isPartner = alpha2 && allPartnerGeos.has(alpha2)
      const isSelected = selectedNumericId && numericId === selectedNumericId

      if (isSelected || isPartner) {
        d3.select(this)
          .attr('stroke', '#333')
          .attr('stroke-width', 1.5)
      }

      // Show tooltip
      showTooltip(event, name, alpha2, isSelected, isPartner, importFlows, exportFlows)
    })
    .on('mouseleave', function() {
      d3.select(this)
        .attr('stroke', '#999')
        .attr('stroke-width', 0.5)
      hideTooltip()
    })

  // Calculate centroids for countries
  const centroids = {}
  countries.features.forEach(feature => {
    const numericId = String(feature.id).padStart(3, '0')
    const alpha2 = getAlpha2Code(numericId)
    if (alpha2) {
      const centroid = d3.geoCentroid(feature)
      if (centroid && !isNaN(centroid[0]) && !isNaN(centroid[1])) {
        centroids[alpha2] = projection(centroid)
      }
    }
  })

  // Mainland centroid overrides for countries with overseas territories
  // These REPLACE calculated centroids to point arrows at the mainland
  const mainlandOverrides = {
    'FR': [2.5, 46.5],      // France - mainland, not pulled toward French Guiana
    'NL': [5.3, 52.2],      // Netherlands - mainland, not Caribbean
    'DK': [9.5, 56.0],      // Denmark - mainland, not pulled toward Greenland
    'PT': [-8.0, 39.5],     // Portugal - mainland, not Azores/Madeira
    'ES': [-3.5, 40.0],     // Spain - mainland, not Canary Islands
    'US': [-98.0, 39.5],    // USA - continental, not pulled by Alaska
    'RU': [40.0, 56.0],     // Russia - European part for EU trade context
    'NO': [9.0, 62.0],      // Norway - mainland, not Svalbard
  }
  for (const [code, coords] of Object.entries(mainlandOverrides)) {
    const projected = projection(coords)
    if (projected) centroids[code] = projected
  }

  // Manual centroids for small territories not in 110m resolution map
  const smallTerritories = {
    'SG': [103.8, 1.35],    // Singapore
    'HK': [114.17, 22.32],  // Hong Kong
    'MO': [113.55, 22.2],   // Macao
    'GI': [-5.35, 36.14],   // Gibraltar
    'MT': [14.5, 35.9],     // Malta
    'LU': [6.13, 49.61],    // Luxembourg
    'AD': [1.52, 42.51],    // Andorra
    'MC': [7.42, 43.73],    // Monaco
    'SM': [12.46, 43.94],   // San Marino
    'VA': [12.45, 41.9],    // Vatican
    'LI': [9.55, 47.16],    // Liechtenstein
    'BH': [50.55, 26.07],   // Bahrain
  }
  for (const [code, coords] of Object.entries(smallTerritories)) {
    if (!centroids[code]) {
      const projected = projection(coords)
      if (projected) centroids[code] = projected
    }
  }

  // Get selected country centroid
  const selectedCentroid = selectedGeo ? centroids[selectedGeo] : null

  // Calculate initial zoom centered on selected country (or Europe as fallback)
  const initialScale = 2.5
  let zoomCenterX, zoomCenterY
  if (selectedCentroid) {
    // Center on selected country
    zoomCenterX = selectedCentroid[0]
    zoomCenterY = selectedCentroid[1]
  } else {
    // Fallback to Europe (lon 10, lat 50)
    const europeCoords = projection([10, 50])
    zoomCenterX = europeCoords[0]
    zoomCenterY = europeCoords[1]
  }
  const initialX = containerWidth / 2 - zoomCenterX * initialScale
  const initialY = containerHeight / 2 - zoomCenterY * initialScale
  const initialZoom = d3.zoomIdentity.translate(initialX, initialY).scale(initialScale)

  // Double-click to reset zoom (back to selected country view)
  svg.on('dblclick.zoom', null) // Disable default double-click zoom
  svg.on('dblclick', () => {
    svg.transition().duration(300).call(zoomBehavior.transform, initialZoom)
    currentZoom = initialZoom
  })

  // Apply initial or restored zoom
  if (currentZoom) {
    svg.call(zoomBehavior.transform, currentZoom)
  } else {
    svg.call(zoomBehavior.transform, initialZoom)
    currentZoom = initialZoom
  }

  // Draw trade flow arrows only if we have a selected country
  if (selectedCentroid && (importFlows.length > 0 || exportFlows.length > 0)) {
    const flowsGroup = mapGroup.append('g').attr('class', 'trade-flows')

    // Width scale: truly proportional (0-100% -> 0-6px)
    const widthScale = d3.scaleLinear()
      .domain([0, 100])
      .range([0, 6])
      .clamp(true)

    // Track offset per partner country to spread multiple arrows to the same destination
    const partnerOffsets = new Map()
    function getPartnerOffset(partnerGeo) {
      const current = partnerOffsets.get(partnerGeo) || 0
      partnerOffsets.set(partnerGeo, current + 1)
      return current
    }

    // Draw import flows (partner -> selected) - only if imports direction is active
    if (activeDirections.value.has('imports')) {
      importFlows.forEach((flow) => {
        const partnerCentroid = centroids[flow.partnerGeo]
        if (!partnerCentroid) return

        const offset = getPartnerOffset(flow.partnerGeo)
        drawFlowArrow(
          flowsGroup,
          partnerCentroid,
          selectedCentroid,
          flow,
          widthScale,
          offset,
          flow.typeCode,
          flow.color
        )
      })
    }

    // Draw export flows (selected -> partner) - only if exports direction is active
    if (activeDirections.value.has('exports')) {
      exportFlows.forEach((flow) => {
        const partnerCentroid = centroids[flow.partnerGeo]
        if (!partnerCentroid) return

        const offset = getPartnerOffset(flow.partnerGeo)
        drawFlowArrow(
          flowsGroup,
          selectedCentroid,
          partnerCentroid,
          flow,
          widthScale,
          offset,
          flow.typeCode,
          flow.color
        )
      })
    }
  }

  // Create tooltip element
  let tooltip = d3.select(container).select('.map-tooltip')
  if (tooltip.empty()) {
    tooltip = d3.select(container)
      .append('div')
      .attr('class', 'map-tooltip')
      .style('opacity', 0)
      .style('position', 'absolute')
      .style('pointer-events', 'none')
  }
}

function drawFlowArrow(group, from, to, flow, widthScale, offset, typeCode, color) {
  // Calculate control point for curved path
  const midX = (from[0] + to[0]) / 2
  const midY = (from[1] + to[1]) / 2

  // Perpendicular offset for curve
  const dx = to[0] - from[0]
  const dy = to[1] - from[1]
  const dist = Math.sqrt(dx * dx + dy * dy)

  if (dist < 10) return // Skip very short arrows

  // Normalize and perpendicular
  const perpX = -dy / dist
  const perpY = dx / dist

  // Curve amount: gentle curve, capped for visual cleanliness
  const curveAmount = Math.min(dist * 0.08, 15)

  // Spread multiple arrows to same partner: each arrow gets more curve
  // Spacing scales with distance for consistent visual separation
  const arrowSpacing = Math.max(3, dist * 0.04)
  const totalOffset = curveAmount + (offset * arrowSpacing)

  // Apply offset perpendicular to the line
  const controlX = midX + perpX * totalOffset
  const controlY = midY + perpY * totalOffset

  // Proportional width with minimum for visibility
  const strokeWidth = Math.max(0.2, widthScale(flow.sharePercent || 0))
  const outlineWidth = strokeWidth + 0.25
  const markerId = `arrow-${typeCode}-${flow.direction}`

  // Arrowhead length: markerWidth(3) * (6/10) * strokeWidth (arrow is 6 units in 10-unit viewBox)
  const arrowLength = 1.8 * strokeWidth

  // Shorten the endpoint so arrowhead tip lands at target
  // Direction from control point to target (tangent at endpoint)
  const tangentDx = to[0] - controlX
  const tangentDy = to[1] - controlY
  const tangentDist = Math.sqrt(tangentDx * tangentDx + tangentDy * tangentDy)
  const shortenedToX = to[0] - (tangentDx / tangentDist) * arrowLength
  const shortenedToY = to[1] - (tangentDy / tangentDist) * arrowLength

  // Create quadratic bezier path with shortened endpoint
  const pathD = `M ${from[0]} ${from[1]} Q ${controlX} ${controlY} ${shortenedToX} ${shortenedToY}`

  // Outline color based on direction (red for imports, green for exports)
  const outlineColor = flow.direction === 'imports' ? '#e53935' : '#43a047'

  // Draw outline path first (underneath) - no arrowhead, just the stroke
  group.append('path')
    .attr('d', pathD)
    .attr('fill', 'none')
    .attr('stroke', outlineColor)
    .attr('stroke-width', outlineWidth)
    .attr('stroke-opacity', 0.85)
    .attr('class', `flow-arrow-outline flow-${typeCode} flow-${flow.direction}`)
    .style('pointer-events', 'none')

  // Draw main path on top
  const mainPath = group.append('path')
    .attr('d', pathD)
    .attr('fill', 'none')
    .attr('stroke', color)
    .attr('stroke-width', strokeWidth)
    .attr('stroke-opacity', 0.9)
    .attr('marker-end', `url(#${markerId})`)
    .attr('class', `flow-arrow flow-${typeCode} flow-${flow.direction}`)

  mainPath
    .on('mouseenter', function(event) {
      d3.select(this)
        .attr('stroke-opacity', 1)

      const directionLabel = flow.direction === 'imports' ? 'imports' : 'exports'
      const tooltipContent = `
        <strong>${flow.partnerName}</strong><br/>
        <span style="color: ${color}">${flow.typeName}</span><br/>
        ${formatVolume(flow.value)}<br/>
        ${flow.sharePercent?.toFixed(1)}% of ${flow.typeName} ${directionLabel}
      `
      showFlowTooltip(event, tooltipContent)
    })
    .on('mouseleave', function() {
      d3.select(this)
        .attr('stroke-opacity', 0.9)
      hideTooltip()
    })
}

function showTooltip(event, name, alpha2, isSelected, isPartner, importFlows, exportFlows) {
  const container = mapContainerRef.value
  if (!container) return

  let content = `<strong>${name}</strong>`

  if (isSelected) {
    content += '<br/><em>Selected country</em>'
  } else if (isPartner) {
    // Find flows for this partner
    const imports = importFlows.filter(f => f.partnerGeo === alpha2)
    const exports = exportFlows.filter(f => f.partnerGeo === alpha2)

    if (imports.length > 0) {
      content += '<br/><span class="tooltip-section">Imports from:</span>'
      imports.forEach(f => {
        const typeInfo = energyTypes.find(t => t.code === f.typeCode)
        content += `<br/>  <span style="color: ${f.color}">${typeInfo?.label || f.typeCode}</span>: ${formatVolume(f.value)} (${f.sharePercent?.toFixed(1)}%)`
      })
    }

    if (exports.length > 0) {
      content += '<br/><span class="tooltip-section">Exports to:</span>'
      exports.forEach(f => {
        const typeInfo = energyTypes.find(t => t.code === f.typeCode)
        content += `<br/>  <span style="color: ${f.color}">${typeInfo?.label || f.typeCode}</span>: ${formatVolume(f.value)} (${f.sharePercent?.toFixed(1)}%)`
      })
    }
  }

  const tooltip = d3.select(container).select('.map-tooltip')
  if (!tooltip.empty()) {
    const containerRect = container.getBoundingClientRect()
    tooltip
      .html(content)
      .style('left', `${event.clientX - containerRect.left + 10}px`)
      .style('top', `${event.clientY - containerRect.top - 10}px`)
      .style('opacity', 1)
  }
}

function showFlowTooltip(event, content) {
  const container = mapContainerRef.value
  if (!container) return

  const tooltip = d3.select(container).select('.map-tooltip')
  if (!tooltip.empty()) {
    const containerRect = container.getBoundingClientRect()
    tooltip
      .html(content)
      .style('left', `${event.clientX - containerRect.left + 10}px`)
      .style('top', `${event.clientY - containerRect.top - 10}px`)
      .style('opacity', 1)
  }
}

function hideTooltip() {
  const container = mapContainerRef.value
  if (!container) return

  const tooltip = d3.select(container).select('.map-tooltip')
  if (!tooltip.empty()) {
    tooltip.style('opacity', 0)
  }
}

// Watch for changes and re-render
// Reset zoom when country changes so map re-centers
watch(
  () => props.country,
  () => {
    currentZoom = null
  }
)

watch(
  () => [props.tradeData, props.country, props.year, activeTypes.value, activeDirections.value, arrowCutoff.value],
  () => {
    nextTick(() => renderMap())
  },
  { deep: true }
)

onMounted(() => {
  renderMap()

  resizeObserver = new ResizeObserver(() => {
    renderMap()
  })

  if (mapContainerRef.value) {
    resizeObserver.observe(mapContainerRef.value)
  }
})

onUnmounted(() => {
  if (resizeObserver) {
    resizeObserver.disconnect()
  }
})
</script>

<style scoped>
.trading-partners-map {
  padding: 1.5rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background: #fafafa;
}

.chart-header {
  margin-bottom: 1rem;
}

.chart-header h4 {
  margin: 0 0 0.25rem 0;
  font-size: 1.1rem;
  color: #2c3e50;
}

.chart-subtitle {
  margin: 0;
  font-size: 0.85rem;
  color: #666;
}

.volume-summary {
  margin-bottom: 1rem;
}

.volume-grid {
  display: grid;
  grid-template-columns: auto repeat(5, 1fr);
  gap: 0.25rem 0.5rem;
  align-items: center;
}

.volume-row-label {
  font-size: 0.8rem;
  font-weight: 600;
  color: #666;
  text-align: right;
  padding-right: 0.75rem;
}

.imports-label {
  color: #e53935;
}

.exports-label {
  color: #43a047;
}

.direction-toggle {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0.25rem 0.5rem 0.25rem 0;
  border-radius: 4px;
  transition: background-color 0.15s ease;
}

.direction-toggle:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.direction-toggle .checkbox-icon {
  font-size: 1rem;
  line-height: 1;
}

.direction-toggle.imports-label .checkbox-icon {
  color: #e53935;
}

.direction-toggle.exports-label .checkbox-icon {
  color: #43a047;
}

.volume-header-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.35rem;
  padding: 0.5rem 0.75rem;
  border: 2px solid var(--type-color);
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: center;
  white-space: nowrap;
}

.volume-header-btn::before {
  content: '';
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background-color: var(--type-color);
  flex-shrink: 0;
}

.volume-header-btn.active::before {
  display: none;
}

.volume-header-btn:hover {
  opacity: 0.85;
  transform: translateY(-1px);
}

.volume-header-btn.active {
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

.volume-cell {
  text-align: center;
  padding: 0.5rem 0.25rem;
  border-radius: 4px;
  transition: opacity 0.15s ease;
}

.volume-cell.inactive {
  opacity: 0.3;
}

.volume-cell.imports {
  background: linear-gradient(135deg, #e8a87c11, #e8a87c22);
}

.volume-cell.exports {
  background: linear-gradient(135deg, #81b29a11, #81b29a22);
}

.volume-value {
  display: block;
  font-size: 1rem;
  font-weight: 600;
  color: #2c3e50;
}

.volume-unit {
  display: block;
  font-size: 0.65rem;
  color: #888;
  white-space: nowrap;
}

.no-data {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 3rem;
  color: #888;
}

.no-data-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.map-wrapper {
  display: flex;
  gap: 2.5rem;
  align-items: flex-start;
}

.map-container {
  width: 60%;
  min-width: 400px;
  max-width: 700px;
  flex-shrink: 0;
}

.map-svg-container {
  position: relative;
  background: #f5f5f5;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  min-height: 300px;
}

.map-svg-container :deep(svg) {
  display: block;
}

.map-svg-container :deep(.map-tooltip) {
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 8px 12px;
  font-size: 0.8rem;
  line-height: 1.4;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  z-index: 100;
  max-width: 250px;
}

.map-svg-container :deep(.map-tooltip strong) {
  color: #2c3e50;
}

.map-svg-container :deep(.map-tooltip .tooltip-section) {
  color: #666;
  font-weight: 500;
}

.map-svg-container :deep(.flow-arrow) {
  cursor: pointer;
}

.map-svg-container :deep(.map-error) {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 300px;
  color: #888;
  font-style: italic;
}

.map-controls {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 0.5rem;
  padding: 0.25rem 0;
}

.controls-left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.reset-zoom-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  padding: 0;
  border: 1px solid #ccc;
  border-radius: 4px;
  background: #fff;
  color: #666;
  cursor: pointer;
  transition: all 0.15s ease;
}

.reset-zoom-btn:hover {
  background: #f0f0f0;
  border-color: #999;
  color: #333;
}

.reset-zoom-btn .material-symbols-outlined {
  font-size: 18px;
}

.map-hint {
  font-size: 0.75rem;
  color: #999;
  font-style: italic;
}

.cutoff-slider {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.cutoff-label {
  font-size: 0.75rem;
  color: #666;
  white-space: nowrap;
}

.cutoff-range {
  width: 80px;
  height: 4px;
  cursor: pointer;
  accent-color: #2c3e50;
}

.cutoff-value {
  font-size: 0.75rem;
  color: #333;
  font-weight: 500;
  min-width: 28px;
  text-align: right;
}

.chart-meta {
  margin-top: 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  padding-top: 0.5rem;
  border-top: 1px solid #eee;
}

.meta-section {
  display: flex;
  flex-wrap: wrap;
  gap: 0.3rem;
  font-size: 0.7rem;
  line-height: 1.4;
}

.meta-label {
  font-weight: 600;
  color: #555;
  flex-shrink: 0;
}

.meta-text {
  color: #666;
}

.meta-text code {
  background: #e9ecef;
  padding: 0.05rem 0.25rem;
  border-radius: 2px;
  font-size: 0.65rem;
  color: #495057;
}

.meta-list {
  margin: 0.2rem 0 0 0;
  padding-left: 1.2rem;
  color: #666;
}

.meta-list li {
  margin-bottom: 0.15rem;
}

.meta-list code {
  background: #e9ecef;
  padding: 0.05rem 0.25rem;
  border-radius: 2px;
  font-size: 0.65rem;
  color: #495057;
}

.chart-notes {
  margin-top: 0.2rem;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.chart-note {
  display: flex;
  align-items: flex-start;
  gap: 0.35rem;
  margin: 0;
  font-size: 0.7rem;
  color: #777;
  line-height: 1.4;
}

.note-icon {
  flex-shrink: 0;
  font-weight: 600;
  color: #999;
}

.map-info {
  flex: 1;
  min-width: 0;
  font-size: 0.8rem;
  line-height: 1.5;
}

.info-section {
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #eee;
}

.info-section:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.info-section.data-hint-note {
  background: #f8f9fa;
  padding: 0.75rem;
  border-radius: 6px;
  border-bottom: none;
  margin-bottom: 1.25rem;
}

.info-section.data-hint-note .info-title {
  font-size: 0.8rem;
  color: #666;
}

.info-section.data-hint-note .info-text {
  font-size: 0.75rem;
  color: #666;
}

.info-title {
  font-weight: 600;
  font-size: 0.9rem;
  color: #333;
  margin-bottom: 0.4rem;
}

.info-text {
  margin: 0;
  color: #555;
  font-size: 0.8rem;
  line-height: 1.55;
}

.placeholder-content {
  background: repeating-linear-gradient(
    -45deg,
    transparent,
    transparent 10px,
    rgba(255, 193, 7, 0.05) 10px,
    rgba(255, 193, 7, 0.05) 20px
  );
  border-left: 3px solid #ffc107;
  padding-left: 0.75rem;
  border-radius: 0;
}

.placeholder-title {
  color: #996600;
  font-style: italic;
}

.placeholder-text {
  color: #888;
  font-style: italic;
}


@media (max-width: 900px) {
  .map-wrapper {
    flex-direction: column;
  }

  .map-container {
    width: 100%;
    max-width: none;
  }

  .map-info {
    width: 100%;
  }

  .volume-grid {
    font-size: 0.85rem;
  }

  .volume-value {
    font-size: 0.9rem;
  }
}
</style>
