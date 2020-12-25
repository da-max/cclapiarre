<template>
  <section
    class="uk-margin-medium-top uk-width-1-2@m uk-margin-auto"
  >
    <div
      v-if="!loading || orders.edges.length === 0"
      class="uk-text-center"
    >
      Aucune commande n’a été trouvé.
    </div>
    <div
      v-for="order in orders.edges"
      :key="order.node.id"
    >
      <CoffeeOrderListItem
        :order="order"
        @display-details="(coffee) => displayDetails(coffee)"
        @order-delete="refetchOrderAll()"
      />
    </div>
    <CoffeeDetails
      id="coffee-details"
      :coffee="coffeeSelect"
    />
  </section>
</template>

<script>
import useCoffee from '@/composition/coffee/useCoffee'

import CoffeeDetails from '@/components/Coffee/Order/Section/Coffee/CoffeeDetails'

import CoffeeOrderListItem from './CoffeeOrderListItem.vue'

export default {
  name: 'CoffeeOrderListSection',
  components: { CoffeeDetails, CoffeeOrderListItem },
  setup () {
    const { coffeeSelect, displayDetails, allOrder } = useCoffee()

    const { orders, loading, refetchOrderAll } = allOrder()

    return { orders, loading, coffeeSelect, displayDetails, refetchOrderAll }
  }
}
</script>
