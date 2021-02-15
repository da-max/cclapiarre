<template>
  <FormInputNumber
    v-model="changeOrderAmount"
    :name="product.name"
    :value="amount"
    label="Quantité commandé"
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
        amount: {
            required: false,
            type: Number,
            default: 0
        }
    },
    setup (props) {
        const { currentAmountByCitrusId, setCurrentOrderAmount } = useOrder()

        const changeOrderAmount = computed({
            get: () => currentAmountByCitrusId(props.product.id),
            set: (newAmount) => setCurrentOrderAmount(props.product.id, newAmount)
        })

        return {
            changeOrderAmount
        }
    }
}
</script>

<style scoped>

</style>
