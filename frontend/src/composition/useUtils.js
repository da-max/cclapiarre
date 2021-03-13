import { onMounted } from '@vue/composition-api'

import store from '@/store/index'
import { useQuery } from '@vue/apollo-composable'

export function useSetupTitle (title = '') {
    onMounted(() => {
        document.title = `${title} | CC La Piarre`
    })
}

export function useShowModal (modalId) {
    // eslint-disable-next-line no-undef
    UIkit.modal(modalId).show()
}

export function useHideModal (modalId) {
    // eslint-disable-next-line no-undef
    UIkit.modal(modalId).hide()
}

export function useUtilsQuery (query, variables = {}) {
    store.commit('START_LOADING')
    try {
        const { result, loading, error, refetch } = useQuery(query, variables)
        return { result, loading, error, refetch }
    } catch (e) {
        store.commit('alert/ADD_UNKNOWN')
    } finally {
        store.commit('END_LOADING')
    }
}

export async function useUtilsMutation (mutation, variables) {
    store.commit('START_LOADING')
    try {
        await mutation(variables)
    } catch (error) {
        store.commit('alert/ADD_UNKNOWN')
    } finally {
        store.commit('END_LOADING')
    }
}
