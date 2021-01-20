<template>
  <form>
    <select
      v-model="action"
      name="actions"
      class="uk-select uk-form-width-medium"
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
    <UtilsButton
      v-show="action && citrusChecked && citrusChecked.length !== 0"
      class="uk-margin-medium-left"
      @click="patchCitrus(action)"
    >
      Appliquer
    </UtilsButton>
  </form>
</template>

<script>
import { reactive, toRefs } from '@vue/composition-api'
import useCitrus from '@/composition/citrus/useCitrus'

import UtilsButton from '@/components/Utils/UtilsButton'

export default {
    name: 'CitrusProductListActions',
    components: {
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
