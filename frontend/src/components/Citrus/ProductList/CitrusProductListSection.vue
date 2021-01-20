<template>
  <section class="uk-margin-medium-top uk-width-3-4@m uk-margin-auto">
    <header class="uk-margin-large-bottom uk-flex uk-flex-between">
      <div>
        <FormSearch
          placeholder="Rechercher un produit"
          :elements="citrus"
          :keys="searchKeys"
          @fuseResultsUpdated="(result) => setSearchCitrus(result)"
        />
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

import FormSearch from '@/components/Utils/Form/FormSearch'
import ProductListTable from '@/components/Citrus/ProductList/Table/ProductListTable'
import CitrusProductListActions from '@/components/Citrus/ProductList/CitrusProductListActions'
import CitrusProductModal from '@/components/Citrus/ProductList/CitrusProductModal'
import CitrusProductDelete from '@/components/Citrus/ProductList/CitrusProductDelete'

export default {
    components: {
        CitrusProductDelete,
        CitrusProductListActions,
        CitrusProductModal,
        FormSearch,
        ProductListTable
    },
    setup () {
        const state = reactive({
            searchKeys: ['node.name', 'node.description']

        })

        const { citrus, searchCitrus, setSearchCitrus } = useCitrus()

        return {
            ...toRefs(state),
            citrus,
            setSearchCitrus,
            searchCitrus
        }
    }
}
</script>
