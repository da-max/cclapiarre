<template>
  <section class="uk-margin-medium-top uk-width-3-4@l uk-margin-auto">
    <header
      class="uk-margin-large-bottom uk-flex uk-flex-between"
      uk-grid
    >
      <div class="uk-width-1-1 uk-text-center uk-hidden@l">
        <UtilsButton
          type="primary"
          @click="showCitrusProductModal"
        >
          Ajouter un produit
        </UtilsButton>
      </div>
      <div>
        <FormSearch
          placeholder="Rechercher un produit"
          :elements="citrus"
          :keys="searchKeys"
          @fuseResultsUpdated="(result) => setSearchCitrus(result)"
        />
      </div>
      <div class="uk-visible@l">
        <UtilsButton
          type="primary"
          @click="showCitrusProductModal"
        >
          Ajouter un produit
        </UtilsButton>
      </div>
      <div>
        <CitrusProductListActions />
      </div>
    </header>
    <ProductListTable />
    <CitrusProductModal id="citrus-product-modal" />
    <CitrusProductDelete id="citrus-product-delete" />
  </section>
</template>

<script>
import { reactive, toRefs } from '@vue/composition-api'

import useCitrus from '@/composition/citrus/useCitrus'
import { useShowModal } from '@/composition/useUtils'

import FormSearch from '@/components/Utils/Form/FormSearch'
import ProductListTable from '@/components/Citrus/ProductList/Table/ProductListTable'
import CitrusProductListActions from '@/components/Citrus/ProductList/CitrusProductListActions'
import CitrusProductModal from '@/components/Citrus/ProductList/CitrusProductModal'
import CitrusProductDelete from '@/components/Citrus/ProductList/CitrusProductDelete'
import UtilsButton from '@/components/Utils/UtilsButton.vue'

export default {
    components: {
        CitrusProductDelete,
        CitrusProductListActions,
        CitrusProductModal,
        FormSearch,
        ProductListTable,
        UtilsButton
    },
    setup () {
        const state = reactive({
            searchKeys: ['node.name', 'node.description']

        })

        const {
            clearSelectCitrus,
            citrus,
            searchCitrus, setSearchCitrus
        } = useCitrus()

        const showCitrusProductModal = () => {
            clearSelectCitrus()
            useShowModal('#citrus-product-modal')
        }

        return {
            ...toRefs(state),
            citrus,
            setSearchCitrus,
            searchCitrus,
            showCitrusProductModal
        }
    }
}
</script>
