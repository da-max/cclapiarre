import { reactive, toRefs } from '@vue/composition-api'

export default function useProduct () {
  const state = reactive({
    product: {}
  })

  return { ...toRefs(state) }
}
