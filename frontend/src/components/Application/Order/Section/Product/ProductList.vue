<template>
  <div>
    <form
      class="uk-form-horizontal uk-width-1-3@m uk-margin-large-bottom"
    >
      <label
        for="filter"
        class="uk-form-label"
      >Filtrer les produits</label>
      <div class="uk-form-controls">
        <select
          v-model="value"
          name="filter"
          class="uk-select"
        >
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
      <p class="uk-text-center uk-text-muted">
        Aucun produit disponible.
      </p>
    </div>
    <transition-group
      v-else
      name="fade"
      uk-grid
      class="uk-child-width-1-3@l uk-child-width-1-2@m uk-grid-match uk-grid-large uk-text-center uk-flex-center"
    >
      <div
        v-for="product in filterProduct"
        :key="product.node.id"
      >
        <ProductItem
          class="product-card"
          :product="product"
          @update-product="updateProduct"
        />
      </div>
    </transition-group>
    <ProductFormModal
      v-if="isAdmin"
      id="update-product"
      :product-update="productUpdate"
      :update="true"
    />
  </div>
</template>
<script>

import useApplication from '@/composition/application/useApplication'

import ProductItem from '@/components/Application/Order/Section/Product/ProductItem'
import ProductFormModal from '@/components/Application/Order/Section/Product/ProductFormModal'
import { computed, reactive, toRefs } from '@vue/composition-api'

export default {
    name: 'ProductList',
    components: {
        ProductItem,
        ProductFormModal
    },
    setup (props, { root }) {
        const { isAdmin, products } = useApplication(root.$route.params.application)
        const state = reactive({
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
            productUpdate: {}
        })

        const filterProduct = computed(() => {
            if (state.value === 'all') {
                return products.value
            }
            return products.value.filter(
                (product) => product.node[state.filter] === state.value
            )
        })

        const updateProduct = (product) => {
            state.productUpdate = product.node
            // eslint-disable-next-line no-undef
            UIkit.modal('#update-product').show()
        }

        return { ...toRefs(state), isAdmin, filterProduct, updateProduct }
    }
}
</script>
