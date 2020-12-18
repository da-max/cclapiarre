import store from '@/store/index'
import { computed } from '@vue/composition-api'

export default function () {
  const getCoffees = () => {
    store.dispatch('coffee/getCoffees')
  }

  const coffees = computed(() => store.state.coffee.coffees)

  return {
    getCoffees,
    coffees
  }
}
