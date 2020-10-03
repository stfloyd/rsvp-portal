import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import { Submission } from '@/interfaces/app'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/RegistrationsList.vue')
  },
  {
    path: '/:registrationSlug',
    name: 'registration',
    component: () => import('@/views/Registration.vue')
  },
  {
    path: '/:registrationSlug/events/:eventSlug',
    name: 'registration-event',
    component: () => import('@/views/Event.vue')
  },
  {
    path: '/confirmation',
    name: 'confirmation',
    component: () => import('@/views/Confirmation.vue'),
    props: true
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
