<template>
  <FormInputNumber
    v-model="changeOrderAmount"
    :name="product.name"
    :value="changeOrderAmount"
    label="Quantité commandé"
    :class="{'uk-disabled': hasOrder}"
    :display-info="false"
    :display-label="false"
    :step="product.step"
    :max="product.maximum"
  />
</template>

<script>
import { computed } from '@vue/composition-api'
import useOrder from '@/composition/citrus/useOrder'

import FormInputNumber from '@/components/Utils/Form/FormInputNumber'

export default {
    name: 'CitrusInputAmount',
    components: {
        FormInputNumber
    },
    props: {
        product: {
            required: true,
            type: Object
        },
        orderId: {
            required: false,
            type: String,
            default: null
        }
    },
    setup (props) {
        const product = computed(() => props.product)
        const orderId = computed(() => props.orderId)
        const {
            currentAmountByCitrusId,
            hasOrder,
            setCurrentOrderAmount
        } = useOrder()

        const changeOrderAmount = computed({
            get: () =>
                currentAmountByCitrusId(product.value.id),
            set: (newAmount) => {
                setCurrentOrderAmount(product.value.id, newAmount)
            }
        })

        return {
            changeOrderAmount,
            hasOrder: orderId.value ? false : hasOrder
        }
    }
}
</script>
