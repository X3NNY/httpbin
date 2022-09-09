import {createRouter, createWebHashHistory} from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'index',
    redirect: '/index',
    component: () => import('@/views/index'),
    children: [
      {
        path: 'index',
        name: 'httpbin',
        component: () => import('@/views/httpbin')
      }, {
        path: 'login',
        name: 'login',
        component: () => import('@/views/login')
      }, {
        path: 'register',
        name: 'register',
        component: () => import('@/views/register')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
