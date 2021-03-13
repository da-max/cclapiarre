<template>
  <main>
    <CitrusOrderHeader />
    <div
      class="uk-width-2-5@l uk-width4-5@s uk-margin-auto uk-margin-large-bottom uk-margin-large-top"
    >
      <Alerts />
      <Alert
        v-show="hasOrder"
        :alert-id="Date.now()"
        :header="true"
        status="primary"
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
      <Alert
        v-if="currentOrderNumberCase > MAX_CASE_ORDERED"
        :alert-id="Date.now()"
        :header="true"
        status="warning"
      >
        <template #header>
          Nombre de caisses trop important
        </template>
        <template #body>
          Le nombre de caisse que vous avez commandé est trop
          important, en effet, il est limité à {{ MAX_CASE_ORDERED }},
          merci de modifier votre commande afin qu’elle respecte cette condition.
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
import Alert from '@/components/Utils/Alert/Alert.vue'

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
        const {
            currentOrderNumberCase,
            hasOrder,
            MAX_CASE_ORDERED
        } = useOrder()
        return {
            currentOrderNumberCase,
            hasOrder,
            MAX_CASE_ORDERED
        }
    }
}
</script>
