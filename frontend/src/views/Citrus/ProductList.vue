<template>
  <main>
    <CitrusProductListHeader class="uk-width-3-5@m uk-margin-auto" />
    <CitrusProductListSection />
  </main>
</template>

<script>
import { useSetupTitle } from '@/composition/useUtils'
import useCitrus from '@/composition/citrus/useCitrus'

import CitrusProductListHeader from '@/components/Citrus/ProductList/CitrusProductListHeader'
import CitrusProductListSection from '@/components/Citrus/ProductList/CitrusProductListSection'

export default {
  components: {
    CitrusProductListHeader,
    CitrusProductListSection
  },
  setup () {
    const { getCitrus } = useCitrus()
    getCitrus()
    useSetupTitle('Liste des produits')
  }
}
</script>
