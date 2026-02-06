<template>
  <div class="app-select-wrapper">
    <label v-if="label" :for="id" class="app-select-label">{{ label }}</label>
    <div class="app-select-container">
      <select
        :id="id"
        :value="modelValue"
        class="app-select"
        :disabled="disabled"
        @change="$emit('update:modelValue', $event.target.value)"
      >
        <option v-if="placeholder" value="" disabled>{{ placeholder }}</option>
        <option v-for="option in options" :key="option.key" :value="option.value">
          {{ option.label }}
        </option>
      </select>
      <span class="app-select-icon">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
          <path d="M4 6L8 10L12 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
        </svg>
      </span>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: ''
  },
  options: {
    type: Array,
    required: true,
    validator: (arr) => arr.every((item) => item.value !== undefined && item.label !== undefined)
  },
  label: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: ''
  },
  disabled: {
    type: Boolean,
    default: false
  },
  id: {
    type: String,
    default: () => `select-${Math.random().toString(36).substr(2, 9)}`
  }
});

defineEmits(['update:modelValue']);
</script>

<style scoped>
.app-select-wrapper {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.app-select-label {
  font-size: 0.9rem;
  font-weight: 500;
}

.app-select-container {
  position: relative;
  display: inline-block;
  width: 100%;
  max-width: 20rem;
}

.app-select {
  width: 100%;
  padding: 0.75rem 2.5rem 0.75rem 1rem;
  font-size: 0.95rem;
  border: 1px solid #d0d0d0;
  border-radius: 6px;
  background-color: white;
  color: var(--text-color-dark-green);
  cursor: pointer;
  transition: all 0.2s ease;
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
}

.app-select:hover:not(:disabled) {
  border-color: var(--border-hover-color);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.app-select:focus {
  outline: none;
  border-color: var(--border-hover-color);
  box-shadow: 0 0 0 3px rgba(76, 76, 76, 0.1);
}

.app-select:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  background-color: var(--placeholder-color);
}

.app-select-icon {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  pointer-events: none;
  color: var(--text-color-dark-green);
  display: flex;
  align-items: center;
  justify-content: center;
}

.app-select:disabled ~ .app-select-icon {
  opacity: 0.5;
}
</style>
