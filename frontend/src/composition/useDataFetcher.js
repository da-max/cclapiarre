import store from '@/store/index'
import { apolloClient } from '@/vue-apollo'
import { reactive, onMounted, toRefs } from '@vue/composition-api'

export function useDataFetcher (query) {
  const state = reactive({
    error: null,
    data: {}
  })

  onMounted(async () => {
    store.commit('START_LOADING')
    try {
      state.data = await apolloClient.query(query)
    } catch (error) {
      state.error = error
    }

    store.commit('END_LOADING')
  })

  return { ...toRefs(state) }
}
