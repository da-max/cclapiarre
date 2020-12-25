<template>
  <section
    class="uk-margin-medium-top uk-width-1-2@m uk-margin-auto"
  >
    <header class="uk-margin-large-bottom">
      <a
        class="uk-button uk-button-secondary"
        href="#"
      >
        Générer le récapitulatif PDF de la commande
      </a>
      <UtilsButton
        type="danger"
        class="uk-margin-large-left"
        @click="removeAllOrder"
      >
        Supprimer toutes les commandes
      </UtilsButton>
    </header>
    <div
      v-if="loading"
      class="uk-text-center"
    >
      Chargement en cours.
    </div>
    <div
      v-else-if="orders.edges.length === 0"
      class="uk-text-center"
    >
      Aucune commande n’a été trouvé.
    </div>
    <section
      v-for="order in orders.edges"
      v-else
      :key="order.node.id"
    >
      <CoffeeOrderListItem
        :order="order"
        @display-details="(coffee) => displayDetails(coffee)"
        @order-delete="refetchOrderAll()"
      />
    </section>
    <CoffeeDetails
      id="coffee-details"
      :coffee="coffeeSelect"
    />
  </section>
</template>

<script>
import useCoffee from '@/composition/coffee/useCoffee'
import store from '@/store/index'
import { useUtilsMutation } from '@/composition/useUtils'

import CoffeeDetails from '@/components/Coffee/Order/Section/Coffee/CoffeeDetails'
import CoffeeOrderListItem from '@/components/Coffee/OrderList/CoffeeOrderListItem.vue'
import UtilsButton from '@/components/Utils/UtilsButton'

export default {
  name: 'CoffeeOrderListSection',
  components: { CoffeeDetails, CoffeeOrderListItem, UtilsButton },
  setup () {
    const { coffeeSelect, displayDetails, allOrder, orderRemove, onDoneRemoveOrder } = useCoffee()

    const { orders, loading, refetchOrderAll } = allOrder()

    const removeAllOrder = () => {
      const ordersId = orders.value.edges.map(order => order.node.id)
      useUtilsMutation(orderRemove, { ordersId })
    }

    onDoneRemoveOrder((result) => {
      if (result.data.batchRemoveCoffeeOrder.deletionCount !== 0) {
        refetchOrderAll()
        store.commit('alert/ADD_ALERT', {
          header: true,
          headerContent: 'Commandes supprimées',
          body: 'Toutes les commandes ont été supprimées.',
          status: 'success',
          close: true
        })
      } else {
        store.commit('alert/ADD_ALERT', {
          header: true,
          headerContent: 'Commande non trouvé',
          body: 'Les commandes n’ont pas pu être supprimées.',
          status: 'warning',
          close: true
        })
      }
    })

    return { orders, loading, coffeeSelect, displayDetails, refetchOrderAll, removeAllOrder }
  }
}
</script>
