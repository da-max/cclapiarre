import apolloClient from '@/vue-apollo'

import COFFEE_ALL from '@/graphql/Coffee/CoffeeAll.gql'

export default {
  namespaced: true,
  state: () => ({
    coffees: []
  }),

  mutations: {
    SET_COFFEE (state, coffees) {
      state.coffees = coffees
    }
  },
  actions: {
    async getCoffees ({ commit }) {
      commit('START_LOADING', null, { root: true })
      try {
        const response = await apolloClient.query({ query: COFFEE_ALL })
        console.log(response)
        commit('SET_COFFEE', response.data.coffee.edges)
      } catch (e) {
        commit('alert/ADD_ALERT', {
          header: false,
          body: `Une erreur est survenue, merci de réessayer : ${e}`,
          status: 'error',
          close: true
        })
      }
    }
  }
}
