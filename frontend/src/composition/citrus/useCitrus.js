import { computed } from '@vue/composition-api'

import store from '@/store/index'

export default function () {
  const citrus = computed(() => store.state.citrus.citrus)
  const searchCitrus = computed(() => store.state.citrus.searchCitrus)

  // Actions
  // ========

  const getCitrus = () => {
    store.dispatch('citrus/getCitrus')
  }

  // Mutations
  // =========

  const setSearchCitrus = (result) => {
    store.commit('citrus/SET_SEARCH_CITRUS', result)
  }

  const checkAll = computed({
    get: () => false,
    set: (value) => {
      store.commit('citrus/CHECK_ALL', value)
    }
  })

  const setCheckCitrus = (citrus, value) => {
    store.commit('citrus/SET_CHECK_CITRUS', { citrus, value })
  }

  // Getters
  // ========

  const citrusById = (citrusId) =>
    store.getters['citrus/citrusById'](citrusId)

  return {
    getCitrus,
    citrusById,
    citrus,
    searchCitrus,
    setSearchCitrus,
    setCheckCitrus,
    checkAll
  }
}
