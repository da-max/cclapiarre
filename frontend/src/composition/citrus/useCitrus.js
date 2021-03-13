import { computed } from '@vue/composition-api'
import { useMutation } from '@vue/apollo-composable'

import store from '@/store/index'

import CITRUS_ADD from '@/graphql/Citrus/CitrusAdd.gql'
import CITRUS_UPDATE from '@/graphql/Citrus/CitrusUpdate.gql'

export default function () {
    // Store state
    // ===========

    const citrus = computed(() => store.state.citrus.citrus)
    const citrusSelect = computed(() => store.state.citrus.citrusSelect)
    const searchCitrus = computed(() => store.state.citrus.searchCitrus)

    // Store actions
    // =============

    const deleteCitrus = (citrusId) => {
        store.dispatch('citrus/deleteCitrus', citrusId)
    }

    const getCitrus = () => {
        store.dispatch('citrus/getCitrus')
    }

    const patchCitrus = (actions) => {
        store.dispatch('citrus/patchCitrus', { type: null, ...actions })
    }

    // Store mutations
    // ===============

    const clearSelectCitrus = () => {
        store.commit('citrus/CLEAR_SELECT_CITRUS')
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

    const setCitrusAmount = (citrusId, amount) => {
        store.commit('citrus/SET_CITRUS_AMOUNT', { citrusId, amount: Number(amount) })
    }

    const setCitrusSelect = (citrus) => {
        store.commit('citrus/SET_CITRUS_SELECT', citrus)
    }

    const setSearchCitrus = (result) => {
        store.commit('citrus/SET_SEARCH_CITRUS', result)
    }

    // Store getters
    // =============

    const citrusById = (citrusId) => store.getters['citrus/citrusById'](citrusId)

    const citrusChecked = computed(() => store.getters['citrus/citrusChecked'])

    const citrusDisplay = computed(() => store.getters['citrus/citrusDisplay'])

    // GraphQl Mutations
    // =================

    const { mutate: citrusUpdate, onDone: onDoneCitrusUpdate } = useMutation(CITRUS_UPDATE)

    onDoneCitrusUpdate(result => {
        store.commit('citrus/UPDATE_CITRUS', result.data.updateCitrusProduct.citrusProduct)
        store.commit('alert/ADD_ALERT', {
            header: false,
            body: `Le produit « ${result.data.updateCitrusProduct.citrusProduct.name} » a bien été mis à jour.`,
            status: 'success',
            close: true
        })
    })

    const { mutate: citrusAdd, onDone: onDoneCitrusAdd } = useMutation(CITRUS_ADD)

    onDoneCitrusAdd(result => {
        store.commit('citrus/ADD_CITRUS', result.data.addCitrusProduct.citrusProduct)
        store.commit('alert/ADD_ALERT', {
            header: false,
            body: `Le produit « ${result.data.addCitrusProduct.citrusProduct.name} » a bien été créé.`,
            status: 'success',
            close: true
        })
    })

    return {
    // Store state
        citrus,
        citrusSelect,
        searchCitrus,

        // Store mutations
        checkAll,
        setCheckCitrus,
        setCitrusAmount,
        setCitrusSelect,
        setSearchCitrus,

        // Store actions
        clearSelectCitrus,
        deleteCitrus,
        getCitrus,
        patchCitrus,

        // Store getters
        citrusById,
        citrusChecked,
        citrusDisplay,

        // GraphQl mutations
        citrusAdd,
        citrusUpdate
    }
}
