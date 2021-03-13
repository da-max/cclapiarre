<template>
  <UtilsCard media-pos="bottom">
    <template #media>
      <div
        v-if="product.node.image"
        class="uk-transition-toggle uk-inline-clip"
        tabindex="0"
      >
        <img
          :src="'/media/' + product.node.image"
          alt=""
        >
        <ProductItemInformation
          :weights="product.node.weights"
          :options="product.node.options"
          class="uk-transition-fade uk-position-cover uk-overlay uk-overlay-default uk-overflow-auto"
        />
      </div>
      <div v-else>
        <ProductItemInformation
          :weights="product.node.weights"
          :options="product.node.options"
        />
      </div>
    </template>
    <template #body>
      <h3
        :class="['uk-card-title', { 'uk-text-muted': !product.node.display }]"
      >
        {{ product.node.name }}
      </h3>
      <div v-html="product.node.description" />
    </template>
    <template #footer>
      <div
        v-if="product.node.display"
        class="uk-margin-medium-top"
      >
        <UtilsButton
          id="addProductButton"
          class="uk-margin-medium-bottom"
          @click="addProductOrder(product.node)"
        >
          Commander ce produit
        </UtilsButton>
        <UtilsButton
          v-if="isAdmin"
          type="text"
          @click="updateProduct"
        >
          Modifier le produit
        </UtilsButton>
      </div>
      <div
        v-else
        class="uk-text-center"
      >
        <p class="uk-text-muted">
          Produit non disponible à la commande
        </p>
        <UtilsButton
          v-show="isAdmin"
          type="text"
          @click="updateProduct"
        >
          Modifier le produit
        </UtilsButton>
      </div>
    </template>
  </UtilsCard>
</template>

<script>
import useApplication from '@/composition/application/useApplication'
import useOrder from '@/composition/application/useOrder'

import UtilsCard from '@/components/Utils/UtilsCard'
import UtilsButton from '@/components/Utils/UtilsButton'
import ProductItemInformation from '@/components/Application/Order/Section/Product/ProductItemInformation'

export default {
    name: 'ProductItem',
    components: {
        UtilsCard,
        UtilsButton,
        ProductItemInformation
    },
    props: {
        product: {
            required: true,
            type: Object
        }
    },
    setup (props, { emit, root }) {
        const { isAdmin } = useApplication(root.$route.params.application)

        const { addProductOrder } = useOrder()

        const updateProduct = () => {
            emit('update-product', props.product)
        }
        return { isAdmin, addProductOrder, updateProduct }
    }
}
</script>
