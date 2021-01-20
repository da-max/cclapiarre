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
      <FormInputNumber
        :name="citrus.node.name"
        :value="0"
        label="Quantité commandé"
        :display-info="false"
        :display-label="false"
        :step="citrus.node.step"
        :max="citrus.node.maximum"
        @input="changeCitrusAmount"
      />
    </td>
  </tr>
</template>

<script>
import useCitrus from '@/composition/citrus/useCitrus'

import CitrusDetails from '@/components/Citrus/CitrusDetails'
import UtilsButton from '@/components/Utils/UtilsButton'
import FormInputNumber from '@/components/Utils/Form/FormInputNumber'

export default {
  name: 'CitrusOrderItem',
  components: {
    FormInputNumber,
    CitrusDetails,
    UtilsButton
  },
  props: {
    citrus: {
      required: true,
      type: Object
    }
  },
  setup (props) {
    const { setCitrusAmount } = useCitrus()

    const changeCitrusAmount = (amount) => {
      setCitrusAmount(props.citrus.node.id, amount)
    }

    return { changeCitrusAmount }
  }
}
</script>
