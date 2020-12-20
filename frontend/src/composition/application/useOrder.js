import store from '@/store/index'

export default function () {
  const addProductOrder = (product) => {
    // eslint-disable-next-line no-undef
    UIkit.scroll('#addProductButton', { offset: 100 }).scrollTo('#order-list')

    store.commit('order/ADD_PRODUCT_ORDER', product)
  }

  return { addProductOrder }
}
