import apolloClient from '@/vue-apollo'

import APPLICATION_ALL from '@/graphql/Application/ApplicationAll.gql'
import APPLICATION_BY_SLUG from '@/graphql/Application/ApplicationBySlug.gql'
import APPLICATION_UPDATE from '@/graphql/Application/ApplicationUpdate.gql'
import PRODUCT_UPDATE from '@/graphql/Application/Product/ProductUpdate.gql'
import PRODUCT_ADD from '@/graphql/Application/Product/ProductAdd.gql'

export default {
  namespaced: true,
  state: () => ({
    applications: [],
    currentApplication: []
  }),

  mutations: {
    SET_APPLICATIONS (state, applications) {
      state.applications = applications
    },
    SET_CURRENT_APPLICATION (state, application) {
      state.currentApplication = application
    },
    CHANGE_DESCRIPTION (state, newDescription) {
      state.currentApplication = { ...state.currentApplication, newDescription }
    },
    SET_PRODUCT (state, newProduct) {
      const products = [...state.currentApplication.products.edges]
      const productIndex = state.currentApplication.products.edges.findIndex(
        (product) => product.node.id === newProduct.id
      )
      if (productIndex !== -1) {
        const oldProduct = state.currentApplication.products.edges[productIndex]

        products[productIndex] = { ...oldProduct, node: { ...newProduct } }
      } else {
        const product = { node: newProduct }
        products.push(product)
      }

      state.currentApplication = {
        ...state.currentApplication,
        products: {
          ...state.currentApplication.products,
          edges: products
        }
      }
    }
  },

  actions: {
    async getApplications ({ commit }) {
      commit('START_LOADING', null, { root: true })
      try {
        const response = await apolloClient.query({ query: APPLICATION_ALL })
        commit('SET_APPLICATIONS', response.data.allApplications)
      } catch (e) {
        commit('alert/ADD_UNKNOWN', null, { root: true })
      } finally {
        commit('END_LOADING', null, { root: true })
      }
    },
    async getCurrentApplication ({ commit }, applicationSlug) {
      commit('START_LOADING', null, { root: true })
      try {
        const response = await apolloClient.query({
          query: APPLICATION_BY_SLUG,
          variables: { slug: applicationSlug }
        })
        commit('SET_CURRENT_APPLICATION', response.data.applicationBySlug)
      } catch (e) {
        commit('alert/ADD_UNKNOWN', null, { root: true })
      } finally {
        commit('END_LOADING', null, { root: true })
      }
    },

    async saveApplication ({ state, commit }) {
      commit('START_LOADING', null, { root: true })
      try {
        const response = await apolloClient.mutate({
          mutation: APPLICATION_UPDATE,
          variables: {
            id: state.currentApplication.id,
            name: state.currentApplication.name,
            description: state.currentApplication.newDescription
              ? state.currentApplication.newDescription
              : state.currentApplication.description
          }
        })
        commit(
          'SET_CURRENT_APPLICATION',
          response.data.updateApplication.application
        )
      } catch (e) {
        commit('alert/ADD_UNKNOWN', null, { root: true })
      } finally {
        commit('END_LOADING', null, { root: true })
      }
    },
    async saveProduct ({ state, commit }, { product, update }) {
      commit('START_LOADING', null, { root: true })
      console.log(product)
      if (
        !product.name ||
        product.weights.length === 0 ||
        product.maximum <= 0 ||
        product.maximumAll <= 1
      ) {
        commit('alert/ADD_ALERT', {
          header: false,
          body:
            'Un des champs nécessaire n’a pas été rempli, merci de vérifier que tous les champs obligatoires ont bien été remplis, puis réessayer.',
          status: 'warning',
          close: true
        }, { root: true })
      } else {
        try {
          const response = await apolloClient.mutate({
            mutation: update ? PRODUCT_UPDATE : PRODUCT_ADD,
            variables: { ...product }
          })
          commit(
            'SET_PRODUCT',
            update
              ? response.data.updateProduct.product
              : response.data.addProduct.product
          )
          commit(
            'alert/ADD_ALERT',
            {
              header: false,
              body: `Le produit a bien été ${update ? 'modifié' : 'ajouté'} !`,
              status: 'success',
              close: true
            },
            { root: true }
          )
        } catch (e) {
          commit('alert/ADD_UNKNOWN', null, { root: true })
        }
      }
      commit('END_LOADING', null, { root: true })
    }
  },
  getters: {
    applicationBySlug (state) {
      return (slug) =>
        state.applications.find((application) => application.slug === slug)
    },
    idApplicationBySlug (_state, getters) {
      return (slug) => getters.applicationBySlug(slug).id
    },
    isAdmin (_state, getters, rootState) {
      return (slug) =>
        !!getters
          .applicationBySlug(slug)
          .admins.edges.find((admin) => admin.node.id === rootState.auth.currentUser.id)
    },
    products (state) {
      return state.currentApplication.products
        ? state.currentApplication.products.edges
        : []
    },
    applicationImage (state) {
      return state.currentApplication.images
        ? state.currentApplication.images
        : []
    }
  }
}
