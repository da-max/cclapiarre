<template>
  <main>
    <CoffeeOrderListHeader />
    <div
      class="uk-width-2-5@l uk-width4-5@s uk-margin-auto uk-margin-large-bottom"
    >
      <Alerts />
    </div>
    <CoffeeOrderListSection />
  </main>
</template>

<script>
import { useSetupTitle } from '@/composition/useUtils'

import Alerts from '@/components/Utils/Alert/Alerts'
import CoffeeOrderListHeader from '@/components/Coffee/OrderList/CoffeeOrderListHeader'
import CoffeeOrderListSection from '@/components/Coffee/OrderList/CoffeeOrderListSection.vue'

export default {
    name: 'CoffeeOrderList',
    components: {
        Alerts,
        CoffeeOrderListHeader,
        CoffeeOrderListSection
    },
    setup () {
        useSetupTitle('Liste des commandes')
    }
}
</script>
