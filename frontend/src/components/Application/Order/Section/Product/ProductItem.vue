<template>
  <UtilsCard mediaPos="bottom">
    <template #media>
      <div class="uk-transition-toggle uk-inline-clip" tabindex="0">
        <img :src="'/media/' + product.node.image" alt="" />
        <div
          class="uk-transition-fade uk-position-cover uk-overlay uk-overlay-default uk-overflow-auto"
        >
          <div class="uk-text-center">
            <h5>Poids disponible</h5>
            <ul class="uk-list">
              <li
                v-for="weight in product.node.weights.edges"
                :key="weight.node.id"
              >
                {{ weight.node.weight }} {{ weight.node.unit }} pour
                {{ weight.node.price }} €
              </li>
            </ul>
          </div>
          <div v-if="product.node.options.edges.length !== 0">
            <h5>Options disponible</h5>
            <ul class="uk-list">
              <li
                v-for="option in product.node.options.edges"
                :key="option.node.id"
              >
                {{ option.node.name }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </template>
    <template #body>
      <h3 class="uk-card-title">{{ product.node.name }}</h3>
      <div v-html="product.node.description"></div>
    </template>
    <template #footer>
      <div class="uk-margin-medium-top">
        <UtilsButton @click="addProduct(product.node)" id="addProductButton"
          >Commander ce produit</UtilsButton
        >
      </div>
    </template>
  </UtilsCard>
</template>

<script>
import UtilsCard from '@/components/Utils/UtilsCard'
import UtilsButton from '@/components/Utils/UtilsButton'
import { mapMutations } from 'vuex'

export default {
  name: 'ProductItem',
  components: {
    UtilsCard,
    UtilsButton
  },
  props: {
    product: {
      required: true,
      type: Object
    }
  },
  methods: {
    ...mapMutations({ addProductOrder: 'order/ADD_PRODUCT_ORDER' }),
    addProduct (product) {
      // eslint-disable-next-line no-undef
      UIkit.scroll('#addProductButton', { offset: 100 }).scrollTo('#order-list')
      this.addProductOrder(product)
    }
  }
}
</script>
