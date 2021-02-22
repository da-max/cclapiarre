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
          :disabled="ordersLength <= 0"
          type="danger"
          width="large"
          @click="useShowModal('#citrus-orders-delete-all-modal')"
        >
          Supprimer toutes les commandes
        </UtilsButton>
      </div>
      <aside class="uk-margin-large-top uk-width-1-2@m uk-margin-auto">
        <OrderInformation />
        <div class="uk-text-center uk-margin-large-top uk-text-bold">
          <div class="uk-margin-bottom">
            <label
              for="send-mail"
              class="uk-label uk-margin-medium-right"
            >Envoyer un mail récapitulatif</label>
            <input
              id="send-mail"
              v-model="computeSendMail"
              type="checkbox"
              name="send-mail"
              class="uk-checkbox"
            >
          </div>
          <span class="uk-label">Prix actuel de la commande</span> {{ currentOrderPrice }} €
        </div>
      </aside>
    </header>
    <section>
      <div class="uk-margin-medium-top uk-margin-left">
        <select
          id="display-orders"
          class="uk-select uk-form-width-large"
          @input="(e) => setDisplayOrders(Boolean(Number(e.target.value)))"
        >
          <option
            :value="0"
            :selected="displayOrders === false"
          >
            Cacher les commandes
          </option>
          <option
            :value="1"
            :selected="displayOrders === true"
          >
            Afficher les commandes
          </option>
        </select>
      </div>
      <CitrusOrderedTable class="uk-margin-large-top" />
      <footer
        v-show="!displayOrders"
        class="uk-text-center"
      >
        <UtilsButton
          type="secondary"
          :disabled="!currentOrderValide"
          class="uk-margin-large-right"
          @click="useShowModal('#citrus-ordered-sommary')"
        >
          Récapitulatif de la commande
        </UtilsButton>
        <UtilsButton
          :disabled="!currentOrderValide"
          @click="saveOrder"
        >
          Valider ma commande
        </UtilsButton>
      </footer>
    </section>
    <CitrusOrdersDeleteAllModal />
    <CitrusOrderedSommary />
  </section>
</template>

<script>
import { computed } from '@vue/composition-api'
import useCitrus from '@/composition/citrus/useCitrus'
import useOrder from '@/composition/citrus/useOrder'
import { useShowModal } from '@/composition/useUtils'

import CitrusOrderedTable from '@/components/Citrus/Order/Section/CitrusOrderedTable'
import CitrusOrderedSommary from '@/components/Citrus/Order/Sommary/CitrusOrderSommary'
import CitrusOrdersDeleteAllModal from '@/components/Citrus/Order/Section/CitrusOrdersDeleteAllModal'
import OrderInformation from '@/components/Application/Order/Section/OrderInformation'
import UtilsButton from '@/components/Utils/UtilsButton'

export default {
    name: 'CitrusOrderSection',
    components: {
        CitrusOrderedSommary,
        CitrusOrderedTable,
        CitrusOrdersDeleteAllModal,
        OrderInformation,
        UtilsButton
    },
    setup () {
        const { getCitrus } = useCitrus()
        const {
            currentOrderPrice,
            currentOrderValide,
            deleteAllOrders,
            displayOrders,
            getOrders,
            ordersLength,
            saveOrder,
            sendMail,
            setDisplayOrders,
            setSendMail
        } = useOrder()

        const computeSendMail = computed({
            get: () => sendMail,
            set: (newValue) => setSendMail(newValue)
        })

        getCitrus()
        getOrders()

        return {
            computeSendMail,
            currentOrderPrice,
            currentOrderValide,
            deleteAllOrders,
            displayOrders,
            ordersLength,
            saveOrder,
            setDisplayOrders,
            useShowModal
        }
    }
}
</script>
