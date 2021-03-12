<template>
  <form>
    <select
      v-model="action"
      name="actions"
      class="uk-select"
    >
      <option :value="null">
        ------ ------
      </option>
      <option
        v-for="ACTION in ACTIONS"
        :key="ACTION.content"
        :value="ACTION.value"
      >
        {{ ACTION.content }}
      </option>
    </select>
    <FormInputNumber
      v-if="action && typeof(action.value) === 'number'"
      v-model="action.value"
      class="uk-margin-small-top"
      label="Pourcentage à ajouter"
      :display-info="false"
      :max="100"
      :min="-100"
      :step="0.01"
      :value="action.value"
      name="pourcentage"
    />
    <div class="uk-text-center uk-margin-small-top">
      <UtilsButton
        v-show="action && action.value !== 0 && citrusChecked && citrusChecked.length !== 0"
        class="uk-margin-medium-left"
        @click="patchCitrus({...action})"
      >
        Appliquer
      </UtilsButton>
    </div>
  </form>
</template>

<script>
import { reactive, toRefs } from '@vue/composition-api'
import useCitrus from '@/composition/citrus/useCitrus'

import FormInputNumber from '@/components/Utils/Form/FormInputNumber'
import UtilsButton from '@/components/Utils/UtilsButton'

export default {
    name: 'CitrusProductListActions',
    components: {
        FormInputNumber,
        UtilsButton
    },
    setup () {
        const { citrusChecked, patchCitrus } = useCitrus()

        const state = reactive({
            ACTIONS: [
                {
                    value: { key: 'display', value: false },
                    content: 'Cacher les produits'
                },
                {
                    value: { key: 'display', value: true },
                    content: 'Afficher les produits'
                },
                {
                    value: { key: 'maybeNotAvailable', value: true },
                    content: 'Produits potentiellement indisponible'
                },
                {
                    value: { key: 'maybeNotAvailable', value: false },
                    content: 'Produits disponible'
                },
                {
                    value: { key: 'price', value: 10, type: 'percent' },
                    content: 'Ajouter un pourcentage du prix'
                }
            ],
            action: null
        })

        return {
            ...toRefs(state),
            citrusChecked,
            patchCitrus
        }
    }
}
</script>

<style>

</style>
