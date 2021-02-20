import Vue from 'vue'
import apolloClient from '@/vue-apollo'

import ORDER_ALL from '@/graphql/Citrus/Order/OrderAll.gql'
import ORDER_ADD from '@/graphql/Citrus/Order/OrderAdd.gql'

export default {
    namespaced: true,
    state: () => ({
        orders: [],
        currentOrder: [],
        sendMail: true,
        displayOrders: false,
        hasOrder: false
    }),

    mutations: {
        ADD_ORDERS (state, orders) {
            state.orders = { ...state.orders, orders }
        },

        SET_CURRENT_ORDER_AMOUNT (state, { citrusId, amount }) {
            const amountIndex = state.currentOrder.findIndex(order => order.citrusId === citrusId)

            if (amountIndex > -1) {
                if (amount <= 0) {
                    state.currentOrder.splice(amountIndex, 1)
                } else {
                    Vue.set(
                        state.currentOrder[amountIndex],
                        'amount',
                        amount
                    )
                }
            } else {
                state.currentOrder.push({
                    citrusId,
                    amount
                })
            }
        },

        SET_DISPLAY_ORDERS (state, value) {
            state.displayOrders = value
        },

        SET_ORDERS (state, orders) {
            state.orders = orders
        },

        SET_ORDER_AMOUNT (state, { orderId, citrusId, amount }) {
            const orderIndex = state.orders.findIndex(
                o => o.node.id === orderId
            )
            const citrusIndex = state.orders[orderIndex]
                .amounts
                .edges
                .findIndex(
                    amount => amount.node.product.id === citrusId
                )
            Vue.set(
                state.orders[orderIndex]
                    .amounts
                    .edges[citrusIndex]
                    .node,
                'amount',
                amount
            )
        },

        SET_HAS_ORDER (state, value) {
            state.hasOrder = value
        },

        SET_SEND_MAIL (state, value) {
            state.sendMail = value
        }
    },

    actions: {
        async getOrders ({ state, commit, dispatch }, force = false) {
            commit('START_LOADING', null, { root: true })
            try {
                const response = await apolloClient.query({ query: ORDER_ALL })
                commit('SET_ORDERS', response.data.citrusOrder.edges)
                dispatch('searchHasOrder')
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

        searchHasOrder ({ state, commit, rootState }) {
            let hasOrder = false
            if (state.orders.find(order => order.node.user.id === rootState.auth.currentUser.id)) {
                hasOrder = true
            }
            commit('SET_HAS_ORDER', hasOrder)
        },

        async saveOrder ({ commit, state }) {
            commit('START_LOADING', null, { root: true })
            try {
                const order = state.currentOrder.map(
                    o => ({
                        amount: o.amount,
                        product: o.citrusId
                    }))
                const newOrder = await apolloClient.mutate({
                    mutation: ORDER_ADD,
                    variables: {
                        sendMail: state.sendMail,
                        amounts: order
                    }
                })

                console.log(newOrder)

                commit('alert/ADD_ALERT', {
                    header: true,
                    headerContent: 'Commande enregistrée',
                    body: 'Votre commande a bien été enregistrée.',
                    status: 'success',
                    close: true
                },
                { root: true })

                commit('SET_HAS_ORDER', true)
                commit('ADD_ORDERS', newOrder)
            } catch (e) {
                commit('alert/ADD_ALERT', {
                    header: false,
                    body: `Une erreur est survenue, merci de réessayer : ${e}`,
                    close: true,
                    status: 'danger'
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

        currentAmountByCitrusId: (state) => {
            return (citrusId) => {
                let amount = state
                    .currentOrder
                    .find(order => order.citrusId === citrusId)
                if (amount) {
                    amount = amount.amount
                } else {
                    amount = 0
                }
                return amount
            }
        },

        currentOrderPrice: (state, _getters, _rootState, rootGetters) => {
            let price = 0
            state.currentOrder.forEach(order => {
                const citrus = rootGetters['citrus/citrusById'](
                    order.citrusId)
                price += order.amount * citrus
                    .node
                    .price / citrus.node.weight
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
                const currentAmount = state.currentOrder.find(
                    order => order.citrusId === citrusId
                )
                if (currentAmount) {
                    total += currentAmount.amount
                }
                return Math.round(total * 100) / 100
            }
        },

        totalPriceByOrderId: (state) => {
            return (orderId) => {
                let total = 0
                const order = state.orders.find(order => order.node.id === orderId)
                if (order) {
                    order.node.amounts.edges.forEach(amount => {
                        total += amount.node.amount * amount.node.product.price
                    })
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
