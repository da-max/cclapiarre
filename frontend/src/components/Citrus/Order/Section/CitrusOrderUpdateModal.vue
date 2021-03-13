<template>
  <UtilsModal
    v-if="selectOrder"
    id="citrus-order-update-modal"
    :center="true"
    :container="true"
  >
    <template #header>
      <h2 class="uk-modal-title">
        Modifier la commande de {{ selectOrder.user.username }}
      </h2>
    </template>
    <template #body>
      <aside class="uk-margin-small-top uk-width-2-3@m uk-margin-auto">
        <OrderInformation :information="selectOrder.user" />
        <div class="uk-text-center uk-margin-medium-top uk-text-bold">
          <div class="uk-margin-bottom">
            <label
              for="send-mail"
              class="uk-label uk-margin-medium-right"
            >Envoyer un mail récapitulatif</label>
            <input
              id="send-mail"
              :checked="selectOrder.sendMail"
              type="checkbox"
              name="send-mail"
              class="uk-checkbox uk-disabled"
            >
          </div>
          <span class="uk-label">Prix actuel de la commande</span>
          <span>
            {{ currentOrderPrice }} €
          </span>
        </div>
      </aside>
      <UtilsTable class="uk-margin-medium-top">
        <template #head>
          <th>Nom des produits</th>
          <th>Commande de {{ selectOrder.user.username }}</th>
          <th>Total</th>
        </template>
        <template #body>
          <tr
            v-for="citrus in citrusDisplay"
            :key="citrus.node.id"
          >
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
              <CitrusInputAmount
                :product="citrus.node"
                :order-id="selectOrder.id"
              />
            </td>
            <td class="uk-width-1-4">
              {{ totalCitrus(citrus) }}
              <span v-if="citrus.node.weight !== 1">
                caisse⋅s (Soit {{ totalCitrus(citrus) * citrus.node.weight }}kg)
              </span>
            </td>
          </tr>
        </template>
      </UtilsTable>
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
          type="primary"
          @click="saveOrder"
        >
          Modifier
        </UtilsButton>
      </div>
    </template>
  </UtilsModal>
</template>

<script>
import useCitrus from '@/composition/citrus/useCitrus'
import useOrder from '@/composition/citrus/useOrder'

import CitrusDetails from '@/components/Citrus/CitrusDetails'
import CitrusInputAmount from '@/components/Citrus/Order/CitrusInputAmount'
import UtilsButton from '@/components/Utils/UtilsButton'
import UtilsModal from '@/components/Utils/UtilsModal'
import UtilsTable from '@/components/Utils/UtilsTable'
import OrderInformation from '@/components/Application/Order/Section/OrderInformation.vue'

export default {
    name: 'CitrusOrderUpdateModal',
    components: {
        CitrusDetails,
        CitrusInputAmount,
        OrderInformation,
        UtilsButton,
        UtilsModal,
        UtilsTable
    },
    setup () {
        const { citrusDisplay } = useCitrus()
        const {
            currentOrder,
            currentOrderPrice,
            getSelectOrder,
            totalCitrus,
            updateOrder
        } = useOrder()

        const saveOrder = () => {
            // eslint-disable-next-line no-undef
            UIkit.modal('#citrus-order-update-modal').hide()
            updateOrder()
        }

        return {
            citrusDisplay,
            currentOrder,
            currentOrderPrice,
            selectOrder: getSelectOrder,
            totalCitrus,
            saveOrder
        }
    }
}
</script>
