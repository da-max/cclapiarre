export default {
  namespaced: true,
  state: () => ({
    order: [],
    orderId: 0,
    price: 0,
    validate: true
  }),

  mutations: {
    ADD_PRODUCT_ORDER (state, product) {
      state.validate = false
      const id = state.orderId
      state.orderId++
      if (product.weights.edges.length === 1) {
        const weight = product.weights.edges[0]
        state.order.push({ id, product, weight })
      } else state.order.push({ id, product })
    },
    REMOVE_PRODUCT_ORDER (state, productId) {
      state.order = state.order.filter(product => product.id !== productId)
    }
  }
}
