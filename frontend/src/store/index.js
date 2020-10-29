import Vue from 'vue'
import Vuex from 'vuex'

import AuthModule from '@/store/auth'
import AlertModule from '@/store/alert'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    currentUser: {}
  },
  mutations: {

  },

  actions: {

  },
  modules: {
    auth: AuthModule,
    alert: AlertModule
  }
})
