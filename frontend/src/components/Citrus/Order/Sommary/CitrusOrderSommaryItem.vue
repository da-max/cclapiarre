<template>
  <tr>
    <td>
      <UtilsButton
        width="small"
        type="secondary"
      >
        {{ product.node.name }}
      </UtilsButton>
      <CitrusDetails :product="product" />
    </td>
    <td class="uk-width-2-5@m">
      <CitrusInputAmount
        :product="product.node"
        :amount="amount"
      />
    </td>
    <td>
      {{ Math.round(product.node.price * amount * 100) / 100 }} €
    </td>
  </tr>
</template>

<script>
import CitrusDetails from '@/components/Citrus/CitrusDetails'
import CitrusInputAmount from '@/components/Citrus/Order/CitrusInputAmount'
import UtilsButton from '@/components/Utils/UtilsButton'

export default {
    name: 'CitrusOrderSommaryItem',
    components: { UtilsButton, CitrusInputAmount, CitrusDetails },
    props: {
        product: {
            required: true,
            type: Object
        },
        amount: {
            required: true,
            type: Number
        }
    }
}
</script>
