import { createRouter, createWebHistory } from "vue-router";

import LandingView from "../views/LandingView.vue";

import UserView from "../views/UserView.vue";

import AdminView from "../views/AdminView.vue";

import TrekStaffView from "../views/TrekStaffView.vue";


import Login from '../components/auth/Login.vue'
import TrekkerRegister from '../components/auth/TrekkerRegister.vue'

const routes = [
  {
    path: "/",
    component: LandingView
  },
  {
    path: "/user",
    name : "user",
    component: UserView
  },
  {
    path: "/admin",
    name : "admin",
    component: AdminView
  },
  {
    path: "/staff",
    component: TrekStaffView
  },
  {
    path: "/login",
    name: "Login",
    component: Login
  },
  {
    path: "/register",
    component: TrekkerRegister
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;