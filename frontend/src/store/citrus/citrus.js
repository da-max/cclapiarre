import Vue from 'vue'
import apolloClient from '@/vue-apollo'

import CITRUS_ALL from '@/graphql/Citrus/CitrusAll.gql'
import BATCH_CITRUS_PATCH from '@/graphql/Citrus/BatchCitrusPatch.gql'

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
      const product = state.citrus.find((c) => c.node.id === citrus.node.id)
      Vue.set(
        product,
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
    },
    async patchCitrus ({ commit, getters }, { key, value }) {
      commit('START_LOADING', null, { root: true })
      try {
        const variables = getters.citrusChecked.map(citrus => {
          console.log(key)
          const c = { id: citrus.node.id }
          c[key.key] = key.value
          console.log(c)
          return c
        })
        console.log(variables)
        const response = await apolloClient.mutate({ mutation: BATCH_CITRUS_PATCH, variables: { citrus: variables } })
        console.log(response)
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
  },
  getters: {
    citrusById (state) {
      return (citrusId) => state.citrus.find((citrus) => citrus.node.id === citrusId)
    },
    citrusChecked: (state) => state.citrus.filter(c => c.check)

  }
}
