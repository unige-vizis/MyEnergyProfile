import { createRouter, createWebHistory } from "vue-router";

import MainLayout from "@/layouts/MainLayout.vue";
import InfoLayout from "@/layouts/InfoLayout.vue";

import Consumption from "@/components/sections/Consumption.vue";
import Costs from "@/components/sections/Costs.vue";
import Dependency from "@/components/sections/Dependency.vue";
import ETransition from "@/components/sections/ETransition.vue";

// Passe die beiden Imports exakt an deine echten Dateinamen an:
import ProductionCons from "@/components/sections/ProductionConsumption.vue";
import TradingPartner from "@/components/sections/TradingPartner.vue";       // <- ggf. TradingPartner.vue oder TradingPartnerSection.vue

// Du hast Methodology.vue aktuell in sections – wir können es trotzdem für /info nutzen:
import Methodology from "@/components/sections/Methodology.vue";

// Members hast du (noch) nicht im Screenshot -> Datei anlegen, z.B.:
import Members from "@/components/info/Members.vue";

const routes = [
  {
    path: "/",
    component: MainLayout,
    children: [
      { path: "", redirect: "/consumption" },

      { path: "consumption", component: Consumption, meta: { title: "My energy consumption" } },
      { path: "costs", component: Costs, meta: { title: "Energy costs" } },
      { path: "dependency", component: Dependency, meta: { title: "Dependency on imports" } },
      { path: "transition", component: ETransition, meta: { title: "Energy transition in context" } },

      // Diese Pfade sind frei wählbar – nur Sidebar "to" muss gleich sein:
      { path: "production-consumption", component: ProductionCons, meta: { title: "Production & Consumption" } },
      { path: "trading-partners", component: TradingPartner, meta: { title: "The Trading Partners" } },
    ],
  },

  {
    path: "/info",
    component: InfoLayout,
    children: [
      { path: "", redirect: "/info/methodology" },
      { path: "methodology", component: Methodology, meta: { title: "Methodology" } },
      { path: "members", component: Members, meta: { title: "Members" } },
    ],
  },
];

export default createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});
