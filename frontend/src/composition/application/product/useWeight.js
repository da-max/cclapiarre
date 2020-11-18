import { reactive, ref, toRefs } from '@vue/composition-api'
import { useMutation, useResult } from '@vue/apollo-composable'

import { useUtilsQuery } from '@/composition/useUtils'

import WeightByAppliciationSlug from '@/graphql/Application/Product/Weight/WeightByApplicationSlug.gql'
import WeightAdd from '@/graphql/Application/Product/Weight/WeightAdd.gql'

export default function useWeight () {
  // Data
  // ========
  const state = reactive({
    weights: {},
    error: null,
    loading: false
  })

  // Methods
  // ========

  const getWeightByApplicationSlug = function (filter) {
    const { result, loading } = useUtilsQuery(WeightByAppliciationSlug, filter)
    state.weights = useResult(result)
    state.loading = loading
  }

  const { mutate: weightAdd, onDone } = useMutation(WeightAdd)

  onDone((result) => {
    // eslint-disable-next-line no-undef
    UIkit.notification({
      message: 'Poids ajoutée',
      status: 'success',
      pos: 'top-center',
      timeout: 5000
    })

    state.weights = ref({
      edges: [
        ...state.weights.edges, {
          node: result.data.addWeight.weight
        }
      ]
    })
  })

  return { ...toRefs(state), getWeightByApplicationSlug, weightAdd }
}
