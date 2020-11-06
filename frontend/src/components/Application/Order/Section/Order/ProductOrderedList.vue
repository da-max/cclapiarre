<template>
  <section>
    <div uk-grid class="uk-flex-center uk-child-width-1-2@l">
      <transition-group name="fade">
        <div v-for="productOrdered in productsOrdered" :key="productOrdered.id">
          <UtilsCard>
            <template #header>
              <h3 class="uk-card-title uk-text-center">
                {{ productOrdered.product.name }}
              </h3>
            </template>
            <template #body>
              <form class="uk-form-horizontal">
                <div>
                  <label for="weight" class="uk-form-label"
                    >Poids du produit</label
                  >
                  <div class="uk-form-controls">
                    <select
                      name="weight"
                      class="uk-select"
                      :disabled="
                        productOrdered.product.weights.edges.length === 1
                      "
                    >
                      <option
                        v-for="weight in productOrdered.product.weights.edges"
                        :key="weight.node.id"
                        :value="weight.node.weight"
                      >
                        {{ weight.node.weight }} {{ weight.node.unit }} pour
                        {{ weight.node.price }} €
                      </option>
                    </select>
                  </div>
                </div>
                <div
                  class="uk-margin-medium-top"
                  v-if="productOrdered.product.options.edges.length !== 0"
                >
                  <label for="option" class="uk-form-label"
                    >Option pour ce produit</label
                  >
                  <div class="uk-form-controls">
                    <select name="option" class="uk-select">
                      <option
                        :value="option.name"
                        v-for="option in productOrdered.product.options.edges"
                        :key="option.node.id"
                      >
                        {{ option.node.name }}
                      </option>
                    </select>
                  </div>
                </div>
              </form>
            </template>
            <template #footer>
              <div class="uk-text-center">
                <UtilsButton
                  @click="removeProductOrdered(productOrdered.id)"
                  type="danger"
                  >Supprimer</UtilsButton
                >
              </div>
            </template>
          </UtilsCard>
        </div>
      </transition-group>
    </div>
  </section>
</template>

<script>
import { mapMutations, mapState } from 'vuex'

import UtilsButton from '@/components/Utils/UtilsButton'
import UtilsCard from '@/components/Utils/UtilsCard'

export default {
  name: 'ProductOrdered',
  computed: {
    ...mapState({
      productsOrdered: (state) => state.order.order
    })
  },
  components: {
    UtilsCard,
    UtilsButton
  },
  methods: {
    ...mapMutations({ removeProductOrdered: 'order/REMOVE_PRODUCT_ORDER' })
  }
}
</script>

<style lang="scss" scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity .8s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}
</style>
