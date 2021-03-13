<template>
  <UtilsModal
    id="citrus-ordered-sommary"
    :center="true"
    :container="true"
  >
    <template #header>
      <h2 class="uk-modal-title">
        Récapitulatif de la commande
      </h2>
    </template>
    <template #body>
      <OrderInformation />
      <p class="uk-text-center uk-margin-large-bottom uk-text-bold">
        <span class="uk-label">Prix de votre commande</span> {{ price }} €
      </p>
      <UtilsTable>
        <template #head>
          <th>Produit</th>
          <th>Quantité commandée</th>
          <th>Prix</th>
        </template>
        <template #body>
          <CitrusOrderSommaryItem
            v-for="order in currentOrder"
            :key="order.citrusId"
            :product="citrusById(order.citrusId)"
            :amount="order.amount"
          />
        </template>
      </UtilsTable>
    </template>
    <template #footer>
      <div class="uk-text-center">
        <UtilsButton
          type="secondary"
          class="uk-margin-medium-right uk-modal-close"
        >
          Annuler
        </UtilsButton>
        <UtilsButton @click="addOrder">
          Commander
        </UtilsButton>
      </div>
    </template>
  </UtilsModal>
</template>

<script>
import useCitrus from '@/composition/citrus/useCitrus'
import useOrder from '@/composition/citrus/useOrder'

import CitrusOrderSommaryItem from '@/components/Citrus/Order/Sommary/CitrusOrderSommaryItem'
import OrderInformation from '@/components/Application/Order/Section/OrderInformation'
import UtilsModal from '@/components/Utils/UtilsModal'
import UtilsTable from '@/components/Utils/UtilsTable'
import UtilsButton from '@/components/Utils/UtilsButton'

export default {
    name: 'CitrusOrderSommaryModal',
    components: {
        CitrusOrderSommaryItem,
        OrderInformation,
        UtilsButton,
        UtilsModal,
        UtilsTable

    },
    setup () {
        const { currentOrderPrice, currentOrder, saveOrder } = useOrder()
        const { citrusById } = useCitrus()

        const addOrder = () => {
            // eslint-disable-next-line no-undef
            UIkit.modal('#citrus-ordered-sommary').hide()
            saveOrder()
        }

        return { addOrder, price: currentOrderPrice, currentOrder, citrusById }
    }
}
</script>
