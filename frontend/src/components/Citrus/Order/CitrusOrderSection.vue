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
      <OrderInformation class="uk-margin-large-top uk-width-1-2@m uk-margin-auto" />
    </header>
    <section>
      <CitrusOrderTable class="uk-margin-xlarge-top" />
    </section>
  </section>
</template>

<script>
import useCitrus from '@/composition/citrus/useCitrus'

import CitrusOrderTable from '@/components/Citrus/Order/Section/CitrusOrderTable'
import OrderInformation from '@/components/Application/Order/Section/OrderInformation'
import UtilsButton from '@/components/Utils/UtilsButton'

export default {
  name: 'CitrusOrderSection',
  components: {
    CitrusOrderTable,
    OrderInformation,
    UtilsButton
  },
  setup () {
    const { getCitrus } = useCitrus()
    getCitrus()
  }
}
</script>
