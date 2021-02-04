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
  </UtilsModal>
</template>

<script>
import useCitrus from '@/composition/citrus/useCitrus'
import useOrder from '@/composition/citrus/useOrder'

import OrderInformation from '@/components/Application/Order/Section/OrderInformation'
import UtilsModal from '@/components/Utils/UtilsModal'
import UtilsTable from '@/components/Utils/UtilsTable'
import CitrusOrderSommaryItem from '@/components/Citrus/Order/Sommary/CitrusOrderSommaryItem'

export default {
    name: 'CitrusOrderSommaryModal',
    components: {
        CitrusOrderSommaryItem,
        UtilsTable,
        OrderInformation,
        UtilsModal
    },
    setup () {
        const { currentOrderPrice, currentOrder } = useOrder()
        const { citrusById } = useCitrus()

        return { price: currentOrderPrice, currentOrder, citrusById }
    }
}
</script>
