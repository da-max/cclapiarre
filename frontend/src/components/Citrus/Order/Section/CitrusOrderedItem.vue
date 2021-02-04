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
    <td>
      <CitrusInputAmount :product="citrus.node" />
    </td>
    <td class="uk-width-1-2">
      {{ totalCitrus(citrus) }}
      <span v-if="citrus.node.weight !== 1">
        caisse⋅s (Soit {{ totalCitrus(citrus) * citrus.node.weight }}kg)
      </span>
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
        const { totalCitrusById } = useOrder()

        const totalCitrus = (citrus) => totalCitrusById(citrus.node.id)

        return { totalCitrus }
    }
}
</script>
