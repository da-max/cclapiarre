<template>
  <main>
    <CoffeeOrderHeader />
    <div
      class="uk-width-2-5@l uk-width4-5@s uk-margin-auto uk-margin-large-bottom uk-margin-large-top"
    >
      <alert
        v-show="hasOrder"
        :header="true"
      >
        <template #header>
          Vous avez déjà commandé !
        </template>
        <template #body>
          <p>
            Une commande à votre nom a été trouvé.
          </p>
        </template>
      </alert>
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
import Alert from '@/components/Utils/Alert/Alert.vue'

export default {
    name: 'CoffeeOrder',
    components: {
        CoffeeOrderHeader,
        CoffeeOrderSection,
        Alerts,
        Alert
    },
    setup () {
        useSetupTitle('Commander du café')
        const { hasOrder, hasOrdered } = useCoffee()

        hasOrdered()
        return {
            hasOrder
        }
    }
}
</script>
