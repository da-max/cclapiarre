<template>
  <UtilsTable>
    <template
      #head
    >
      <th
        class="uk-background-secondary"
      >
        Nom du produit
      </th>
      <th
        v-show="!displayOrders"
        class="uk-background-secondary"
      >
        Ma commande
      </th>
      <th
        class="uk-background-secondary"
      >
        Total
      </th>
      <th
        v-for="order in orders"
        v-show="displayOrders"
        :key="order.node.id"
        class="uk-background-secondary"
      >
        {{ order.node.user.username }}
      </th>
    </template>
    <template #body>
      <CitrusOrderItem
        v-for="citrus in citrusDisplay"
        :key="citrus.node.id"
        :citrus="citrus"
      />
    </template>
    <template #foot>
      <td>Total</td>
      <td v-show="!displayOrders">
        {{ currentOrderPrice }} €
      </td>
      <td>{{ totalPrice }} €</td>
      <td
        v-for="order in orders"
        v-show="displayOrders"
        :key="order.node.id"
      >
        {{ totalPriceByOrderId(order.node.id) }} €
      </td>
    </template>
  </UtilsTable>
</template>

<script>
import useCitrus from '@/composition/citrus/useCitrus'
import useOrder from '@/composition/citrus/useOrder'

import CitrusOrderItem from '@/components/Citrus/Order/Section/CitrusOrderedItem'
import UtilsTable from '@/components/Utils/UtilsTable'

export default {
    name: 'CitrusOrderTable',
    components: {
        CitrusOrderItem,
        UtilsTable
    },
    setup () {
        const { citrusDisplay, setOrderAmount } = useCitrus()
        const {
            currentOrderPrice,
            displayOrders,
            orders,
            totalPrice,
            totalPriceByOrderId
        } = useOrder()

        return {
            citrusDisplay,
            currentOrderPrice,
            displayOrders,
            orders,
            setOrderAmount,
            totalPrice,
            totalPriceByOrderId
        }
    }
}
</script>

<style lang="scss" scoped>
table th {
  position: sticky;
  top: 80px;
  z-index: 10;
}
</style>
