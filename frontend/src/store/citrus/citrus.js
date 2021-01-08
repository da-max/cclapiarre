import Vue from 'vue'
import apolloClient from '@/vue-apollo'

import CITRUS_ALL from '@/graphql/Citrus/CitrusAll.gql'

export default {
  namespaced: true,
  state: () => ({
    citrus: [],
    searchCitrus: []
  }),

  mutations: {
    SET_CITRUS (state, citrus) {
      const products = []
      citrus.forEach(c => {
        products.push({ ...c })
      })
      state.citrus = products
    },
    SET_SEARCH_CITRUS (state, searchCitrus) {
      state.searchCitrus = searchCitrus
    },
    SET_CHECK_CITRUS (state, { citrus, value }) {
      Vue.set(
        citrus,
        'check',
        value
      )
    },
    CHECK_ALL (state, value) {
      state.searchCitrus.forEach((citrus) => {
        Vue.set(
          citrus,
          'check',
          value
        )
      })
    }
  },

  actions: {
    async getCitrus ({ commit }) {
      commit('START_LOADING', null, { root: true })
      try {
        const response = await apolloClient.query({ query: CITRUS_ALL })
        commit('SET_CITRUS', response.data.citrus.edges)
      } catch (e) {
        commit('alert/ADD_ALERT', {
          header: false,
          body: `Une erreur est survenue, merci de réessayer : ${e}`,
          status: 'danger',
          close: true
        }, { root: true })
      } finally {
        commit('END_LOADING', null, { root: true })
      }
    }
  }
}
