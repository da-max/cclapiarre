import store from '@/store/index'
import { computed } from '@vue/composition-api'

export default function () {
  const coffees = computed(() => store.state.coffee.coffees)
  const coffeesOrder = computed(() => store.state.coffee.order)
  const price = computed(() => store.getters['coffee/totalPrice'])

  const setAmount = (orderId, amount) => {
    store.commit('coffee/SET_COFFEE_ORDER_AMOUNT', { orderId, amount })
  }

  const setType = (orderId, type) => {
    store.commit('coffee/SET_COFFEE_ORDER_TYPE', { orderId, type })
  }

  const setWeight = (orderId, weight) => {
    store.commit('coffee/SET_COFFEE_ORDER_WEIGHT', { orderId, weight })
  }

  const setCoffee = (orderId, coffee) => {
    store.commit('coffee/SET_COFFEE_ORDER', { orderId, coffeeId: coffee })
  }

  const getCoffees = () => {
    store.dispatch('coffee/getCoffees')
  }

  const addCoffeeOrder = (coffee) => {
    // eslint-disable-next-line no-undef
    UIkit.scroll('#add-coffee-button', { offset: 100 }).scrollTo('#order-list')

    store.commit('coffee/ADD_COFFEE_ORDER', coffee)
  }

  const removeCoffeeOrder = (orderId) => {
    store.commit('coffee/REMOVE_COFFEE_ORDER', orderId)
  }

  return {
    addCoffeeOrder,
    getCoffees,
    coffees,
    coffeesOrder,
    setAmount,
    setType,
    setWeight,
    setCoffee,
    removeCoffeeOrder,
    price
  }
}
