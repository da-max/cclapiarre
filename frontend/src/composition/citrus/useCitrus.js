import { computed } from '@vue/composition-api'
import { useMutation } from '@vue/apollo-composable'

import store from '@/store/index'

import CITRUS_UPDATE from '@/graphql/Citrus/CitrusUpdate.gql'

export default function () {
  const citrus = computed(() => store.state.citrus.citrus)
  const searchCitrus = computed(() => store.state.citrus.searchCitrus)
  const citrusSelect = computed(() => store.state.citrus.citrusSelect)

  // Actions
  // ========

  const getCitrus = () => {
    store.dispatch('citrus/getCitrus')
  }

  const patchCitrus = (key, value) => {
    store.dispatch('citrus/patchCitrus', { key, value })
  }

  const deleteCitrus = (citrusId) => {
    store.dispatch('citrus/deleteCitrus', citrusId)
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

  const setCitrusSelect = (citrus) => {
    store.commit('citrus/SET_CITRUS_SELECT', citrus)
  }

  // Getters
  // ========

  const citrusById = (citrusId) =>
    store.getters['citrus/citrusById'](citrusId)

  const citrusChecked = computed(() => store.getters['citrus/citrusChecked'])

  // Mutations

  const { mutate: citrusUpdate, onDone: onDoneCitrusUpdate } = useMutation(CITRUS_UPDATE)

  onDoneCitrusUpdate(result => {
    store.commit('citrus/UPDATE_CITRUS', result.data.updateCitrusProduct.citrusProduct)
    store.commit('alert/ADD_ALERT', {
      header: false,
      body: `Le produit ${result.data.updateCitrusProduct.citrusProduct.name} a bien été mis à jour.`,
      status: 'success',
      close: true
    })
  })

  return {
    // Store state
    citrus,
    searchCitrus,
    citrusSelect,

    // Store mutations
    setSearchCitrus,
    setCheckCitrus,
    setCitrusSelect,
    checkAll,

    // Store actions
    patchCitrus,
    getCitrus,
    deleteCitrus,

    // Store getters
    citrusById,
    citrusChecked,

    // Mutations
    citrusUpdate
  }
}
