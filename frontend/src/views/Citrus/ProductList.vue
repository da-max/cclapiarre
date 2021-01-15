<template>
  <main>
    <CitrusProductListHeader class="uk-width-3-5@m uk-margin-auto" />
    <div
      class="uk-width-2-5@l uk-width4-5@s uk-margin-auto uk-margin-large-bottom"
    >
      <Alerts />
    </div>
    <CitrusProductListSection />
  </main>
</template>

<script>
import { useSetupTitle } from '@/composition/useUtils'
import useCitrus from '@/composition/citrus/useCitrus'

import CitrusProductListHeader from '@/components/Citrus/ProductList/CitrusProductListHeader'
import CitrusProductListSection from '@/components/Citrus/ProductList/CitrusProductListSection'
import Alerts from '@/components/Utils/Alert/Alerts'

export default {
  components: {
    CitrusProductListHeader,
    CitrusProductListSection,
    Alerts
  },
  setup () {
    const { getCitrus } = useCitrus()
    getCitrus()
    useSetupTitle('Liste des produits')
  }
}
</script>
