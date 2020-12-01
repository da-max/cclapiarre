import { onMounted } from '@vue/composition-api'

import store from '@/store/index'
import { useQuery } from '@vue/apollo-composable'

export function useSetupTitle (title = '') {
  onMounted(() => {
    document.title = `${title} | CC La Piarre`
  })
}

export function useUtilsQuery (query, variables = {}) {
  store.commit('START_LOADING')
  try {
    const { result, loading, error } = useQuery(query, variables)
    return { result, loading, error }
  } catch (e) {
    store.commit('alert/ADD_UNKNOWN')
  } finally {
    store.commit('END_LOADING')
  }
}

export function useUtilsMutation (mutation, variables) {
  store.commit('START_LOADING')
  try {
    mutation(variables)
  } catch (error) {
    store.commit('alert/ADD_UNKNOWN')
  } finally {
    store.commit('END_LOADING')
  }
}
