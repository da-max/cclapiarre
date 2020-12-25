import store from '@/store/index'
import { computed, reactive, toRefs } from '@vue/composition-api'
import { useMutation, useResult } from '@vue/apollo-composable'
import { useUtilsQuery } from '@/composition/useUtils'

import ORDER_ALL from '@/graphql/Coffee/Order/OrderAll.gql'
import ORDER_REMOVE from '@/graphql/Coffee/Order/OrderRemove.gql'

export default function () {
  // state
  const state = reactive({
    coffeeSelect: {}
  })

  // Computed
  const coffees = computed(() => store.state.coffee.coffees)
  const coffeesOrder = computed(() => store.state.coffee.order)
  const hasOrder = computed(() => store.state.coffee.hasOrder)
  const price = computed(() => store.getters['coffee/totalPrice'])
  const valide = computed(() => store.getters['coffee/valide'])

  const uniqPrice = (orderId) => store.getters['coffee/uniqPrice'](orderId)

  // Mutations

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

  const addCoffeeOrder = (coffee) => {
    // eslint-disable-next-line no-undef
    UIkit.scroll('#add-coffee-button', { offset: 100 }).scrollTo('#order-list')

    store.commit('coffee/ADD_COFFEE_ORDER', coffee)
  }

  const removeCoffeeOrder = (orderId) => {
    store.commit('coffee/REMOVE_COFFEE_ORDER', orderId)
  }

  // Actions

  const getCoffees = () => {
    store.dispatch('coffee/getCoffees')
  }

  const saveOrder = () => {
    store.dispatch('coffee/saveOrder')
  }

  const hasOrdered = () => {
    store.dispatch('coffee/hasOrdered')
  }

  // Methods

  const displayDetails = (coffee) => {
    state.coffeeSelect = coffee

    // eslint-disable-next-line no-undef
    UIkit.modal('#coffee-details').show()
  }

  const allOrder = () => {
    const { result, loading, refetch: refetchOrderAll } = useUtilsQuery(ORDER_ALL)
    const orders = useResult(result)

    return { orders, loading, refetchOrderAll }
  }

  const { mutate: orderRemove, onDone: onDoneRemoveOrder } = useMutation(ORDER_REMOVE)

  return {
    // State
    ...toRefs(state),

    // Store state or getter
    coffees,
    price,
    valide,
    hasOrder,
    coffeesOrder,
    uniqPrice,

    // Mutations
    addCoffeeOrder,
    setAmount,
    setType,
    setWeight,
    setCoffee,
    removeCoffeeOrder,

    // Actions
    getCoffees,
    saveOrder,
    hasOrdered,

    // Methods
    allOrder,
    displayDetails,
    orderRemove,
    onDoneRemoveOrder
  }
}
