<template>
  <div class="item-slider-container">
    <div class="item-slider">
      <div @click="slide(-slidewith)" :class="{ 'is-disabled-hide': scrollX < 1 }" class="left-arrow-left">
        <span class="timeline-icon material-symbols-outlined">chevron_left</span>
      </div>
      <div id="slider-container" ref="scrl" @scroll="scrollCheck" class="item-container">
        <slot></slot>
      </div>
      <div @click="slide(slidewith)" :class="{ 'is-disabled-hide': scrollEnd }" class="right-arrow-right">
        <span class="timeline-icon material-symbols-outlined">chevron_right</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ItemsSlider',
  data() {
    return {
      scrollX: 0,
      scrollEnd: false,
      slidewith: 100
    };
  },
  mounted() {
    this.$nextTick(() => {
        const sliderContainer = document.getElementById('slider-container')
        if (sliderContainer) {
        const sliderContainerWidth = sliderContainer.clientWidth
        const itemsToShow = document.documentElement.clientWidth < 600 ? 1 : 2
        this.slidewith = sliderContainerWidth / itemsToShow + (document.documentElement.clientWidth < 600 ? 10 : 0)
        }
    })
  },
  methods: {
    slide(shift) {
      this.$refs.scrl.scrollBy({
        left: shift,
        behavior: 'smooth'
      });

      this.$refs.scrl.scrollLeft += shift;
      this.scrollX += shift;

      if (Math.floor(this.$refs.scrl.scrollWidth - this.$refs.scrl.scrollLeft) <= this.$refs.scrl.offsetWidth) {
        this.scrollEnd = true;
      } else {
        this.scrollEnd = false;
      }
    },
    scrollCheck() {
      this.scrollX = this.$refs.scrl.scrollLeft;

      if (Math.floor(this.$refs.scrl.scrollWidth - this.$refs.scrl.scrollLeft) <= this.$refs.scrl.offsetWidth) {
        this.scrollEnd = true;
      } else {
        this.scrollEnd = false;
      }
    }
  },
  props: {
    title: String
  }
};
</script>

<style scoped>
.item-slider-container {
  margin-bottom: 20px;
}
.item-title {
  font-weight: bold;
}
.item-slider {
  display: flex;
  align-items: center;
  position: relative;
}
.item-container {
  display: flex;
  overflow-x: hidden;
  scroll-behavior: smooth;
  gap: 10px;
}
.left-arrow-left,
.right-arrow-right {
  cursor: pointer;
  padding: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: opacity 0.3s ease;
}
.left-arrow-left.is-disabled-hide,
.right-arrow-right.is-disabled-hide {
  opacity: 0.5;
  pointer-events: none;
}
.timeline-icon {
  font-size: 24px;
}
</style>
