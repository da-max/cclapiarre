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
        class="uk-background-secondary"
      >
        Ma commande
      </th>
      <th
        class="uk-background-secondary"
      >
        Total
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
      <td>{{ currentOrderPrice }} €</td>
      <td>{{ totalPrice }} €</td>
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
        const { currentOrderPrice, totalPrice } = useOrder()

        return { citrusDisplay, currentOrderPrice, setOrderAmount, totalPrice }
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
