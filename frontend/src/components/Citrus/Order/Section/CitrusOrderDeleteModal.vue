<template>
  <UtilsModal
    id="citrus-order-delete-modal"
    :bg-close="true"
  >
    <template #header>
      <h2
        v-if="selectOrder === 'all'"
        class="uk-modal-title"
      >
        Supprimer toutes les commandes ?
      </h2>
      <h2
        v-else
        class="uk-modal-title"
      >
        Supprimer la commande de {{ selectOrder.user.username }}
      </h2>
    </template>
    <template #body>
      <p>
        Vous êtes sur le point de supprimer
        <span v-if="selectOrder === 'all'">
          toutes les commandes.
        </span>
        <span v-else>
          la commande de {{ selectOrder.user.username }}
        </span>
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
          v-if="selectOrder === 'all'"
          type="danger"
          @click="removeOrder"
        >
          Supprimer toutes les commandes
        </UtilsButton>
        <UtilsButton
          v-else
          type="danger"
          @click="removeOrder"
        >
          Supprimer la commande
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
        const {
            deleteAllOrders,
            deleteOrder,
            selectOrder
        } = useOrder()

        const removeOrder = () => {
            // eslint-disable-next-line no-undef
            UIkit.modal('#citrus-order-delete-modal').hide()
            if (selectOrder === 'all') {
                deleteAllOrders()
            } else {
                deleteOrder(selectOrder.id)
            }
        }

        return { removeOrder, selectOrder }
    }
}
</script>
