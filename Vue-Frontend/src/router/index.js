import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import AadharForm from '../views/AadharForm.vue';
import PanForm from '../views/PanForm.vue';
import FinalPage from '../views/FinalPage.vue';
const routes = [
  {
    path: '/',
    name: 'home',
    component: HomePage
  },
  {
    path: '/aadhar',
    name: 'AadharForm',
    component: AadharForm
  },
  {
    path: '/pan',
    name: 'PanForm',
    component: PanForm
  },
  {
    path: '/FinalPage',
    name: 'FinalPage',
    component: FinalPage
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
