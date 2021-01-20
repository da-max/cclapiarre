import { reactive, toRefs, ref } from '@vue/composition-api'
import { useMutation, useResult } from '@vue/apollo-composable'

import { useUtilsQuery } from '@/composition/useUtils'

import OptionByApplicationSlug from '@/graphql/Application/Product/Option/OptionByApplicationSlug.gql'
import OptionAdd from '@/graphql/Application/Product/Option/OptionAdd.gql'

export default function useOption () {
    // Data
    // ============
    const state = reactive({
        options: {},
        error: null,
        loading: false,
        newOption: ''
    })

    // Methods
    // ===========
    const getOptionsByApplicationSlug = (filter) => {
        const { result, loading } = useUtilsQuery(OptionByApplicationSlug, filter)
        state.options = useResult(result)
        state.loading = loading
    }

    const { mutate: optionAdd, onDone } = useMutation(OptionAdd)

    onDone((result) => {
    // eslint-disable-next-line no-undef
        UIkit.notification({
            message: 'Option ajoutée',
            status: 'success',
            pos: 'top-center',
            timout: 5000
        })
        state.options = ref({
            edges: [
                ...state.options.edges, {
                    node: result.data.addOption.option
                }
            ]
        })
    })

    return { ...toRefs(state), getOptionsByApplicationSlug, optionAdd }
}
