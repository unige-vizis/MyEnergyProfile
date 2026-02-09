<template>
  <footer class="site-footer">
    <div class="footer-names">
      <div class="name-with-tooltip">
        <span class="footer-name">Matteo Gläser</span>
        <div class="tooltip">Data research, development & data set management</div>
      </div>

      <div class="name-with-tooltip">
        <span class="footer-name">Petula Arnold</span>
        <div class="tooltip">Concept, statistics & content structure</div>
      </div>

      <div class="name-with-tooltip">
        <span class="footer-name">Maleah Leonie Kögler</span>
        <div class="tooltip">Design, storytelling & content structure</div>
      </div>
    </div>

    <div class="footer-right">
      <button
        class="methodology-button"
        @click="openMethodology"
        type="button"
        aria-label="Info / Methodology"
        title="Info / Methodology"
      >
        <span class="material-symbols-outlined">info</span>
      </button>
      <span class="footer-title">VIZIS</span>
    </div>
  </footer>
</template>

<script setup>
import { useRouter } from "vue-router";
const router = useRouter();
function openMethodology() {
  router.push("/info");
}
</script>

<style scoped>
.methodology-button {
    display: none;
}
@media (max-width: 600px) {
    .methodology-button {
        display: flex;
        margin-left: 0;
    }
}
</style>
