<template>
  <tr>
    <td>
      <div class="uk-inline">
        <UtilsButton
          type="secondary"
        >
          {{ citrus.node.name }}
        </UtilsButton>
        <CitrusDetails :product="citrus" />
      </div>
    </td>
    <td v-if="!displayOrders">
      <CitrusInputAmount :product="citrus.node" />
    </td>
    <td :class="{'uk-width-1-2': !displayOrders}">
      {{ totalCitrus(citrus) }}
      <span v-if="citrus.node.weight !== 1">
        caisse⋅s (Soit {{ totalCitrus(citrus) * citrus.node.weight }}kg)
      </span>
    </td>
    <td
      v-for="order in orders"
      v-show="displayOrders"
      :key="order.node.id"
    >
      {{ orderAmountByCitrusId(order.node, citrus.node.id) }}
    </td>
  </tr>
</template>

<script>
import useOrder from '@/composition/citrus/useOrder'

import CitrusDetails from '@/components/Citrus/CitrusDetails'
import UtilsButton from '@/components/Utils/UtilsButton'
import CitrusInputAmount from '@/components/Citrus/Order/CitrusInputAmount'

export default {
    name: 'CitrusOrderItem',
    components: {
        CitrusInputAmount,
        CitrusDetails,
        UtilsButton
    },
    props: {
        citrus: {
            required: true,
            type: Object
        }
    },
    setup () {
        const {
            displayOrders,
            orders,
            orderAmountByCitrusId,
            totalCitrus
        } = useOrder()

        return {
            displayOrders,
            orders,
            orderAmountByCitrusId,
            totalCitrus
        }
    }
}
</script>
