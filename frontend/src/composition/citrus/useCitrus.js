import { computed } from '@vue/composition-api'

import store from '@/store/index'

export default function () {
  const citrus = computed(() => store.state.citrus.citrus)
  const searchCitrus = computed(() => store.state.citrus.searchCitrus)
  const citrusUpdate = computed(() => store.state.citrus.citrusUpdate)

  // Actions
  // ========

  const getCitrus = () => {
    store.dispatch('citrus/getCitrus')
  }

  const patchCitrus = (key, value) => {
    store.dispatch('citrus/patchCitrus', { key, value })
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

  const setCitrusUpdate = (citrus) => {
    store.commit('citrus/SET_CITRUS_UPDATE', citrus)
  }

  // Getters
  // ========

  const citrusById = (citrusId) =>
    store.getters['citrus/citrusById'](citrusId)

  const citrusChecked = computed(() => store.getters['citrus/citrusChecked'])

  return {
    getCitrus,
    patchCitrus,
    citrusById,
    citrusChecked,
    citrus,
    searchCitrus,
    citrusUpdate,
    setSearchCitrus,
    setCheckCitrus,
    setCitrusUpdate,
    checkAll
  }
}
