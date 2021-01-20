import Vue from 'vue'
import VueRouter from 'vue-router'

import { loginRequired, utilsBeforeEach, utilsAfterEach, applicationPermissionRequired } from '@/router/utils'
import applicationRoutes from './application'
import coffeeRoutes from './coffee'
import citrusRoutes from './citrus'

const CONNECTION_URL = '/compte/connexion'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import(/* webpackChunkName: "home" */ '../views/Home.vue')
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/compte/liste-des-adherents',
    name: 'MemberList',
    component: () => import(/* webpackChunkName: "member-list" */ '../views/Registration/MemberList.vue'),
    meta: { loginRequired: true }
  },
  {
    path: '/compte/connexion',
    name: 'Login',
    component: () => import(/* webpackChunkName: "login" */ '../views/Registration/Login.vue')
  },
  ...citrusRoutes,
  ...coffeeRoutes,
  ...applicationRoutes
]

const router = new VueRouter({
  routes,
  mode: 'hash'
})

router.beforeEach(async (to, from, next) => {
  utilsBeforeEach()
  let go = true

  if (to.matched.some(record => record.meta.loginRequired)) {
    go = await loginRequired(to, from)
  }

  if (to.matched.some(record => record.meta.applicationPermission) && go) {
    go = await applicationPermissionRequired(to, from, to.meta.applicationPermission)
  }

  go ? next() : next(`${CONNECTION_URL}?next=${to.path}`)
})

router.afterEach((_to, _from) => {
  utilsAfterEach()
})
export default router
