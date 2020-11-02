import apolloClient from '@/vue-apollo'

import USER_LOGIN from '@/graphql/User/UserLogin.gql'
import USER_LOGOUT from '@/graphql/User/UserLogout.gql'
import USER_CURRENT from '@/graphql/User/UserCurrent.gql'

export default {
  namespaced: true,
  state: () => {
    return { currentUser: {} }
  },

  mutations: {
    LOGOUT_USER (state) {
      state.currentUser = {}
    },
    SET_CURRENT_USER (state, user) {
      state.currentUser = user
    }
  },

  actions: {
    async logoutUser ({ commit }) {
      try {
        const response = await apolloClient.mutate({
          mutation: USER_LOGOUT
        })
        commit('LOGOUT_USER')
        return response.data.logout.ok
      } catch {
        return { error: 'Vous n’avez pas pu être déconnecté. Merci de réessayer.' }
      }
    },

    async loginUser ({ commit }, { username, password }) {
      try {
        const response = await apolloClient.mutate({
          mutation: USER_LOGIN,
          variables: {
            username,
            password
          }
        })

        const user = response.data.login.user
        commit('SET_CURRENT_USER', user)
        return response.data.login
      } catch (e) {
        return { error: 'Nom d’utilisateur ou mot de passe incorrect. Merci de réessayer.' }
      }
    },

    /*
    This action get user with the sessionid cookie if the user is logged.
    */
    async loadUser ({ commit }) {
      const response = await apolloClient.query({
        query: USER_CURRENT
      })
      commit('SET_CURRENT_USER', response.data.user)
    }
  }
}
