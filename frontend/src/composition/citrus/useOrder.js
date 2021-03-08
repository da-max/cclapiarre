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

    const clearCurrentOrder = () => {
        store.commit('citrusOrder/CLEAR_CURRENT_ORDER')
    }

    const clearSelectOrder = () => {
        store.commit('citrusOrder/CLEAR_SELECT_ORDER')
    }

    const setCurrentOrder = (order) => {
        store.commit('citrusOrder/SET_CURRENT_ORDER', order)
    }

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
    const deleteAllOrders = () => store.dispatch('citrusOrder/deleteAllOrders')
    const deleteOrder = (orderId) => store.dispatch('citrusOrder/deleteOrder', orderId)
    const saveOrder = () => store.dispatch('citrusOrder/saveOrder')
    const updateOrder = () => store.dispatch('citrusOrder/updateOrder')

    // Store getters
    // =============
    const amountByOrderIdCitrusId = (orderId, citrusId) => store.getters['citrusOrder/amountByOrderIdCitrusId'](orderId, citrusId)
    const currentAmountByCitrusId = (citrusId) => store.getters['citrusOrder/currentAmountByCitrusId'](citrusId)
    const currentOrderPrice = computed(() => store.getters['citrusOrder/currentOrderPrice'])
    const currentOrderValide = computed(() => store.getters['citrusOrder/currentOrderValide'])
    const getOrderById = (orderId) => store.getters['citrusOrder/getOrderById'](orderId)
    const getSelectOrder = computed(() => store.getters['citrusOrder/getSelectOrder'])
    const ordersLength = computed(() => store.getters['citrusOrder/ordersLength'])
    const totalCitrusById = (citrusId) => store.getters['citrusOrder/totalCitrusById'](citrusId)
    const totalPrice = computed(() => store.getters['citrusOrder/totalPrice'])
    const totalPriceByOrderId = (orderId) => store.getters['citrusOrder/totalPriceByOrderId'](orderId)

    // Getters
    // =======
    const canChangeOrder = () => store.getters['auth/findPermission']('change_citrusorder')
    const canDeleteOrder = () => store.getters['auth/findPermission']('delete_citrusorder')
    const totalCitrus = (citrus) => totalCitrusById(citrus.node.id)

    // Methods
    // =======

    const displayCitrusOrderDeleteModal = (orderId = null) => {
        setSelectOrder(orderId)
        useShowModal('#citrus-order-delete-modal')

        // eslint-disable-next-line no-undef
        UIkit.util.on(
            '#citrus-order-delete-modal',
            'hidden',
            () => {
                clearSelectOrder()
            })
    }

    const displayCitrusOrderUpdateModal = async (orderId = null) => {
        await setSelectOrder(orderId)
        const order = await getSelectOrder.value.amounts.edges.map(o => ({
            amount: o.node.amount,
            citrusId: o.node.product.id
        }))
        setCurrentOrder(order)
        useShowModal('#citrus-order-update-modal')

        // eslint-disable-next-line no-undef
        UIkit.util.on(
            '#citrus-order-update-modal',
            'hidden',
            () => {
                clearCurrentOrder()
                clearSelectOrder()
            })
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
        clearCurrentOrder,
        clearSelectOrder,
        deleteAllOrders,
        deleteOrder,
        getOrders,
        saveOrder,
        updateOrder,

        // Store getters
        amountByOrderIdCitrusId,
        currentAmountByCitrusId,
        currentOrderPrice,
        currentOrderValide,
        getOrderById,
        getSelectOrder,
        ordersLength,
        totalCitrusById,
        totalPrice,
        totalPriceByOrderId,

        // Methods
        displayCitrusOrderDeleteModal,
        displayCitrusOrderUpdateModal,
        orderAmountByCitrusId,

        // Getters
        canChangeOrder,
        canDeleteOrder,
        totalCitrus

    }
}
