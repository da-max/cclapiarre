<template>
  <div>
    <OrderSectionProductList :products="products"/>
  </div>
</template>

<script>
import OrderSectionProductList from '@/components/Application/Order/Section/OrderSectionProductList'

export default {
  name: 'OrderSection',
  props: {
    products: {
      type: Array,
      required: true
    }
  },
  components: {
    OrderSectionProductList
  }
}
</script>
