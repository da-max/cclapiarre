import Vue from 'vue'
import apolloClient from '@/vue-apollo'

import ORDER_ALL from '@/graphql/Citrus/Order/OrderAll.gql'

export default {
    namespaced: true,
    state: () => ({
        orders: [],
        currentOrder: []
    }),

    mutations: {
        SET_ORDERS (state, orders) {
            state.orders = orders
        },

        SET_CURRENT_ORDER_AMOUNT (state, { citrusId, amount }) {
            const citrusIndex = state.currentOrder.findIndex(c => c.node.id === citrusId)
            Vue.set(
                state.currentOrder[citrusIndex],
                'amount',
                amount
            )
        },

        SET_ORDER_AMOUNT (state, { orderId, citrusId, amount }) {
            const orderIndex = state.orders.findIndex(o => o.node.id === orderId)
            const citrusIndex = state.orders[orderIndex]
                .amounts
                .edges
                .findIndex(
                    amount => amount.node.product.id === citrusId
                )
            Vue.set(
                state.orders[orderIndex].amounts.edges[citrusIndex].node,
                'amount',
                amount
            )
        }
    },

    actions: {
        async getOrders ({ commit }) {
            commit('START_LOADING', null, { root: true })
            try {
                const response = apolloClient.query({ query: ORDER_ALL })
                commit('SER_ORDERS', response.data.citrusOrders.edges)
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
