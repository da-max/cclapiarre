import { reactive, toRefs } from '@vue/composition-api'
import { useMutation, useResult } from '@vue/apollo-composable'

import { useUtilsQuery } from '@/composition/useUtils'
import { useUtilsMutation } from './useUtils'
import store from '@/store/index'

import ApplicationUpdate from '@/graphql/Application/ApplicationUpdate.gql'
import ApplicationBySlug from '@/graphql/Application/ApplicationBySlug.gql'

export default function () {
  const state = reactive({
    application: {},
    loading: false,
    error: null
  })

  const { mutate: applicationUpdate, onDone } = useMutation(ApplicationUpdate)

  onDone(result => {
    state.application = useResult(result)
    store.commit('alert/ADD_ALERT', {
      header: false,
      body: 'La description a bien été mise à jour.',
      status: 'success',
      close: true

    })
  })

  const updateApplication = (application) => {
    useUtilsMutation(applicationUpdate, application)
  }

  const getApplication = (filter) => {
    const { result, loading, error } = useUtilsQuery(ApplicationBySlug, filter)
    state.loading = loading
    state.error = error
    state.application = useResult(result)
  }

  return { ...toRefs(state), updateApplication, getApplication }
}
