import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/",
    component: () => import("@/layouts/Home.vue"),
  },
  {
    path: "/info",
    component: () => import("@/layouts/InfoLayout.vue"),
  },
];

export default createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});
