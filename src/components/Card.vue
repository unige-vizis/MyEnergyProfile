<template>
  <div class="card">
    <img :src="props.imgSrc" alt="Card image" v-if="props.imgSrc" />
    <div class="content">
      <h4>{{ props.title }}</h4>
      <p>
        {{ props.content }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'

const props = defineProps({
  title: String,
  imgSrc: String,
  content: String,
})

onMounted(() => {
    const sliderContainer = document.getElementById('slider-container')
    if (sliderContainer) {
    const observer = new ResizeObserver(entries => {
            const width = entries[0].contentRect.width
            const gapWidth = 10
            const itemsToShow = 2
            const itemWidth = (width / itemsToShow) - gapWidth
            document.documentElement.style.setProperty('--item-width', `${itemWidth}px`)
        })
        observer.observe(sliderContainer)
    }
})
</script>

<style scoped>
.card {
  width: var(--item-width);
  border-radius: 8px;
  box-sizing: border-box;
  border: 1px solid var(--border-color);
  height: 100%;
}
.card h4 {
  margin: 0 0 8px;
}
.card .content {
  display: flex;
  flex-direction: column;
  padding: 16px 32px;
}
.card img {
  width: 100%;
  height: 200px;
  border-radius: 4px 4px 0 0;
  object-fit: cover;
  object-position: center;
}
.card .content p {
  font-size: 0.9em;
}
</style>
