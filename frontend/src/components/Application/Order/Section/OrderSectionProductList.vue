<template>
  <div
    uk-grid
    class="uk-child-width-1-3@l uk-child-width-1-2@m uk-grid-match uk-grid-large uk-text-center uk-flex-center"
  >
    <div v-for="product in products" :key="product.node.id">
      <OrderSectionProductItem class="product-card" :product="product" />
    </div>
  </div>
</template>
<script>
import OrderSectionProductItem from '@/components/Application/Order/Section/OrderSectionProductItem'
export default {
  name: 'OrderSectionProductList',
  props: {
    products: {
      type: Array,
      required: true
    }
  },
  components: {
    OrderSectionProductItem
  }
}
</script>
