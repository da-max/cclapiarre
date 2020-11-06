<template>
  <div>
    <ProductOrderedList class="uk-margin-xlarge uk-width-4-5@l uk-margin-auto" />

    <ProductList :products="products"/>
  </div>
</template>

<script>
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
    ProductOrderedList
  }
}
</script>
