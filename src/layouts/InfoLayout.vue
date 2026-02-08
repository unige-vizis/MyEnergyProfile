<script setup>
import Sidebar from "@/components/Sidebar.vue";

const infoItems = [
  { id: "/info/methodology", name: "Methodology", icon: "menu_book" },
  { id: "/info/members", name: "Members", icon: "group" },
];
</script>

<template>
  <div id="app-container">
    <Sidebar :sections="infoItems" mode="route" class="short-sidebar"/>
    <div class="main-content">
      <RouterView />
    </div>
  </div>
</template>
