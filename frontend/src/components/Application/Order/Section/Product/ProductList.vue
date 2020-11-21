<template>
  <div>
    <form
      class="uk-form-horizontal uk-width-1-3@m uk-margin-large-bottom"
      v-if="isAdmin($route.params.application)"
    >
      <label for="filter" class="uk-form-label">Filtrer les produits</label>
      <div class="uk-form-controls">
        <select name="filter" class="uk-select" v-model="value">
          <option
            v-for="(val, text) in FILTERS"
            :key="val.value"
            :value="val.value"
          >
            {{ text }}
          </option>
        </select>
      </div>
    </form>
    <div v-if="filterProduct.length === 0">
      <p class="uk-text-center uk-text-muted">Aucun produit disponible.</p>
    </div>
    <transition-group
      v-else
      name="fade"
      uk-grid
      class="uk-child-width-1-3@l uk-child-width-1-2@m uk-grid-match uk-grid-large uk-text-center uk-flex-center"
    >
      <div v-for="product in filterProduct" :key="product.node.id">
        <ProductItem
          class="product-card"
          :product="product"
          @update-product="updateProduct"
        />
      </div>
    </transition-group>
    <ProductUpdateModal
      id="updateProduct"
      :product="productUpdate"
      v-if="isAdmin($route.params.application)"
    ></ProductUpdateModal>
  </div>
</template>
<script>
import { mapGetters, mapState } from 'vuex'

import ProductItem from '@/components/Application/Order/Section/Product/ProductItem'
import ProductUpdateModal from '@/components/Application/Order/Section/Product/ProductUpdateModal'

export default {
  name: 'ProductList',
  data () {
    return {
      filter: 'display',
      value: true,
      FILTERS: {
        'Afficher les produits disponibles à la commande': {
          filter: 'display',
          value: true
        },
        'Afficher les produits cachés': {
          filter: 'display',
          value: false
        },
        'Afficher tout les produits': {
          filter: 'display',
          value: 'all'
        }
      },
      productUpdate: this.products[0].node
    }
  },
  props: {
    products: {
      type: Array,
      required: true
    }
  },
  components: {
    ProductItem,
    ProductUpdateModal
  },
  computed: {
    ...mapGetters({ application: 'application/applicationBySlug', isAdmin: 'application/isAdmin' }),
    ...mapState({ loading: (state) => state.loading }),
    filterProduct () {
      if (this.value === 'all') {
        return this.products
      }
      return this.products.filter(
        (product) => product.node[this.filter] === this.value
      )
    }
  },
  methods: {
    updateFilter (event) {
      console.log(event.target.value)
    },
    updateProduct (product) {
      this.productUpdate = product.node
      // eslint-disable-next-line no-undef
      UIkit.modal('#updateProduct').show()
    }
  }
}
</script>
