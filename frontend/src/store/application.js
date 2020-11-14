import apolloClient from '@/vue-apollo'

import APPLICATION_ALL from '@/graphql/Application/ApplicationAll.gql'

export default {
  namespaced: true,
  state: () => ({
    applications: []
  }),

  mutations: {
    SET_APPLICATIONS (state, applications) {
      state.applications = applications
    }
  },

  actions: {
    async getApplications ({ commit }) {
      commit('START_LOADING', null, { root: true })
      try {
        const response = await apolloClient.query({ query: APPLICATION_ALL })
        console.log(response)
        commit('SET_APPLICATIONS', response.data.allApplications)
      } catch (e) {
        commit('alert/ADD_UNKNOWN', null, { root: true })
      } finally {
        commit('END_LOADING', null, { root: true })
      }
    }
  },
  getters: {
    applicationBySlug (state) {
      return (slug) => state.applications.find(application => application.slug === slug)
    },
    idApplicationBySlug (_state, getters) {
      return (slug) => getters.applicationBySlug(slug).id
    }
  }
}
