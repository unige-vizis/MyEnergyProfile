<template>
  <aside class="timeline-sidebar">
    <div class="sidebar-content">
      <div class="logo-section">
        <h1 class="app-name">EnergyLens</h1>
      </div>

      <nav class="timeline-nav">
        <div class="timeline-line"></div>
        <ul>
          <li v-for="section in sections" :key="section.id">
            <a
              :href="`#${section.id}`"
              @click.prevent="scrollToSection(section.id)"
              :class="{ active: currentSection === section.id }"
              class="timeline-item"
            >
              <div class="timeline-dot"></div>
              <span class="timeline-label">{{ section.name }}</span>
            </a>
          </li>
        </ul>
      </nav>
    </div>
  </aside>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const currentSection = ref('features')
const sections = ref([
  { id: 'features', name: 'Features' },
  { id: 'about', name: 'About' },
  { id: 'data', name: 'Data Sources' },
  { id: 'contact', name: 'Contact' }
])

const scrollToSection = (sectionId) => {
  const element = document.getElementById(sectionId)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' })
  }
}

const handleScroll = () => {
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
  window.addEventListener('scroll', handleScroll)
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
  width: 200px;
  background-color: #1a1a1a;
  color: white;
  box-shadow: 4px 0 12px rgba(0, 0, 0, 0.4);
  overflow-y: auto;
  z-index: 1000;
}

.sidebar-content {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 2rem 0;
}

.logo-section {
  text-align: center;
  padding: 0 1.5rem;
  margin-bottom: 2.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}

.logo {
  font-size: 2.5rem;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-8px); }
}

.app-name {
  font-size: 1.25rem;
  font-weight: 700;
  margin: 0;
  letter-spacing: 0.5px;
  color: #ffffff;
}

.timeline-nav {
  flex: 1;
  padding: 0 1rem;
  position: relative;
}

.timeline-line {
  position: absolute;
  left: 50%;
  top: 0;
  bottom: 0;
  width: 2px;
  background: linear-gradient(to bottom, #444, #333, #444);
  transform: translateX(-50%);
}

.timeline-nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 2rem;
  position: relative;
  z-index: 1;
}

.timeline-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem 1rem;
  color: #aaa;
  text-decoration: none;
  transition: all 0.3s ease;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  position: relative;
}

.timeline-dot {
  min-width: 16px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background-color: #444;
  border: 2px solid #555;
  transition: all 0.3s ease;
  position: relative;
  z-index: 2;
}

.timeline-label {
  white-space: nowrap;
  flex: 1;
  opacity: 0.7;
}

.timeline-item:hover {
  color: #ddd;
}

.timeline-item:hover .timeline-dot {
  border-color: #666;
  background-color: #555;
  box-shadow: 0 0 8px rgba(255, 255, 255, 0.2);
}

.timeline-item.active {
  color: #ffffff;
}

.timeline-item.active .timeline-dot {
  background-color: #ffffff;
  border-color: #ffffff;
  width: 24px;
  height: 24px;
  margin-left: -4px;
  box-shadow: 0 0 12px rgba(255, 255, 255, 0.5);
}

.timeline-item.active .timeline-label {
  opacity: 1;
  font-weight: 600;
}

.sidebar-footer {
  padding: 1.5rem;
  border-top: 1px solid #333;
  text-align: center;
}

.version {
  font-size: 0.7rem;
  color: #666;
  margin: 0;
}
</style>
