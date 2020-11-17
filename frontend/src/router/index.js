import Vue from 'vue'
import VueRouter from 'vue-router'

import { groupRequired } from '@/router/utils'
import Home from '../views/Home.vue'
import { applicationPermissionRequired, loginRequired, utilsBeforeEach, utilsAfterEach } from './utils'

const CONNECTION_URL = '/compte/connexion'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
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
    beforeEnter: async (to, from, next) => {
      if (loginRequired(to, from) && groupRequired(to, from, 'members')) {
        next()
      } else {
        next(`${CONNECTION_URL}?next=${to.path}`)
      }
    }
  },
  {
    path: '/compte/connexion',
    name: 'Login',
    component: () => import(/* webpackChunkName: "login" */ '../views/Registration/Login.vue')
  },
  {
    path: '/:application/commander',
    name: 'Order',
    component: () => import(/* webpackChunkName: "application-order" */ '../views/Application/Product/Order.vue'),
    props: route => ({ applicationSlug: route.params.application }),
    beforeEnter: async (to, from, next) => {
      const logged = await loginRequired(to, from)
      const application = await applicationPermissionRequired(to, from, 'members')
      if (logged && application) {
        next()
      } else {
        next(`${CONNECTION_URL}?next=${to.path}`)
      }
    }
  }
]

const router = new VueRouter({
  routes,
  mode: 'hash'
})

router.beforeEach((_to, _from, next) => {
  utilsBeforeEach()
  next()
})

router.afterEach((_to, _from) => {
  utilsAfterEach()
})
export default router
