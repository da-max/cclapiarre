import { reactive, toRefs } from '@vue/composition-api'

export default function () {
  const state = reactive({
    results: []
  })

  const resultsUpdated = (newResult) => {
    state.results = newResult
  }

  return {
    ...toRefs(state),
    resultsUpdated
  }
}
