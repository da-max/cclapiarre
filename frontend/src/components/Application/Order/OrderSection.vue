<template>
  <div>
    <div class="uk-text-center">
      <a
        class="uk-button uk-button-secondary"
        v-show="isAdmin"
        :href="'/' + $route.params.application + '/recapitulatif'"
        >Générer le récapitulatif de la commande</a
      >
      <UtilsButton
        type="primary"
        class="uk-margin-medium-left"
        v-show="isAdmin"
        :to="{ name: 'ApplicationProductCreate' }"
        @click="showProductFormModal"
        >Ajouter un produit</UtilsButton
      >
    </div>
    <ProductFormModal />
    <OrderInformation class="uk-width-1-2@l uk-margin-auto" />
    <ProductOrderedList
      class="uk-margin-xlarge uk-width-4-5@l uk-margin-auto"
      id="order-list"
    />

    <ProductList />
  </div>
</template>

<script>
import useApplication from '@/composition/application/useApplication'

import OrderInformation from '@/components/Application/Order/Section/OrderInformation'
import ProductList from '@/components/Application/Order/Section/Product/ProductList'
import ProductOrderedList from '@/components/Application/Order/Section/Order/ProductOrderedList'
import ProductFormModal from '@/components/Application/Order/Section/Product/ProductFormModal'
import UtilsButton from '../../Utils/UtilsButton.vue'

export default {
  name: 'OrderSection',
  setup (props, { root }) {
    const { isAdmin } = useApplication(root.$route.params.application)
    // eslint-disable-next-line no-undef
    const showProductFormModal = () => UIkit.modal('#product-form-modal').show()
    return {
      isAdmin,
      showProductFormModal
    }
  },
  components: {
    ProductList,
    ProductOrderedList,
    OrderInformation,
    UtilsButton,
    ProductFormModal
  }
}
</script>
