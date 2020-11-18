import { useMutation } from '@vue/apollo-composable'
import { reactive, toRefs } from '@vue/composition-api'

import store from '@/store/index'

import ProductAdd from '@/graphql/Application/Product/ProductUpdate.gql'

export default function useProduct () {
  const state = reactive({
    productUpdated: {}
  })

  const { mutate: productUpdate, onDone } = useMutation(ProductAdd)

  onDone((_result) => {
    store.commit('alert/ADD_ALERT', {
      header: false,
      body: 'Le produit a bien été mis à jour.',
      status: 'success',
      close: true
    })
  })

  return { ...toRefs(state), productUpdate }
}
