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
  </UtilsTable>
</template>

<script>
import useCitrus from '@/composition/citrus/useCitrus'

import CitrusOrderItem from '@/components/Citrus/Order/Section/CitrusOrderItem'
import UtilsTable from '@/components/Utils/UtilsTable'

export default {
  name: 'CitrusOrderTable',
  components: {
    CitrusOrderItem,
    UtilsTable
  },
  setup () {
    const { citrusDisplay, setOrderAmount } = useCitrus()

    return { citrusDisplay, setOrderAmount }
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
