<template>
  <main>
    <CitrusOrderHeader />
    <div
      class="uk-width-2-5@l uk-width4-5@s uk-margin-auto uk-margin-large-bottom"
    >
      <Alerts />
      <Alert
        v-show="hasOrder"
        :alert-id="Date.now()"
        :header="true"
        type="primary"
      >
        <template #header>
          Vous avez commandé
        </template>
        <template #body>
          Vous avez commandé, si vous souhaitez modifier votre commande
          merci de contacter la responsable des commandes à cette
          adresse : valerie.lechateau@gmail.com
        </template>
      </Alert>
    </div>
    <CitrusOrderSection />
  </main>
</template>

<script>
import { useSetupTitle } from '@/composition/useUtils'
import useOrder from '@/composition/citrus/useOrder'

import Alerts from '@/components/Utils/Alert/Alerts'
import CitrusOrderHeader from '@/components/Citrus/Order/CitrusOrderHeader'
import CitrusOrderSection from '@/components/Citrus/Order/CitrusOrderSection'
import Alert from '../../components/Utils/Alert/Alert.vue'

export default {
    name: 'Order',
    components: {
        Alert,
        Alerts,
        CitrusOrderHeader,
        CitrusOrderSection
    },
    setup () {
        useSetupTitle('Commander des agrumes')
        const { hasOrder } = useOrder()
        return { hasOrder }
    }
}
</script>
