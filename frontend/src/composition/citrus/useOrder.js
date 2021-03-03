import { computed } from '@vue/composition-api'
import { useShowModal } from '@/composition/useUtils'

import store from '@/store/index'

export default function () {
    // Store state
    // ===========

    const currentOrder = computed(() => store.state.citrusOrder.currentOrder)
    const displayOrders = computed(() => store.state.citrusOrder.displayOrders)
    const hasOrder = computed(() => store.state.citrusOrder.hasOrder)
    const orders = computed(() => store.state.citrusOrder.orders)
    const selectOrder = computed(() => store.state.citrusOrder.selectOrder)
    const sendMail = computed(() => store.state.sendMail)

    // Store mutations
    // ===============

    const setCurrentOrderAmount = (citrusId, amount = 0) => {
        store.commit('citrusOrder/SET_CURRENT_ORDER_AMOUNT', { citrusId, amount: Number(amount) })
    }

    const setDisplayOrders = (value) => {
        store.commit('citrusOrder/SET_DISPLAY_ORDERS', value)
    }

    const setSelectOrder = (value) => {
        store.commit('citrusOrder/SET_SELECT_ORDER', value)
    }

    const setSendMail = (value) => {
        store.commit('citrusOrder/SET_SEND_MAIL', value)
    }

    // Store actions
    // =============
    const getOrders = () => store.dispatch('citrusOrder/getOrders')
    const saveOrder = () => store.dispatch('citrusOrder/saveOrder')
    const deleteAllOrders = () => store.dispatch('citrusOrder/deleteAllOrders')

    // Store getters
    // =============
    const currentAmountByCitrusId = (citrusId) => store.getters['citrusOrder/currentAmountByCitrusId'](citrusId)
    const currentOrderPrice = computed(() => store.getters['citrusOrder/currentOrderPrice'])
    const currentOrderValide = computed(() => store.getters['citrusOrder/currentOrderValide'])
    const ordersLength = computed(() => store.getters['citrusOrder/ordersLength'])
    const totalCitrusById = (citrusId) => store.getters['citrusOrder/totalCitrusById'](citrusId)
    const totalPrice = computed(() => store.getters['citrusOrder/totalPrice'])
    const totalPriceByOrderId = (orderId) => store.getters['citrusOrder/totalPriceByOrderId'](orderId)

    // Getters
    // =======
    const canChangeOrder = () => store.getters['auth/findPermission']('change_citrusorder')
    const canDeleteOrder = () => store.getters['auth/findPermission']('delete_citrusorder')

    // Methods
    // =======

    const displayCitrusOrderDeleteModal = (order) => {
        setSelectOrder(order)
        useShowModal('#citrus-order-delete-modal')
    }

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
        currentOrder,
        displayOrders,
        hasOrder,
        orders,
        selectOrder,
        sendMail,

        // Store mutations
        setCurrentOrderAmount,
        setDisplayOrders,
        setSelectOrder,
        setSendMail,

        // Store actions
        deleteAllOrders,
        getOrders,
        saveOrder,

        // Store getters
        currentAmountByCitrusId,
        currentOrderPrice,
        currentOrderValide,
        ordersLength,
        totalCitrusById,
        totalPrice,
        totalPriceByOrderId,

        // Methods
        displayCitrusOrderDeleteModal,
        orderAmountByCitrusId,

        // Getters
        canChangeOrder,
        canDeleteOrder

    }
}
