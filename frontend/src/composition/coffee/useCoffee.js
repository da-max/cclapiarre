import store from '@/store/index'
import { computed } from '@vue/composition-api'

export default function () {
  const coffees = computed(() => store.state.coffee.coffees)
  const coffeesOrder = computed(() => store.state.coffee.order)

  const getCoffees = () => {
    store.dispatch('coffee/getCoffees')
  }

  const addCoffeeOrder = (coffee) => {
    store.commit('coffee/ADD_COFFEE_ORDER', coffee)
  }
  return {
    addCoffeeOrder,
    getCoffees,
    coffees,
    coffeesOrder
  }
}
