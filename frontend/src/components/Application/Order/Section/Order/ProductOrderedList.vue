<template>
  <section>
    <div class="uk-text-center uk-margin-large-bottom uk-text-bold">
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
      <UtilsButton
        :disabled="!valide"
        @click="showModal('#sommaryModal')"
        >Commander</UtilsButton
      >
    </div>
    <ProductOrderedSommaryModal id="sommaryModal" />
  </section>
</template>

<script>
import { mapActions, mapGetters, mapState } from 'vuex'

import UtilsButton from '@/components/Utils/UtilsButton'
import ProductOrderedItem from '@/components/Application/Order/Section/Order/ProductOrderedItem'
import ProductOrderedSommaryModal from '@/components/Application/Order/Section/Order/ProductOrderedSommaryModal'

export default {
  name: 'ProductOrdered',
  props: {
    applicationId: {
      type: String,
      required: true
    }
  },
  components: {
    ProductOrderedItem,
    UtilsButton,
    ProductOrderedSommaryModal
  },
  computed: {
    ...mapState({
      productsOrdered: (state) => state.order.order
    }),
    ...mapGetters({
      valide: 'order/valide',
      price: 'order/totalPrice'
    })
  },
  methods: {
    ...mapActions({ saveOrder: 'order/saveOrder' }),
    showModal (modalId) {
      // eslint-disable-next-line no-undef
      UIkit.modal(modalId).show()
    }
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
