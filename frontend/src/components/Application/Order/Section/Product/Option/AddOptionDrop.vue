<template>
  <UtilsDrop
    pos="left"
    mode="click"
  >
    <template #default>
      <FormInput
        v-model="newOption"
        type="text"
        :value="newOption"
        name="option-name"
        label="Nom de l’option"
      />
      <UtilsButton
        width="small"
        @click="
          $emit('add-option', {
            newOption,
            application: $route.params.application,
          })
        "
      >
        Ajouter l’option
      </UtilsButton>
    </template>
  </UtilsDrop>
</template>

<script>
import UtilsDrop from '@/components/Utils/UtilsDrop'
import UtilsButton from '@/components/Utils/UtilsButton'
import FormInput from '@/components/Utils/Form/FormInput'
import { ref } from '@vue/composition-api'

export default {
    name: 'AddOptionDrop',
    components: {
        UtilsDrop,
        UtilsButton,
        FormInput
    },
    setup () {
        const newOption = ref('')

        return {
            newOption
        }
    }
}
</script>
