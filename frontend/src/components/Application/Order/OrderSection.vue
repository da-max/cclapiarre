<template>
  <div>
    <div class="uk-text-center uk-margin-medium-bottom">
      <a
        v-show="isAdmin"
        class="uk-button uk-button-secondary"
        :href="'/' + $route.params.application + '/recapitulatif'"
      >Générer le récapitulatif de la commande</a>
      <UtilsButton
        v-show="isAdmin"
        type="primary"
        class="uk-margin-medium-left"
        @click="showProductFormModal"
      >
        Ajouter un produit
      </UtilsButton>
    </div>
    <ProductFormModal />
    <OrderInformation class="uk-width-1-2@l uk-margin-auto" />
    <ProductOrderedList
      id="order-list"
      class="uk-margin-xlarge uk-width-4-5@l uk-margin-auto"
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
  components: {
    ProductList,
    ProductOrderedList,
    OrderInformation,
    UtilsButton,
    ProductFormModal
  },
  setup (props, { root }) {
    const { isAdmin } = useApplication(root.$route.params.application)
    // eslint-disable-next-line no-undef
    const showProductFormModal = () => UIkit.modal('#product-form-modal').show()
    return {
      isAdmin,
      showProductFormModal
    }
  }
}
</script>
