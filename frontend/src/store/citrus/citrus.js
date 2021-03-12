import Vue from 'vue'
import apolloClient from '@/vue-apollo'

import CITRUS_ALL from '@/graphql/Citrus/CitrusAll.gql'
import BATCH_CITRUS_PATCH from '@/graphql/Citrus/BatchCitrusPatch.gql'
import CITRUS_DELETE from '@/graphql/Citrus/CitrusDelete.gql'

export default {
    namespaced: true,
    state: () => ({
        citrus: [],
        searchCitrus: [],
        citrusSelect: {}
    }),

    mutations: {
        ADD_CITRUS (state, value) {
            state.citrus = [...state.citrus, { node: { ...value } }]
        },

        CHECK_ALL (state, value) {
            state.searchCitrus.forEach((citrus) => {
                Vue.set(
                    citrus,
                    'check',
                    value
                )
            })
        },

        CLEAR_SELECT_CITRUS (state) {
            state.citrusSelect = {}
        },

        DELETE_CITRUS (state, citrusId) {
            state.citrus = state.citrus.filter(citrus => citrus.node.id !== citrusId)
        },

        SET_CHECK_CITRUS (state, { citrus, value }) {
            const product = state.citrus.find((c) => c.node.id === citrus.node.id)
            Vue.set(
                product,
                'check',
                value
            )
        },

        SET_CITRUS_SELECT (state, value) {
            state.citrusSelect = value
        },

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

        UPDATE_CITRUS (state, citrusUpdate) {
            const citrusIndex = state.citrus.findIndex(c => c.node.id === citrusUpdate.id)
            Vue.set(
                state.citrus[citrusIndex],
                'node',
                citrusUpdate
            )
        }
    },

    actions: {
        async getCitrus ({ state, commit }, force = false) {
            if (state.citrus.length !== 0 && !force) {
                return
            }
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

        async patchCitrus ({ commit, getters }, { key, value, type }) {
            commit('START_LOADING', null, { root: true })
            try {
                let variables
                if (type === 'percent') {
                    variables = getters.citrusChecked.map(citrus => {
                        const c = { id: citrus.node.id }
                        c[key] = citrus.node[key] + (citrus.node[key] * value) / 100
                        return c
                    })
                } else {
                    variables = getters.citrusChecked.map(citrus => {
                        const c = { id: citrus.node.id }
                        c[key] = value
                        return c
                    })
                }
                const response = await apolloClient.mutate({
                    mutation: BATCH_CITRUS_PATCH,
                    variables: { citrus: variables }
                })
                response.data.batchPatchCitrusProduct
                    .citrusProducts
                    .forEach(citrus => {
                        commit('UPDATE_CITRUS', citrus)
                    })
                commit(
                    'alert/ADD_ALERT',
                    {
                        header: false,
                        body:
              'Les produits sélectionnés ont bien été modifié.',
                        status: 'success',
                        close: true
                    },
                    { root: true }
                )
                commit('CHECK_ALL', false)
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

        async deleteCitrus ({ commit }, citrusId) {
            commit('START_LOADING', null, { root: true })
            try {
                const response = await apolloClient.mutate({ mutation: CITRUS_DELETE, variables: { id: citrusId } })
                if (!response.data.deleteCitrusProduct.found) {
                    throw new Error('Product not found')
                }
                commit('DELETE_CITRUS', citrusId)
                commit('alert/ADD_ALERT', {
                    header: false,
                    body: 'Le produit a bien été supprimé.',
                    status: 'success',
                    close: true
                }, { root: true })
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

        citrusChecked: (state) => state.citrus.filter(c => c.check),

        citrusDisplay: (state) => state.citrus.filter(c => c.node.display)

    }
}
