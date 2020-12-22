<template>
  <main>
    <CoffeeOrderHeader />
    <div
      class="uk-width-2-5@l uk-width4-5@s uk-margin-auto uk-margin-large-bottom"
    >
      <Alerts />
    </div>
    <CoffeeOrderSection />
  </main>
</template>

<script>
import { useSetupTitle } from '@/composition/useUtils'
import useCoffee from '@/composition/coffee/useCoffee'

import Alerts from '@/components/Utils/Alert/Alerts'
import CoffeeOrderHeader from '@/components/Coffee/Order/CoffeeOrderHeader.vue'
import CoffeeOrderSection from '@/components/Coffee/Order/CoffeeOrderSection'

export default {
  name: 'CoffeeOrder',
  components: {
    CoffeeOrderHeader,
    CoffeeOrderSection,
    Alerts
  },
  setup () {
    useSetupTitle('Commander du café')
    const { hasOrdered } = useCoffee()

    hasOrdered()
  }
}
</script>
