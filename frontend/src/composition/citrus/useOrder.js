import { computed } from '@vue/composition-api'

import store from '@/store/index'

export default function () {
    // Store state
    // ===========
    const orders = computed(() => store.state.citrusOrder.orders)

    return {
        orders
    }
}
