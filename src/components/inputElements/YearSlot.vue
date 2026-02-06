<script setup>
import { computed, ref, watch, nextTick } from 'vue'

const props = defineProps({
  modelValue: { type: Number, required: true },
  years: { type: Array, required: true },
  label: { type: String, default: '' }
})

const emit = defineEmits(['update:modelValue'])
const showDropdown = ref(false)
const isAnimating = ref(false)
const displayYear = ref(props.modelValue)

const currentIndex = computed(() => props.years.indexOf(props.modelValue))
const canGoUp = computed(() => currentIndex.value > 0)
const canGoDown = computed(() => currentIndex.value < props.years.length - 1)
const prevYear = computed(() => canGoUp.value ? props.years[currentIndex.value - 1] : null)
const nextYear = computed(() => canGoDown.value ? props.years[currentIndex.value + 1] : null)

watch(() => props.modelValue, (newVal) => {
  displayYear.value = newVal
})

function go(dir) {
  const newIndex = currentIndex.value + dir
  if (newIndex >= 0 && newIndex < props.years.length) {
    changeTo(props.years[newIndex])
  }
}

function changeTo(year) {
  if (year === props.modelValue) return

  isAnimating.value = true
  displayYear.value = year
  emit('update:modelValue', year)

  setTimeout(() => {
    isAnimating.value = false
  }, 200)
}

function selectYear(year) {
  showDropdown.value = false
  if (year !== props.modelValue) {
    changeTo(year)
  }
}

function onClickOutside(e) {
  if (!e.target.closest('.year-slot')) showDropdown.value = false
}

watch(showDropdown, (val) => {
  if (val) document.addEventListener('click', onClickOutside)
  else document.removeEventListener('click', onClickOutside)
})
</script>

<template>
  <div class="year-slot">
    <label v-if="label" class="year-slot-label">{{ label }}</label>
    <div class="year-slot-row">
      <button class="year-slot-btn" :disabled="!canGoUp" @click="go(-1)" type="button">
        <svg width="10" height="10" viewBox="0 0 10 10"><path d="M7 1L3 5L7 9" stroke="currentColor" stroke-width="1.5" fill="none"/></svg>
      </button>
      <div class="year-slot-display" @click="showDropdown = !showDropdown">
        <span class="year-adj">{{ prevYear || '' }}</span>
        <div class="year-drum">
          <span class="year-current" :class="{ 'year-pop': isAnimating }">{{ displayYear }}</span>
        </div>
        <span class="year-adj">{{ nextYear || '' }}</span>
      </div>
      <button class="year-slot-btn" :disabled="!canGoDown" @click="go(1)" type="button">
        <svg width="10" height="10" viewBox="0 0 10 10"><path d="M3 1L7 5L3 9" stroke="currentColor" stroke-width="1.5" fill="none"/></svg>
      </button>
    </div>
    <div v-if="showDropdown" class="year-slot-dropdown">
      <div
        v-for="year in years"
        :key="year"
        class="year-slot-option"
        :class="{ active: year === modelValue }"
        @click.stop="selectYear(year)"
      >{{ year }}</div>
    </div>
  </div>
</template>

<style scoped>
.year-slot {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.year-slot-label {
  font-size: 0.9rem;
  font-weight: 500;
}

.year-slot-row {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
}

.year-slot-btn {
  height: 38px;
  width: 32px;
  border: 1px solid #999;
  border-radius: 6px;
  background: #e5e5e5;
  color: #555;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.year-slot-btn:hover:not(:disabled) {
  border-color: #b0b0b0;
  color: #333;
}

.year-slot-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.year-slot-display {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  height: 38px;
  padding: 0 0.75rem;
  border: 1px solid #000;
  border-radius: 6px;
  background: #fcf1e6; /* beige */
  cursor: pointer;
  transition: all 0.2s ease;
}


.year-slot-display:hover {
  border-color: #4c4c4c;
}

.year-adj {
  font-size: 0.8rem;
  color: #000; /* schwarz */
  opacity: 0.4; /* dezent */
  min-width: 2.5rem;
  text-align: center;
}


.year-drum {
  min-width: 2.5rem;
}

.year-current {
  display: block;
  font-size: 0.95rem;
  font-weight: 600;
  color: #acc278; /* ausgewähltes Jahr */
  text-align: center;
}


.year-pop {
  animation: pop 0.2s ease-out;
}

@keyframes pop {
  0% {
    transform: scale(0.8);
    opacity: 0.5;
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

.year-slot-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  margin-top: 4px;
  background: white;
  border: 1px solid #d0d0d0;
  border-radius: 6px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  max-height: 200px;
  overflow-y: auto;
  z-index: 100;
}

.year-slot-option {
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background 0.15s;
}

.year-slot-option:hover {
  background: #f0f0f0;
}

.year-slot-option.active {
  background: #4c4c4c;
  color: white;
}
</style>
