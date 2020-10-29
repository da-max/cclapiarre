import Vue from 'vue'
import Vuex from 'vuex'
import gql from 'graphql-tag'
import { apolloClient } from '@/vue-apollo'

import AuthModule from '@/store/auth'
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
    auth: AuthModule
  }
})
