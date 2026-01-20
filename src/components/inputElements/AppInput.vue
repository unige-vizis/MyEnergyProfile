<template>
  <div class="app-input-wrapper">
    <label v-if="label" :for="id" class="app-input-label">{{ label }}</label>
    <div class="app-input-container">
      <input
        :id="id"
        :type="type"
        class="app-input"
        :placeholder="placeholder"
        :value="modelValue"
        :disabled="disabled"
        :readonly="readonly"
        @input="$emit('update:modelValue', $event.target.value)"
        @focus="$emit('focus')"
        @blur="$emit('blur')"
      />
      <span v-if="icon" class="app-input-icon">
        <slot name="icon">{{ icon }}</slot>
      </span>
    </div>
    <p v-if="description" class="app-input-description">{{ description }}</p>
    <p v-if="error" class="app-input-error">{{ error }}</p>
  </div>
</template>

<script setup>
defineProps({
  modelValue: {
    type: [String, Number],
    default: ''
  },
  type: {
    type: String,
    default: 'text',
    validator: (value) => ['text', 'email', 'password', 'number', 'tel', 'url'].includes(value)
  },
  placeholder: {
    type: String,
    default: ''
  },
  label: {
    type: String,
    default: ''
  },
  description: {
    type: String,
    default: ''
  },
  error: {
    type: String,
    default: ''
  },
  icon: {
    type: String,
    default: ''
  },
  disabled: {
    type: Boolean,
    default: false
  },
  readonly: {
    type: Boolean,
    default: false
  },
  id: {
    type: String,
    default: () => `input-${Math.random().toString(36).substr(2, 9)}`
  }
});

defineEmits(['update:modelValue', 'focus', 'blur']);
</script>

<style scoped>
.app-input-wrapper {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.app-input-label {
  font-size: 0.9rem;
  font-weight: 500;
}

.app-input-container {
  position: relative;
  display: inline-block;
  width: 100%;
}

.app-input {
  width: 100%;
  padding: 0.75rem 1rem;
  font-size: 0.95rem;
  border: 1px solid #d0d0d0;
  border-radius: 6px;
  background-color: white;
  color: #333;
  transition: all 0.2s ease;
  font-family: inherit;
}

.app-input::placeholder {
  color: #999;
}

.app-input:hover:not(:disabled):not(:readonly) {
  border-color: #b0b0b0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.app-input:focus {
  outline: none;
  border-color: #4c4c4c;
  box-shadow: 0 0 0 3px rgba(76, 76, 76, 0.1);
}

.app-input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  background-color: #f5f5f5;
}

.app-input:readonly {
  background-color: #f9f9f9;
  cursor: default;
}

.app-input-icon {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #999;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
  pointer-events: none;
}

.app-input-description {
  margin: 0;
  font-size: 0.85rem;
  color: #666;
  line-height: 1.4;
}

.app-input-error {
  margin: 0;
  font-size: 0.85rem;
  color: #d32f2f;
  line-height: 1.4;
}
</style>
