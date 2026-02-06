<script setup>
import { computed, ref, watch, nextTick } from 'vue'

const props = defineProps({
  modelValue: { type: Number, required: true },
  years: { type: Array, required: true },
  label: { type: String, default: '' }
})

const emit = defineEmits(['update:modelValue'])
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
</script>

<template>
  <div class="year-slot">
    <label v-if="label" class="year-slot-label">{{ label }}</label>
    <div class="year-slot-row">
      <button class="year-slot-btn" :disabled="!canGoUp" @click="go(-1)" type="button">
        <svg width="10" height="10" viewBox="0 0 10 10">
          <path d="M7 1L3 5L7 9" stroke="currentColor" stroke-width="1.5" fill="none" />
        </svg>
      </button>
      <div class="year-slot-display">
        <span class="year-adj">{{ prevYear || '' }}</span>
        <div class="year-drum">
          <span class="year-current" :class="{ 'year-pop': isAnimating }">{{ displayYear }}</span>
        </div>
        <span class="year-adj">{{ nextYear || '' }}</span>
      </div>
      <button class="year-slot-btn" :disabled="!canGoDown" @click="go(1)" type="button">
        <svg width="10" height="10" viewBox="0 0 10 10">
          <path d="M3 1L7 5L3 9" stroke="currentColor" stroke-width="1.5" fill="none" />
        </svg>
      </button>
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
  border: 1px solid var(--primary-color);
  border-radius: 6px;
  background: var(--primary-color);
  color: var(--text-color-dark-green);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.year-slot-btn:hover:not(:disabled) {
  border-color: var(--border-hover-color);
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
  border: 1px solid var(--primary-color);
  border-radius: 6px;
  background: var(--primary-color);
  cursor: pointer;
  transition: all 0.2s ease;
}

.year-adj {
  font-size: 0.8rem;
  color: var(--text-color-dark-green);
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
  color: var(--text-color-dark-green); /* ausgewähltes Jahr */
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
</style>
