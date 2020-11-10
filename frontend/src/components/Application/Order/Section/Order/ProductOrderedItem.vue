<template>
  <UtilsCard>
    <template #header>
      <h3 class="uk-card-title uk-text-center">
        {{ productOrdered.product.name }}
      </h3>
    </template>
    <template #body>
      <form class="uk-form-horizontal">
        <div>
          <label for="weight" class="uk-form-label">Poids du produit</label>
          <div class="uk-form-controls">
            <select
              name="weight"
              class="uk-select"
              @input="selectWeight"
              :disabled="productOrdered.product.weights.edges.length === 1"
            >
              <option
                v-for="weight in productOrdered.product.weights.edges"
                :key="weight.node.id"
                :value="weight.node.id"
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
            <select name="option" class="uk-select" @input="selectOption">
              <option selected>Sélectionner une option</option>
              <option
                :value="option.node.id"
                v-for="option in productOrdered.product.options.edges"
                :key="option.node.id"
              >
                {{ option.node.name }}
              </option>
            </select>
          </div>
        </div>
        <div class="uk-margin-medium-top">
          <FormInput
            label="Quantité"
            name="amount"
            type="number"
            :value="productOrdered.amount"
            min="0"
            @input="changeAmount"
          />
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
</template>

<script>
import UtilsCard from '@/components/Utils/UtilsCard'
import UtilsButton from '@/components/Utils/UtilsButton'
import FormInput from '@/components/Utils/Form/FormInput'
import { mapGetters, mapMutations } from 'vuex'

export default {
  name: 'ProductOrderedItem',
  props: {
    productOrdered: {
      required: true,
      type: Object
    }
  },
  computed: {
    ...mapGetters({ productById: 'order/productById' })
  },
  components: {
    UtilsCard,
    UtilsButton,
    FormInput
  },
  methods: {
    ...mapMutations({
      removeProductOrdered: 'order/REMOVE_PRODUCT_ORDER',
      setWeight: 'order/SET_WEIGHT',
      setOption: 'order/SET_OPTION',
      setAmount: 'order/SET_AMOUNT'
    }),
    selectWeight (event) {
      const weight = this.productById(
        this.productOrdered.id
      ).product.weights.edges.find(
        (weight) => weight.node.id === event.target.value
      )
      this.setWeight({ id: this.productOrdered.id, weight })
    },
    selectOption (event) {
      const option = this.productById(
        this.productOrdered.id
      ).product.options.edges.find(
        (option) => option.node.id === event.target.value
      )
      this.setOption({ id: this.productOrdered.id, option })
    },
    changeAmount (amount) {
      this.setAmount({ id: this.productOrdered.id, amount })
    }
  }
}
</script>
