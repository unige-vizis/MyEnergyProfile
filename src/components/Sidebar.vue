<template>
  <aside class="timeline-sidebar">
    <div class="sidebar-content">
      <div>
        <h1 class="sidebar-title">My Energy Profile</h1>
      </div>

      <nav class="timeline-nav">
        <div class="timeline-line"></div>
        <div class="timeline-sections">
          <div v-for="section in sections" :key="section.id">
            <a
              :href="`#${section.id}`"
              @click.prevent="scrollToSection(section.id)"
              :class="{ active: currentSection === section.id }"
              class="timeline-item"
            >
              <div class="timeline-dot">
                <span class="timeline-icon material-symbols-outlined">{{ section.icon }}</span>
              </div>
              <span class="timeline-label">{{ section.name }}</span>
            </a>
          </div>
        </div>
      </nav>
    </div>
  </aside>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const currentSection = ref('consumption')
const sections = ref([
  { id: "consumption", name: "My energy consumption", icon: "battery_android_frame_5", },
  { id: "productionconsumption", name: "Production & Consumption", icon: "instant_mix", },
  { id: "costs", name: "Energy costs", icon: "euro", },
  { id: "tradingpartner", name: "The Trading Partners", icon: "cycle",},
  { id: "dependency", name: "Dependency on imports", icon: "trending_up",},
  { id: "transition", name: "Energy transition in context", icon: "energy",},
]);

const scrollToSection = (sectionId) => {
  const element = document.getElementById(sectionId)
  const container = document.querySelector('.main-content')
  if (element && container) {
    // scroll the container so the element is visible
    const containerRect = container.getBoundingClientRect()
    const elemRect = element.getBoundingClientRect()
    const offset = elemRect.top - containerRect.top + container.scrollTop
    window.scrollTo({ top: offset, behavior: 'smooth' })
  } else if (element) {
    element.scrollIntoView({ behavior: 'smooth' })
  }
}

const handleScroll = () => {
  const container = document.querySelector('.main-content')

  // Use window scroll approach - this is what's actually scrolling
  const scrollPosition = window.scrollY + window.innerHeight / 3

  for (const section of sections.value) {
    const element = document.getElementById(section.id)
    if (element) {
      const { offsetTop, offsetHeight } = element
      if (scrollPosition >= offsetTop && scrollPosition < offsetTop + offsetHeight) {
        currentSection.value = section.id
        break
      }
    }
  }
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll, { passive: true })
  handleScroll()
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
.timeline-sidebar {
  position: fixed;
  left: 0;
  top: 0;
  height: 100vh;
  background-color: var(--secondary-color);
  color: var(--text-color-dark-green);
  box-shadow: 4px 0 12px rgba(0, 0, 0, 0.4);
  z-index: 1000;
}

.sidebar-title {
  margin-left: 1rem;
  margin-top: 0;
  margin-bottom: 2rem;
}

.sidebar-content {
  display: flex;
  height: 100%;
  flex-direction: column;
  padding: 2rem 1rem;
  overflow: hidden;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-8px); }
}

.timeline-nav {
  flex: 1;
  position: relative;
}

.timeline-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem 1rem;
  color: var(--text-color-dark-green);
  text-decoration: none;
  transition: all 0.3s ease;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  position: relative;
  background-color: var(--secondary-color);
}

.timeline-dot {
  display: flex;
  align-items: center;
  min-width: 30px;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background-color: var(--primary-color);
  transition: all 0.3s ease;
  position: relative;
  z-index: 2;
}

.timeline-icon {
  margin: auto;
}

.timeline-label {
  white-space: nowrap;
  flex: 1;
  opacity: 0.7;
}

.timeline-sections {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 90%;
  z-index: 1;
}

.timeline-line {
  position: absolute;
  left: 32px;
  top: 0.5rem;
  bottom: 0.5rem;
  width: 2px;
  height: 85%;
  background: linear-gradient(to bottom, #444, #333, #444);
  transform: translateX(-50%);
}

.timeline-item:hover .timeline-dot {
  border-color: var(--text-color-dark-green);
  background-color: var(--primary-color);
  box-shadow: 0 0 8px rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

.timeline-item.active {
  color: var(--primary-color);
}

.timeline-item.active .timeline-dot {
  color: var(--text-color-dark-green);
  background-color: var(--primary-color);
  border-color: var(--primary-color);
  width: 40px;
  height: 40px;
  margin-left: -4px;
  box-shadow: 0 0 12px rgba(255, 255, 255, 0.5);
}

.timeline-item.active .timeline-label {
  opacity: 1;
  font-weight: 600;
}
</style>
