import { computed } from '@vue/composition-api'

import store from '@/store/index'

export default function () {
    // Store state
    // ===========
    const orders = computed(() => store.state.citrusOrder.orders)
    const currentOrder = computed(() => store.state.citrusOrder.currentOrder)
    const displayOrders = computed(() => store.state.citrusOrder.displayOrders)

    // Store mutations
    // ===============

    const setCurrentOrderAmount = (citrusId, amount = 0) => {
        store.commit('citrusOrder/SET_CURRENT_ORDER_AMOUNT', { citrusId, amount: Number(amount) })
    }

    const setDisplayOrders = (value) => {
        console.log(value)
        store.commit('citrusOrder/SET_DISPLAY_ORDERS', value)
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

    // Methods
    // =======

    const orderAmountByCitrusId = (order, citrusId) => {
        let amount = order.amounts.edges.find(a => a.node.product.id === citrusId)
        if (!amount) {
            amount = 0
        } else {
            amount = amount.node.amount
        }
        return amount
    }

    return {
        // Store state
        orders,
        currentOrder,
        displayOrders,

        // Store mutations
        setCurrentOrderAmount,
        setDisplayOrders,

        // Store actions
        getOrders,

        // Store getters
        currentOrderPrice,
        currentOrderValide,
        orderAmountByCitrusId,
        totalCitrusById,
        totalPrice
    }
}
