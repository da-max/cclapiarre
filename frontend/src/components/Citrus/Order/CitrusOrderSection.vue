<template>
  <section>
    <header>
      <div class="uk-text-center">
        <UtilsButton
          type="secondary"
          width="large"
        >
          Générer le récapitulatif PDF de la commande
        </UtilsButton>
        <UtilsButton
          class="uk-margin-large-left"
          type="danger"
          width="large"
        >
          Supprimer toutes les commandes
        </UtilsButton>
      </div>
      <aside class="uk-margin-large-top uk-width-1-2@m uk-margin-auto">
        <OrderInformation />
        <div class="uk-text-center uk-margin-large-top uk-text-bold">
          <span class="uk-label">Prix actuel de la commande</span> {{ currentOrderPrice }} €
        </div>
      </aside>
    </header>
    <section>
      <CitrusOrderedTable class="uk-margin-xlarge-top" />
      <footer class="uk-text-center">
        <UtilsButton
          type="secondary"
          :disabled="!currentOrderValide"
          class="uk-margin-large-right"
          @click="useShowModal('#citrus-ordered-sommary')"
        >
          Récapitulatif de la commande
        </UtilsButton>
        <UtilsButton :disabled="!currentOrderValide">
          Valider ma commande
        </UtilsButton>
      </footer>
    </section>
    <CitrusOrderedSommary />
  </section>
</template>

<script>
import useCitrus from '@/composition/citrus/useCitrus'
import useOrder from '@/composition/citrus/useOrder'
import { useShowModal } from '@/composition/useUtils'

import CitrusOrderedTable from '@/components/Citrus/Order/Section/CitrusOrderedTable'
import OrderInformation from '@/components/Application/Order/Section/OrderInformation'
import UtilsButton from '@/components/Utils/UtilsButton'
import CitrusOrderedSommary from '@/components/Citrus/Order/Sommary/CitrusOrderSommary'

export default {
    name: 'CitrusOrderSection',
    components: {
        CitrusOrderedSommary,
        CitrusOrderedTable,
        OrderInformation,
        UtilsButton
    },
    setup () {
        const { getCitrus } = useCitrus()
        const { getOrders, currentOrderPrice, currentOrderValide } = useOrder()

        getCitrus()
        getOrders()

        return { currentOrderPrice, currentOrderValide, useShowModal }
    }
}
</script>
