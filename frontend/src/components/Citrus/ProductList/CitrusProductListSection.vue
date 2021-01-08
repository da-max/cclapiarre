<template>
  <section class="uk-margin-medium-top uk-width-3-4@m uk-margin-auto">
    <header class="uk-margin-large-bottom">
      <FormSearch
        placeholder="Rechercher un produit"
        :elements="citrus"
        :keys="searchKeys"
        @fuseResultsUpdated="(result) => setSearchCitrus(result)"
      />
    </header>

    <div>
      <ProductListTable />
    </div>
  </section>
</template>

<script>
import { reactive, toRefs } from '@vue/composition-api'

import useCitrus from '@/composition/citrus/useCitrus'

import FormSearch from '@/components/Utils/Form/FormSearch'
import ProductListTable from '@/components/Citrus/ProductList/Table/ProductListTable'

export default {
  components: {
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
