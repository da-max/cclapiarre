import Vue from 'vue'

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
      state.order = state.order.filter(product => product.id !== productId)
    },
    SET_WEIGHT (state, { id, weight }) {
      Vue.set(state.order.find(productOrdered => productOrdered.id === id), 'weight', weight)
    },
    SET_OPTION (state, { id, option }) {
      Vue.set(state.order.find(productOrdered => productOrdered.id === id), 'option', option)
    },
    SET_AMOUNT (state, { id, amount }) {
      Vue.set(state.order.find(productOrdered => productOrdered.id === id), 'amount', parseInt(amount))
    }
  },
  getters: {
    productById: (state) => { return (productOrderedId) => state.order.find(product => product.id === productOrderedId) },
    valide (state) {
      let valide = true
      state.order.forEach(productOrdered => {
        if ((productOrdered.product.options.edges.length !== 0 && productOrdered.option === undefined) || productOrdered.amount === 0) {
          valide = false
        }
      })
      return valide
    }
  }
}
