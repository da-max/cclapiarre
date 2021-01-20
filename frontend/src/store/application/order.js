import Vue from 'vue'

import apolloClient from '@/vue-apollo'

import ADD_ORDER from '@/graphql/Application/Order/OrderAdd.gql'

export default {
    namespaced: true,
    state: () => ({
        order: [],
        productOrderedId: 0,
        price: 0
    }),

    mutations: {
        ADD_PRODUCT_ORDER (state, product) {
            state.order.push({
                id: state.productOrderedId,
                product,
                weight: product.weights.edges[0],
                amount: 1
            })

            state.productOrderedId++
        },
        REMOVE_PRODUCT_ORDER (state, productId) {
            state.order = state.order.filter((product) => product.id !== productId)
        },
        CLEAR_ORDER (state) {
            state.order = []
        },
        SET_WEIGHT (state, { id, weight }) {
            Vue.set(
                state.order.find((productOrdered) => productOrdered.id === id),
                'weight',
                weight
            )
        },
        SET_OPTION (state, { id, option }) {
            Vue.set(
                state.order.find((productOrdered) => productOrdered.id === id),
                'option',
                option
            )
        },
        SET_AMOUNT (state, { id, amount }) {
            Vue.set(
                state.order.find((productOrdered) => productOrdered.id === id),
                'amount',
                parseInt(amount)
            )
        }
    },

    actions: {
        async saveOrder ({ state, commit }, applicationId) {
            commit('START_LOADING', null, { root: true })
            try {
                const orders = state.order.map((productOrdered) => ({
                    option: productOrdered.option ? productOrdered.option.node.id : null,
                    weight: productOrdered.weight.node.id,
                    amount: parseInt(productOrdered.amount),
                    product: productOrdered.product.id
                }))
                await apolloClient.mutate({
                    mutation: ADD_ORDER,
                    variables: {
                        application: parseInt(applicationId),
                        amounts: orders
                    }
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
            } catch (error) {
                commit(
                    'alert/ADD_ALERT',
                    { header: false, body: error, status: 'danger', close: true },
                    { root: true }
                )
            } finally {
                commit('END_LOADING', null, { root: true })
            }
        }
    },

    getters: {
        productById: (state) => {
            return (productOrderedId) =>
                state.order.find((product) => product.id === productOrderedId)
        },
        valide (state) {
            let valide = true
            state.order.forEach((productOrdered) => {
                if (
                    (productOrdered.product.options.edges.length !== 0 &&
            productOrdered.option === undefined) ||
          productOrdered.amount === 0
                ) {
                    valide = false
                }
            })
            return valide
        },
        totalPrice (state) {
            let price = 0
            state.order.forEach((productOrdered) => {
                if (productOrdered.weight && productOrdered.amount) {
                    price += productOrdered.weight.node.price * productOrdered.amount
                }
            })
            return Math.round(price * 100) / 100
        },
        uniqPrice: (_state, getters) => {
            return (productId) => {
                const product = getters.productById(productId)
                if (product.weight && product.amount) {
                    return (
                        Math.round(product.weight.node.price * product.amount * 100) / 100
                    )
                } else {
                    return 0
                }
            }
        }
    }
}
