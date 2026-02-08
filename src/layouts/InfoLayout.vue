<script setup>
import Members from "@/components/sections/Members.vue";
import Methodology from "@/components/sections/Methodology.vue";
import Sidebar from "@/components/Sidebar.vue";
import Footer from "@/components/Footer.vue";

const sections = [
  { id: "methodology", name: "Methodology", icon: "menu_book" },
  { id: "members", name: "Teammembers", icon: "group" },
];
</script>

<template>
  <div id="app-container">
    <Sidebar :sections="sections" class="short-sidebar"></Sidebar>
    <main>
      <div class="main-content">
        <Methodology />
        <Members />
      </div>
      <Footer></Footer>
    </main>
  </div>
</template>

<style scoped>
.main-content {
  margin-top: 2rem;
}
</style>
