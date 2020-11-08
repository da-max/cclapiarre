<template>
  <div>
    <OrderInformation class="uk-width-1-2@l uk-margin-auto" />
    <ProductOrderedList class="uk-margin-xlarge uk-width-4-5@l uk-margin-auto" id="order-list" />

    <ProductList :products="products"/>
  </div>
</template>

<script>
import OrderInformation from '@/components/Application/Order/Section/OrderInformation'
import ProductList from '@/components/Application/Order/Section/Product/ProductList'
import ProductOrderedList from '@/components/Application/Order/Section/Order/ProductOrderedList'

export default {
  name: 'OrderSection',
  props: {
    products: {
      type: Array,
      required: true
    }
  },
  components: {
    ProductList,
    ProductOrderedList,
    OrderInformation
  }
}
</script>
