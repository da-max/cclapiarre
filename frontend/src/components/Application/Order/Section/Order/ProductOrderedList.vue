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
      <div
        v-for="productOrdered in productsOrdered"
        :key="productOrdered.id"
      >
        <ProductOrderedItem :product-ordered="productOrdered" />
      </div>
    </transition-group>
    <div
      v-show="productsOrdered.length !== 0"
      class="uk-text-center uk-margin-large-top"
    >
      <UtilsButton
        :disabled="!valide"
        type="secondary"
        @click="showModal('#sommaryModal')"
      >
        Récapitulatif de la commande
      </UtilsButton>
      <UtilsButton
        class="uk-margin-large-left"
        :disabled="!valide"
        @click="addOrder"
      >
        Commander
      </UtilsButton>
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
      price: 'order/totalPrice',
      idApplicationBySlug: 'application/idApplicationBySlug'
    }),
    applicationId () {
      return this.idApplicationBySlug(this.$route.params.application)
    }
  },
  methods: {
    ...mapActions({ saveOrder: 'order/saveOrder' }),
    showModal (modalId) {
      // eslint-disable-next-line no-undef
      UIkit.modal(modalId).show()
    },
    async addOrder () {
      await this.saveOrder(this.applicationId)
    }
  }
}
</script>
