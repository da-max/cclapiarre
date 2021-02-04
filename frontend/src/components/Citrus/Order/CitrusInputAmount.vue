<template>
  <FormInputNumber
    :name="product.name"
    :value="amount"
    label="Quantité commandé"
    :display-info="false"
    :display-label="false"
    :step="product.step"
    :max="product.maximum"
    @input="changeOrderAmount"
  />
</template>

<script>
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
        const { setCurrentOrderAmount } = useOrder()

        const changeOrderAmount = (newAmount) => {
            setCurrentOrderAmount(props.product.id, newAmount)
        }

        return {
            changeOrderAmount
        }
    }
}
</script>

<style scoped>

</style>
