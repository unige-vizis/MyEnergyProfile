import { createRouter, createWebHistory } from "vue-router";

const MainLayout = import("@/layouts/Home.vue");
const InfoLayout = import("@/layouts/InfoLayout.vue");


const routes = [
  {
    path: "/",
    component: MainLayout,
    children: [
      {
        path: "",
        component: () => import("@/layouts/Home.vue"),
      },
    ],
  },

  {
    path: "/info",
    component: InfoLayout,
    children: [
      {
        path: "",
        component: () => import("@/layouts/InfoLayout.vue"),
      },
    ],
  },
];


export default createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});
