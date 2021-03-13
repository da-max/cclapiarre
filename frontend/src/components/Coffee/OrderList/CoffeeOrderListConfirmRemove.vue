<template>
  <UtilsModal id="confirm-remove-order">
    <template #header>
      <h2 class="uk-modal-title">
        {{ all ? allHeader : uniqHeader + order.node.user.username }}
      </h2>
    </template>
    <template #body>
      <p>
        {{ all ? allBody : uniqBody + order.node.user.username }}
        <span
          class="uk-text-danger uk-text-bold"
        >attention, cette action est irréversible !!</span>
      </p>
    </template>
    <template #footer>
      <div class="uk-text-center">
        <UtilsButton
          type="danger"
          @click="removeOrder"
        >
          Supprimer
        </UtilsButton>
        <UtilsButton
          type="default"
          class="uk-modal-close uk-margin-medium-left"
        >
          Annuler
        </UtilsButton>
      </div>
    </template>
  </UtilsModal>
</template>

<script>
import { reactive, toRefs } from '@vue/composition-api'
import store from '@/store/index'
import { useUtilsMutation, useHideModal } from '@/composition/useUtils'
import useCoffee from '@/composition/coffee/useCoffee'

import UtilsModal from '@/components/Utils/UtilsModal'
import UtilsButton from '@/components/Utils/UtilsButton'

export default {
    name: 'CoffeeOrderListConfirmRemove',
    components: {
        UtilsModal,
        UtilsButton
    },
    props: {
        all: {
            required: false,
            default: true,
            type: Boolean
        },
        order: {
            required: true,
            default: () => ({}),
            type: [Object, Array]
        }
    },
    setup (props, { emit }) {
        const state = reactive({
            allHeader: 'Supprimer toutes les commandes ?',
            uniqHeader: 'Supprimer la commande de ',
            allBody:
        'Vous êtes sur le point de supprimer toutes les commandes de café',
            uniqBody: 'Vous êtes sur le point de supprimer la commande de '
        })

        const { orderRemove, onDoneRemoveOrder } = useCoffee()

        const removeOrder = () => {
            useHideModal('#confirm-remove-order')
            if (Array.isArray(props.order)) {
                const ordersId = props.order.map((order) => order.node.id)
                useUtilsMutation(orderRemove, { ordersId })
            } else {
                useUtilsMutation(orderRemove, { ordersId: props.order.node.id })
            }
        }

        onDoneRemoveOrder((result) => {
            if (result.data.batchRemoveCoffeeOrder.deletionCount !== 0) {
                emit('refetch-order')
                store.commit('alert/ADD_ALERT', {
                    header: true,
                    headerContent: props.all
                        ? 'Commandes supprimées'
                        : 'Commande supprimée.',
                    body: props.all
                        ? 'Toutes les commandes ont été supprimées.'
                        : 'La commande a bien été supprimée.',
                    status: 'success',
                    close: true
                })
            } else {
                store.commit('alert/ADD_ALERT', {
                    header: true,
                    headerContent: props.all
                        ? 'Commandes non trouvées'
                        : 'Commande non trouvée',
                    body: props.all
                        ? 'Les commandes n’ont pas pu être supprimées.'
                        : 'La commande n’a pas pu être supprimée.',
                    status: 'warning',
                    close: true
                })
            }
        })
        return { ...toRefs(state), removeOrder }
    }
}
</script>
