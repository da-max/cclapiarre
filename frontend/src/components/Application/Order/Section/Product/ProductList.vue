<template>
  <div>
    <form
      class="uk-form-horizontal uk-width-1-3@m uk-margin-large-bottom"
      v-if="isAdmin"
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
      <transition-group
        name="fade"
        uk-grid
        class="uk-child-width-1-3@l uk-child-width-1-2@m uk-grid-match uk-grid-large uk-text-center uk-flex-center"
      >
        <div v-for="product in filterProduct" :key="product.node.id">
          <ProductItem class="product-card" :product="product" />
        </div>
      </transition-group>
    </div>
</template>
<script>
import ProductItem from '@/components/Application/Order/Section/Product/ProductItem'
import { mapGetters } from 'vuex'
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
      }
    }
  },
  props: {
    products: {
      type: Array,
      required: true
    }
  },
  components: {
    ProductItem
  },
  computed: {
    ...mapGetters({ application: 'application/applicationBySlug' }),
    filterProduct () {
      if (this.value === 'all') {
        return this.products
      }
      return this.products.filter(
        (product) => product.node[this.filter] === this.value
      )
    },
    isAdmin () {
      return !!this.application(this.$route.params.application).admins.find(
        (admin) => admin.id === this.$store.state.auth.currentUser.id
      )
    }
  },
  methods: {
    updateFilter (event) {
      console.log(event.target.value)
    }
  }
}
</script>
