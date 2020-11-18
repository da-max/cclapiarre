<template>
  <UtilsDrop pos="right" id="addOption" mode="click">
    <template>
      <FormInput
        type="number"
        :value="newWeight.weight"
        v-model="newWeight.weight"
        name="weight"
        label="Poids"
      />
      <FormInput
        type="text"
        :value="newWeight.unit"
        v-model="newWeight.unit"
        name="unit"
        label="Unité du poids"
      />
      <FormInput
        type="number"
        :value="newWeight.price"
        v-model="newWeight.price"
        name="price"
        label="Prix du produit pour ce poids"
      />
      <UtilsButton
        width="small"
        @click="
          $emit('add-weight', {
            application: $route.params.application,
            newWeight,
          })
        "
        >Ajouter le poids</UtilsButton
      >
    </template>
  </UtilsDrop>
</template>

<script>
import { ref } from '@vue/composition-api'

import UtilsButton from '@/components/Utils/UtilsButton'
import UtilsDrop from '@/components/Utils/UtilsDrop'
import FormInput from '@/components/Utils/Form/FormInput'

export default {
  name: 'AddWeightDrop',
  components: {
    UtilsButton,
    UtilsDrop,
    FormInput
  },
  setup () {
    const newWeight = ref({
      price: 0,
      unit: '',
      weight: 0
    })

    return { newWeight }
  }

}
</script>
