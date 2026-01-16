<template>
  <div class="year-picker">
    <div class="picker-container" @click="toggleDropdown">
      <button
        class="arrow-btn up"
        @click.stop="incrementYear"
        :disabled="!canIncrement"
      >
        <svg width="12" height="8" viewBox="0 0 12 8">
          <path d="M1 6L6 1L11 6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" fill="none"/>
        </svg>
      </button>

      <div class="slot-window">
        <div
          class="slot-reel"
          :class="{ 'spinning-up': spinDirection === 'up', 'spinning-down': spinDirection === 'down' }"
          @animationend="onAnimationEnd"
        >
          <span class="year-display">{{ displayYear }}</span>
        </div>
      </div>

      <button
        class="arrow-btn down"
        @click.stop="decrementYear"
        :disabled="!canDecrement"
      >
        <svg width="12" height="8" viewBox="0 0 12 8">
          <path d="M1 2L6 7L11 2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" fill="none"/>
        </svg>
      </button>
    </div>

    <div v-if="isOpen" class="dropdown-overlay" @click="closeDropdown"></div>

    <div v-if="isOpen" class="dropdown-panel">
      <div class="year-grid">
        <button
          v-for="year in availableYears"
          :key="year"
          class="year-option"
          :class="{ selected: year === modelValue }"
          @click="selectYear(year)"
        >
          {{ year }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: [Number, String],
    default: null
  },
  years: {
    type: Array,
    default: () => []
  },
  min: {
    type: Number,
    default: 1990
  },
  max: {
    type: Number,
    default: 2024
  }
})

const emit = defineEmits(['update:modelValue'])

const isOpen = ref(false)
const spinDirection = ref(null)
const displayYear = ref(props.modelValue)

const availableYears = computed(() => {
  if (props.years && props.years.length > 0) {
    return [...props.years].sort((a, b) => b - a)
  }
  const years = []
  for (let y = props.max; y >= props.min; y--) {
    years.push(y)
  }
  return years
})

const currentIndex = computed(() => {
  return availableYears.value.indexOf(Number(props.modelValue))
})

const canIncrement = computed(() => {
  return currentIndex.value > 0
})

const canDecrement = computed(() => {
  return currentIndex.value < availableYears.value.length - 1
})

function incrementYear() {
  if (!canIncrement.value) return
  spinDirection.value = 'up'
  const newYear = availableYears.value[currentIndex.value - 1]
  emit('update:modelValue', newYear)
}

function decrementYear() {
  if (!canDecrement.value) return
  spinDirection.value = 'down'
  const newYear = availableYears.value[currentIndex.value + 1]
  emit('update:modelValue', newYear)
}

function onAnimationEnd() {
  spinDirection.value = null
  displayYear.value = props.modelValue
}

function toggleDropdown() {
  isOpen.value = !isOpen.value
}

function closeDropdown() {
  isOpen.value = false
}

function selectYear(year) {
  const oldIndex = currentIndex.value
  const newIndex = availableYears.value.indexOf(year)

  if (newIndex < oldIndex) {
    spinDirection.value = 'up'
  } else if (newIndex > oldIndex) {
    spinDirection.value = 'down'
  }

  emit('update:modelValue', year)
  closeDropdown()
}

// Watch for external changes
import { watch } from 'vue'
watch(() => props.modelValue, (newVal) => {
  if (!spinDirection.value) {
    displayYear.value = newVal
  }
})
</script>

<style scoped>
.year-picker {
  position: relative;
  display: inline-block;
}

.picker-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: #fff;
  border: 1px solid #d0d0d0;
  border-radius: 8px;
  padding: 0.25rem;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 70px;
}

.picker-container:hover {
  border-color: #999;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
}

.arrow-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  padding: 0.2rem;
  border: none;
  background: transparent;
  color: #666;
  cursor: pointer;
  transition: all 0.15s ease;
  border-radius: 4px;
}

.arrow-btn:hover:not(:disabled) {
  background: #f0f0f0;
  color: #333;
}

.arrow-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.slot-window {
  overflow: hidden;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(to bottom,
    rgba(0,0,0,0.03) 0%,
    transparent 30%,
    transparent 70%,
    rgba(0,0,0,0.03) 100%
  );
  border-radius: 4px;
  width: 100%;
}

.slot-reel {
  display: flex;
  align-items: center;
  justify-content: center;
}

.year-display {
  font-size: 1rem;
  font-weight: 600;
  color: #333;
  font-variant-numeric: tabular-nums;
}

.slot-reel.spinning-up {
  animation: spinUp 0.2s ease-out;
}

.slot-reel.spinning-down {
  animation: spinDown 0.2s ease-out;
}

@keyframes spinUp {
  0% {
    transform: translateY(100%);
    opacity: 0;
  }
  100% {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes spinDown {
  0% {
    transform: translateY(-100%);
    opacity: 0;
  }
  100% {
    transform: translateY(0);
    opacity: 1;
  }
}

.dropdown-overlay {
  position: fixed;
  inset: 0;
  z-index: 99;
}

.dropdown-panel {
  position: absolute;
  top: calc(100% + 4px);
  left: 50%;
  transform: translateX(-50%);
  z-index: 100;
  background: white;
  border: 1px solid #d0d0d0;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
  padding: 0.5rem;
  max-height: 200px;
  overflow-y: auto;
}

.year-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.25rem;
}

.year-option {
  padding: 0.4rem 0.6rem;
  border: none;
  background: transparent;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: 500;
  color: #555;
  transition: all 0.15s ease;
  font-variant-numeric: tabular-nums;
}

.year-option:hover {
  background: #f0f0f0;
  color: #333;
}

.year-option.selected {
  background: #333;
  color: #fff;
}
</style>
