<template>
  <UtilsModal
    id="citrus-orders-delete-all-modal"
    :bg-close="true"
  >
    <template #header>
      <h2 class="uk-modal-title">
        Supprimer toutes les commandes ?
      </h2>
    </template>
    <template #body>
      <p>
        Vous êtes sur le point de supprimer toutes les commandes.
        <span class="uk-text-bold uk-text-warning">
          Attention, cette action est irréversible !
        </span>
      </p>
    </template>
    <template #footer>
      <div class="uk-text-center">
        <UtilsButton
          class="uk-modal-close uk-margin-medium-right"
          type="secondary"
        >
          Annuler
        </UtilsButton>
        <UtilsButton
          type="danger"
          @click="removeAllOrders"
        >
          Supprimer toutes les commandes
        </UtilsButton>
      </div>
    </template>
  </UtilsModal>
</template>

<script>
import useOrder from '@/composition/citrus/useOrder'

import UtilsModal from '@/components/Utils/UtilsModal'
import UtilsButton from '@/components/Utils/UtilsButton.vue'

export default {
    name: 'CitrusOrdersDeleteAllModal',
    components: {
        UtilsModal,
        UtilsButton
    },
    setup () {
        const { deleteAllOrders } = useOrder()

        const removeAllOrders = () => {
            // eslint-disable-next-line no-undef
            UIkit.modal('#citrus-orders-delete-all-modal').hide()
            deleteAllOrders()
        }

        return { removeAllOrders }
    }
}
</script>
