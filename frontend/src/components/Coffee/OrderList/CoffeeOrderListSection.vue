<template>
  <section
    class="uk-margin-medium-top uk-width-1-2@m uk-margin-auto"
  >
    <CoffeeOrderListConfirmRemove
      :order="orderToDelete"
      :all="all"
      @refetch-order="refetchOrderAll"
    />
    <header
      v-show="!loading && orders.edges.length !== 0"
      class="uk-margin-large-bottom"
    >
      <a
        class="uk-button uk-button-secondary"
        href="#"
      >
        Générer le récapitulatif PDF de la commande
      </a>
      <UtilsButton
        type="danger"
        class="uk-margin-large-left"
        @click="confirmRemoveAllOrder"
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
        @confirm-remove="confirmRemoveOrder"
      />
    </section>
    <CoffeeDetails
      id="coffee-details"
      :coffee="coffeeSelect"
    />
  </section>
</template>

<script>
import { reactive, toRefs } from '@vue/composition-api'
import useCoffee from '@/composition/coffee/useCoffee'
import { useShowModal } from '@/composition/useUtils'

import CoffeeDetails from '@/components/Coffee/Order/Section/Coffee/CoffeeDetails'
import CoffeeOrderListItem from '@/components/Coffee/OrderList/CoffeeOrderListItem.vue'
import UtilsButton from '@/components/Utils/UtilsButton'
import CoffeeOrderListConfirmRemove from '@/components/Coffee/OrderList/CoffeeOrderListConfirmRemove'

export default {
  name: 'CoffeeOrderListSection',
  components: {
    CoffeeOrderListConfirmRemove,
    CoffeeDetails,
    CoffeeOrderListItem,
    UtilsButton
  },
  setup () {
    const state = reactive({
      all: true,
      orderToDelete: []
    })

    const {
      coffeeSelect,
      displayDetails,
      allOrder
    } = useCoffee()

    const { orders, loading, refetchOrderAll } = allOrder()

    const confirmRemoveAllOrder = () => {
      state.orderToDelete = orders.value.edges
      state.all = true
      useShowModal('#confirm-remove-order')
    }

    const confirmRemoveOrder = (order) => {
      state.orderToDelete = order
      state.all = false
      useShowModal('#confirm-remove-order')
    }

    return {
      orders,
      loading,
      coffeeSelect,
      displayDetails,
      refetchOrderAll,
      confirmRemoveAllOrder,
      confirmRemoveOrder,
      ...toRefs(state)
    }
  }
}
</script>
