<template>
  <button
    :id="id"
    :type="type"
    :class="class"
    class="app-btn"
    :disabled="disabled"
    @focus="$emit('focus')"
    @blur="$emit('blur')"
    @click="$emit('click')"
  >
    {{ label }}
  </button>
  <p v-if="error" class="app-btn-error">{{ error }}</p>
</template>

<script setup>
defineProps({
  class: {
    type: String,
    default: ''
  },
  type: {
    type: String,
    default: 'button',
    validator: (value) => ['submit', 'reset', 'button'].includes(value)
  },
  placeholder: {
    type: String,
    default: ''
  },
  label: {
    type: String,
    default: ''
  },
  error: {
    type: String,
    default: ''
  },
  disabled: {
    type: Boolean,
    default: false
  },
  id: {
    type: String,
    default: () => `input-${Math.random().toString(36).substr(2, 9)}`
  },
  click: {
    type: Function,
    default: () => {}
  }
});

defineEmits([ 'focus', 'blur', 'click' ]);
</script>

<style scoped>
.app-btn {
  padding: 0.75rem 1rem;
  border: 1px solid #d0d0d0;
  border-radius: 6px;
  background-color: white;
  color: #333;
  transition: all 0.2s ease;
  font-family: inherit;
}

.app-btn.active {
  border-color: #4c4c4c;
  background-color: #f0f0f0;
}

.app-btn:hover:not(:disabled) {
  border-color: #b0b0b0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.app-btn:focus {
  outline: none;
  border-color: #4c4c4c;
  box-shadow: 0 0 0 3px rgba(76, 76, 76, 0.1);
}

.app-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  background-color: #f5f5f5;
}

.app-btn-error {
  margin: 0;
  font-size: 0.85rem;
  color: #d32f2f;
  line-height: 1.4;
}
</style>
