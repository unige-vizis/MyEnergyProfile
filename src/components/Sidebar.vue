<template>
  <aside class="timeline-sidebar">
    <div class="sidebar-content">
      <div>
        <h1>My Energy Profile</h1>
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
  { id: "global", name: "Global comparison", icon: "globe", },
  { id: "costs", name: "Energy costs", icon: "euro", },
  { id: "availability", name: "Availability of energy", icon: "location_on",},
  { id: "mix", name: "My energy mix", icon: "instant_mix", },
  { id: "household", name: "My household", icon: "home", },
  { id: "transition", name: "Energy transition in context", icon: "energy",},
  { id: "if", name: "What if?", icon: "question_mark", },
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
  width: 300px;
  height: 100vh;

  background: #acc278;
  color: #1a1a1a;

  box-shadow: 4px 0 12px rgba(0, 0, 0, 0.12);
  z-index: 1000;

  font-family: "Inria Serif", serif;
  font-weight: 500;
}


.sidebar-content {
  display: flex;
  height: 100%;
  flex-direction: column;

  padding: 2rem 1rem;
  overflow: hidden;
  background: transparent;
}

.timeline-sidebar *:not(.material-symbols-outlined) {
  font-family: "Inria Serif", serif !important;
}

.timeline-sidebar h1 {
  padding-top: 1.7rem;

  font-size: 1.9rem;
  font-weight: 1000;
  margin: 0 0 1.25rem 0;
  padding-bottom: 2.2rem;
}


.timeline-nav {
  flex: 1;
  position: relative;
  --axis-x: 56px;
  color:#acc278;
}



.timeline-line {
  display: none;
}


.timeline-sections {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: calc(100% - 140px); /* reserviert unten Platz */
  padding-bottom: 1rem;
}


.timeline-item {
  display: flex;
  align-items: center;
  gap: 0.85rem;

  padding: 0.55rem 0.75rem;  /* kleiner */
  border-radius: 10px;
  text-decoration: none;
  cursor: pointer;

 
  background: rgba(255, 255, 255, 0.18);
  border: 1.5px solid rgba(0, 0, 0, 0.55);

  color: rgba(0, 0, 0, 0.85);

  transition: transform 0.15s ease, box-shadow 0.15s ease, background 0.15s ease;
}


.timeline-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 18px rgba(0, 0, 0, 0.12);
  background: rgba(255, 255, 255, 0.28);
}


.timeline-item.active {
  background: rgba(255, 255, 255, 0.38);
  border-color: rgba(0, 0, 0, 0.8);
}

.timeline-dot {
  display: grid;
  place-items: center;

  width: 28px;
  height: 28px;
  border-radius: 999px;

  background: rgba(255, 255, 255, 0.28);
  border: 1.5px solid rgba(0, 0, 0, 0.65);

  flex: 0 0 28px;
}


.timeline-icon {
  font-size: 18px;
  color: rgba(0, 0, 0, 0.75);
}

.timeline-label {
  white-space: nowrap;
  flex: 1;
  opacity: 1;
  font-weight: 600;
  font-size: 0.85rem;
}

</style>
