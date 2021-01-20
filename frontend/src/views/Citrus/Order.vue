<template>
  <main>
    <CitrusOrderHeader />
    <div
      class="uk-width-2-5@l uk-width4-5@s uk-margin-auto uk-margin-large-bottom"
    >
      <Alerts />
    </div>
    <CitrusOrderSection />
  </main>
</template>

<script>
import { useSetupTitle } from '@/composition/useUtils'

import Alerts from '@/components/Utils/Alert/Alerts'
import CitrusOrderHeader from '@/components/Citrus/Order/CitrusOrderHeader'
import CitrusOrderSection from '@/components/Citrus/Order/CitrusOrderSection'

export default {
    name: 'Order',
    components: {
        Alerts,
        CitrusOrderHeader,
        CitrusOrderSection
    },
    setup () {
        useSetupTitle('Commander des agrumes')
    }
}
</script>
