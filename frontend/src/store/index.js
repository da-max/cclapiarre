import Vue from 'vue'
import Vuex from 'vuex'
import gql from 'graphql-tag'
import { apolloClient } from '@/vue-apollo'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    currentUser: {}
  },
  mutations: {
    LOGOUT_USER (state) {
      state.currentUser = {}
      window.localStorage.currentUser = JSON.stringify({})
    },
    SET_CURRENT_USER (state, user) {
      state.currentUser = user
      window.localStorage.currentUser = JSON.stringify(user)
    }
  },
  actions: {
    logoutUser ({ commit }) {
      commit('LOGOUT_USER')
    },
    async loginUser ({ commit }, { username, password }) {
      try {
        const response = await apolloClient.mutate({
          mutation: gql`mutation ($username: String!, $password: String!) {
            login(username: $username, password: $password) {
              token,
              user {
                id
                username
                email
                isSuperuser
                groups {
                  id
                  name
                }
              }
            }
          }`,
          variables: {
            username,
            password
          }
        })
        console.log(response)
        commit('SET_CURRENT_USER', response.data.login.user)
        return response.data.login
      } catch (e) {
        console.log(e)
        return { error: 'Username/password combinaison was incorrect. Please try again.' }
      }
    },
    loadUser ({ commit }) {
      const user = JSON.parse(window.localStorage.currentUser)
      commit('SET_CURRENT_USER', user)
    }
  },
  modules: {
  }
})
