import Vue from 'vue'
import apolloClient from '@/vue-apollo'

import BATCH_CITRUS_ORDER_REMOVE from '@/graphql/Citrus/Order/BatchCitrusOrderRemove.gql'
import ORDER_ALL from '@/graphql/Citrus/Order/OrderAll.gql'
import ORDER_ADD from '@/graphql/Citrus/Order/OrderAdd.gql'

export default {
    namespaced: true,
    state: () => ({
        orders: [],
        currentOrder: [],
        sendMail: true,
        displayOrders: 0,
        hasOrder: false
    }),

    mutations: {
        ADD_ORDER (state, order) {
            state.orders = [...state.orders, order]
        },

        CLEAR_CURRENT_ORDER (state) {
            state.currentOrder = []
        },

        REMOVE_ORDERS (state, ordersId) {
            state.orders = state.orders.filter(
                order => ordersId.findIndex(
                    id => id === order.node.id) === -1)
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
        async deleteAllOrders ({ state, commit }) {
            commit('START_LOADING', null, { root: true })
            try {
                const ordersId = state.orders.map(order => order.node.id)
                const response = await apolloClient.mutate({
                    mutation: BATCH_CITRUS_ORDER_REMOVE,
                    variables: { ordersId }
                })
                commit('REMOVE_ORDERS', response.data.batchRemoveCitrusOrder.deletedIds)
                commit('alert/ADD_ALERT', {
                    header: true,
                    body: 'Toutes les commandes ont bien été supprimées.',
                    status: 'success',
                    close: true
                }, { root: true })
                commit('SET_HAS_ORDER', false)
            } catch (e) {
                commit('alert/ADD_ALERT', {
                    header: false,
                    body: `Une erreur est survenue, merci de réssayer : ${e}`,
                    status: 'danger',
                    close: true
                },
                { root: true })
            } finally {
                commit('END_LOADING', null, { root: true })
            }
        },

        async deleteOrders ({ commit, dispatch }, ordersId) {
            commit('START_LOADING', null, { root: true })
            try {
                const response = await apolloClient.mutate({
                    mutation: BATCH_CITRUS_ORDER_REMOVE,
                    variables: { ordersId }
                })
                commit('REMOVE_ORDERS', response.data.batchRemoveCitrusOrder.deletedIds)
                commit('alert/ADD_ALERT', {
                    header: true,
                    body: 'Les commandes ont bien été supprimées.',
                    status: 'success',
                    close: true
                }, { root: true })
                dispatch('searchHasOrder')
            } catch (e) {
                commit('alert/ADD_ALERT', {
                    header: false,
                    body: `Une erreur est survenue, merci de réssayer : ${e}`,
                    status: 'danger',
                    close: true
                },
                { root: true })
            } finally {
                commit('END_LOADING', null, { root: true })
            }
        },

        async getOrders ({ state, commit, dispatch }) {
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
                commit('SET_DISPLAY_ORDERS', true)
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

                commit('alert/ADD_ALERT', {
                    header: true,
                    headerContent: 'Commande enregistrée',
                    body: 'Votre commande a bien été enregistrée.',
                    status: 'success',
                    close: true
                },
                { root: true })

                commit('SET_HAS_ORDER', true)
                commit('ADD_ORDER', { node: { ...newOrder.data.addCitrusOrder.citrusOrder } })
                commit('CLEAR_CURRENT_ORDER')
                commit('SET_DISPLAY_ORDERS', 1)
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

        currentOrderPrice: (state, _getters, rootState, rootGetters) => {
            let price = 0
            if (state.hasOrder) {
                const currentOrder = state.orders.find(order => order.node.user.id === rootState.auth.currentUser.id)
                currentOrder.node.amounts.edges.forEach(amount => {
                    const citrus = rootGetters['citrus/citrusById'](
                        amount.node.product.id)
                    console.log(amount)
                    price += amount.node.amount * citrus
                        .node
                        .price
                })
            } else {
                state.currentOrder.forEach(order => {
                    const citrus = rootGetters['citrus/citrusById'](
                        order.citrusId)
                    price += order.amount * citrus
                        .node
                        .price
                })
            }
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
                    total += amount.node.amount * amount
                        .node
                        .product
                        .price
                })
            })
            if (!state.hasOrder) {
                total += getters.currentOrderPrice
            }
            return Math.round(total * 100) / 100
        }
    }
}
