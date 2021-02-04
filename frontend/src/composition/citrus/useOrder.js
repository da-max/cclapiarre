import { computed } from '@vue/composition-api'

import store from '@/store/index'

export default function () {
    // Store state
    // ===========
    const orders = computed(() => store.state.citrusOrder.orders)
    const currentOrder = computed(() => store.state.citrusOrder.currentOrder)

    // Store mutations
    // ===============

    const setCurrentOrderAmount = (citrusId, amount = 0) => {
        store.commit('citrusOrder/SET_CURRENT_ORDER_AMOUNT', { citrusId, amount: Number(amount) })
    }

    // Store actions
    // =============
    const getOrders = () => store.dispatch('citrusOrder/getOrders')

    // Store getters
    // =============
    const currentOrderPrice = computed(() => store.getters['citrusOrder/currentOrderPrice'])
    const currentOrderValide = computed(() => store.getters['citrusOrder/currentOrderValide'])
    const totalPrice = computed(() => store.getters['citrusOrder/totalPrice'])
    const totalCitrusById = (citrusId) => store.getters['citrusOrder/totalCitrusById'](citrusId)

    return {
        // Store state
        orders,
        currentOrder,

        // Store mutations
        setCurrentOrderAmount,

        // Store actions
        getOrders,

        // Store getters
        currentOrderPrice,
        currentOrderValide,
        totalCitrusById,
        totalPrice
    }
}
