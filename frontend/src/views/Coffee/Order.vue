<template>
    <main>
      <CoffeeOrderHeader />
      <CoffeeOrderSection />
    </main>
</template>

<script>
import { useSetupTitle } from '@/composition/useUtils'

import CoffeeOrderHeader from '@/components/Coffee/Order/CoffeeOrderHeader.vue'
import CoffeeOrderSection from '@/components/Coffee/Order/CoffeeOrderSection'

export default {
  name: 'CoffeeOrder',
  components: {
    CoffeeOrderHeader,
    CoffeeOrderSection
  },
  setup () {
    useSetupTitle('Commander du café')
  }
}
</script>
