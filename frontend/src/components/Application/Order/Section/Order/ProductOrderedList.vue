<template>
  <section>
    <div class="uk-text-center uk-margin-large-bottom">
      <p><span class="uk-label">Prix de votre commande</span> {{ price }} €</p>
    </div>
    <transition-group
      name="fade"
      tag="div"
      class="uk-flex-center uk-child-width-1-2@l uk-grid-match"
      uk-grid
    >
      <div v-for="productOrdered in productsOrdered" :key="productOrdered.id">
        <ProductOrderedItem :productOrdered="productOrdered" />
      </div>
    </transition-group>
    <div
      class="uk-text-center uk-margin-large-top"
      v-show="productsOrdered.length !== 0"
    >
      <UtilsButton :disabled="!valide">Commander</UtilsButton>
    </div>
  </section>
</template>

<script>
import { mapGetters, mapState } from 'vuex'

import UtilsButton from '@/components/Utils/UtilsButton'
import ProductOrderedItem from '@/components/Application/Order/Section/Order/ProductOrderedItem'

export default {
  name: 'ProductOrdered',
  computed: {
    ...mapState({
      productsOrdered: (state) => state.order.order
    }),
    ...mapGetters({
      valide: 'order/valide'
    }),
    price () {
      let price = 0
      this.productsOrdered.forEach((productOrdered) => {
        if (productOrdered.weight && productOrdered.amount) {
          price += productOrdered.weight.node.price * productOrdered.amount
        }
      })
      return price
    }
  },
  components: {
    ProductOrderedItem,
    UtilsButton
  }
}
</script>

<style lang="scss" scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.8s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
