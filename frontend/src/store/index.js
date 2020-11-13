import Vue from 'vue'
import Vuex from 'vuex'

import AuthModule from '@/store/auth'
import AlertModule from '@/store/alert'
import OrderModule from '@/store/order'
import ApplicationModule from '@/store/application'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    loading: false
  },
  mutations: {
    START_LOADING (state) {
      state.loading = true
    },
    END_LOADING (state) {
      state.loading = false
    }
  },

  actions: {

  },
  modules: {
    auth: AuthModule,
    alert: AlertModule,
    order: OrderModule,
    application: ApplicationModule
  }
})
