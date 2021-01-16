<template>
  <UtilsModal :bg-close="true">
    <template #header>
      <h2 class="uk-modal-title">
        Supprimer {{ product.name }} ?
      </h2>
    </template>
    <template #body>
      <p>
        Vous êtes sur le point de supprimer le produit :
        {{ product.name }},
        <span class="uk-text-bold uk-text-primary">
          il est recommandé de cacher le produit plutôt que de le supprimer.
        </span>
      </p>
    </template>
    <template #footer>
      <div class="uk-text-center">
        <UtilsButton
          type="secondary"
          class="uk-modal-close uk-margin-medium-right"
        >
          Annuler
        </UtilsButton>
        <UtilsButton
          type="danger"
          @click="removeCitrus"
        >
          Supprimer le produit
        </UtilsButton>
      </div>
    </template>
  </UtilsModal>
</template>

<script>
import useCitrus from '@/composition/citrus/useCitrus'
import { useHideModal } from '@/composition/useUtils'

import UtilsModal from '@/components/Utils/UtilsModal'
import UtilsButton from '@/components/Utils/UtilsButton'

export default {
  name: 'CitrusProductDelete',
  components: {
    UtilsButton,
    UtilsModal
  },
  setup () {
    const { citrusSelect, deleteCitrus } = useCitrus()

    const removeCitrus = () => {
      useHideModal('#citrus-product-delete')
      deleteCitrus(citrusSelect.value.id)
    }

    return { product: citrusSelect, removeCitrus }
  }
}
</script>
