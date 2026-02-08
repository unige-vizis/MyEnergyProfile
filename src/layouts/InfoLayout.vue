<script setup>
import Members from "@/components/sections/Members.vue";
import Methodology from "@/components/sections/Methodology.vue";
import Sidebar from "@/components/Sidebar.vue";

const sections = [
  { id: "methodology", name: "Methodology", icon: "menu_book" },
  { id: "members", name: "Members", icon: "group" },
];
</script>

<template>
  <div id="app-container">
    <Sidebar :sections="sections" class="short-sidebar"></Sidebar>
    <div class="main-content">
      <Methodology />
      <Members />
    </div>
  </div>
</template>
