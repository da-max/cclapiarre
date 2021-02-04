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
            const amountIndex = state.currentOrder.findIndex(order => order.citrusId === citrusId)

            if (amountIndex > -1) {
                Vue.set(
                    state.currentOrder[amountIndex],
                    'amount',
                    amount
                )
            } else {
                state.currentOrder.push({
                    citrusId,
                    amount
                })
            }
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
                const response = await apolloClient.query({ query: ORDER_ALL })
                commit('SET_ORDERS', response.data.citrusOrder.edges)
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
        amountsByCitrusId: (state) => {
            return (citrusId) => {
                const amounts = []

                state.orders.forEach(
                    order => {
                        const amount = order.node.amounts.edges.find(
                            amount => amount.node.product.id === citrusId)
                        if (amount) {
                            amounts.push(amount.node.amount)
                        }
                    })
                return amounts
            }
        },

        currentOrderPrice: (state, _getters, _rootState, rootGetters) => {
            let price = 0
            state.currentOrder.forEach(order => {
                const citrus = rootGetters['citrus/citrusById'](order.citrusId)
                price += order.amount * citrus.node.price / citrus.node.weight
            })
            return Math.round(price * 100) / 100
        },

        currentOrderValide: (state) => {
            let valide = false
            state.currentOrder.forEach(order => {
                if (order.amount > 0) {
                    valide = true
                }
            })
            return valide
        },

        totalCitrusById: (state, getters) => {
            return (citrusId) => {
                let total = 0

                const amounts = getters.amountsByCitrusId(citrusId)
                amounts.forEach(amount => {
                    total += amount
                })
                const currentAmount = state.currentOrder.find(order => order.citrusId === citrusId)
                if (currentAmount) {
                    total += currentAmount.amount
                }
                return Math.round(total * 100) / 100
            }
        },
        totalPrice: (state, getters) => {
            let total = 0
            state.orders.forEach(order => {
                order.node.amounts.edges.forEach(amount => {
                    total += amount.node.amount * amount.node.product.price
                })
            })
            total += getters.currentOrderPrice
            return Math.round(total * 100) / 100
        }
    }
}
