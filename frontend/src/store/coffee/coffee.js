import Vue from 'vue'
import apolloClient from '@/vue-apollo'

import COFFEE_ALL from '@/graphql/Coffee/CoffeeAll.gql'
import ORDER_BY_USER_ID from '@/graphql/Coffee/Order/OrderByUserId.gql'
import ADD_ORDER from '@/graphql/Coffee/Order/OrderAdd.gql'

export default {
  namespaced: true,
  state: () => ({
    coffees: [],
    coffeeOrderedId: 0,
    order: [],
    hasOrder: false
  }),

  mutations: {
    SET_COFFEE (state, coffees) {
      state.coffees = coffees
    },

    ADD_COFFEE_ORDER (state, coffee) {
      state.order.push({
        id: state.coffeeOrderedId,
        coffee,
        weight: null,
        type: null,
        amount: 1
      })
      state.coffeeOrderedId++
    },

    REMOVE_COFFEE_ORDER (state, orderId) {
      state.order = state.order.filter((coffee) => coffee.id !== orderId)
    },

    SET_COFFEE_ORDER_WEIGHT (state, { orderId, weight }) {
      Vue.set(
        state.order.find((coffee) => coffee.id === orderId),
        'weight',
        weight
      )
    },

    SET_COFFEE_ORDER_TYPE (state, { orderId, type }) {
      Vue.set(
        state.order.find((coffee) => coffee.id === orderId),
        'type',
        type
      )
    },

    SET_COFFEE_ORDER_AMOUNT (state, { orderId, amount }) {
      Vue.set(
        state.order.find((coffee) => coffee.id === orderId),
        'amount',
        amount
      )
    },

    SET_COFFEE_ORDER (state, { orderId, coffeeId }) {
      const coffee = state.coffees.find((coffee) => coffee.node.id === coffeeId)
        .node
      Vue.set(
        state.order.find((coffee) => coffee.id === orderId),
        'coffee',
        coffee
      )
    },

    CLEAR_ORDER (state) {
      state.order = []
    },

    HAS_ORDERED (state) {
      state.hasOrder = true
    }
  },
  actions: {
    async getCoffees ({ commit, rootState }) {
      commit('START_LOADING', null, { root: true })
      try {
        const response = await apolloClient.query({ query: COFFEE_ALL })
        commit('SET_COFFEE', response.data.coffee.edges)
      } catch (e) {
        commit(
          'alert/ADD_ALERT',
          {
            header: false,
            body: `Une erreur est survenue, merci de réessayer : ${e}`,
            status: 'error',
            close: true
          },
          { root: true }
        )
      } finally {
        commit('END_LOADING', null, { root: true })
      }
    },

    async hasOrdered ({ commit, rootState }) {
      commit('START_LOADING', null, { root: true })
      try {
        const response = await apolloClient.query({
          query: ORDER_BY_USER_ID,
          variables: { userId: rootState.auth.currentUser.id }
        })
        if (response.data.coffeeOrder.edges.length !== 0) {
          commit('HAS_ORDERED')
          commit(
            'alert/ADD_ALERT',
            {
              header: true,
              headerContent: 'Vous avez déjà commandé !',
              body: 'Une commande à votre nom a été trouvé.',
              status: 'primary',
              close: true
            },
            { root: true }
          )
        }
      } catch (e) {
        commit(
          'alert/ADD_ALERT',
          {
            header: true,
            headerContent: 'Une erreur est survenue',
            body: 'Merci de réessayer, si vous rencontrez de nouveau cette erreur merci de me contacter.',
            status: 'danger',
            close: true
          },
          { root: true }
        )
      }
    },

    async saveOrder ({ state, commit }) {
      commit('START_LOADING', null, { root: true })
      try {
        const orders = state.order.map((coffeeOrdered) => ({
          sort: coffeeOrdered.type.id,
          weight: `A_${coffeeOrdered.weight}`,
          amount: coffeeOrdered.amount,
          coffee: coffeeOrdered.coffee.id
        }))

        await apolloClient.mutate({
          mutation: ADD_ORDER,
          variables: { amounts: orders }
        })

        commit(
          'alert/ADD_ALERT',
          {
            header: true,
            headerContent: 'Commande enregistrée !',
            body:
              'Votre commande a bien été enregistrée, un mail va vous être envoyé afin de confirmer votre commande !',
            status: 'success',
            close: true
          },
          { root: true }
        )
        commit('CLEAR_ORDER')
        commit('HAS_ORDERED')
      } catch (e) {
        commit(
          'alert/ADD_ALERT',
          {
            header: true,
            headerContent: 'Une erreur est survenue',
            body: `Merci de réessayer, si vous rencontrez de nouveau une erreur merci de me contacter, erreur : ${e}`,
            status: 'danger',
            close: true
          },
          { root: true }
        )
      } finally {
        commit('END_LOADING', null, { root: true })
      }
    }
  },
  getters: {
    orderById (state) {
      return (orderId) => state.order.find((order) => order.id === orderId)
    },
    valide (state) {
      let valide = true

      if (state.hasOrder) {
        return false
      }

      if (Object.keys(state.order).length !== 0) {
        state.order.forEach((coffeeOrdered) => {
          if (
            !coffeeOrdered.weight ||
            !coffeeOrdered.type ||
            coffeeOrdered.amount === '0'
          ) {
            valide = false
          }
        })
      }
      return valide
    },
    totalPrice (state) {
      let price = 0
      state.order.forEach((coffee) => {
        if (coffee.weight === '200') {
          price += coffee.coffee.twoHundredGramPrice * coffee.amount
        } else if (coffee.weight === '1000') {
          price += coffee.coffee.kilogramPrice * coffee.amount
        }
      })
      return Math.round(price * 100) / 100
    },
    uniqPrice (state, getters) {
      return (orderId) => {
        const order = getters.orderById(orderId)
        if (order.weight === '200') {
          return (
            Math.round(order.amount * order.coffee.twoHundredGramPrice * 100) /
            100
          )
        } else {
          return (
            Math.round(order.amount * order.coffee.kilogramPrice * 100) / 100
          )
        }
      }
    }
  }
}
