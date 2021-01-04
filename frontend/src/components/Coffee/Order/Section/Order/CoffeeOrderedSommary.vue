<template>
  <UtilsModal
    :container="true"
    :center="true"
  >
    <template #header>
      <h2 class="uk-modal-title">
        Récapitulatif de la commande
      </h2>
    </template>
    <template #body>
      <OrderInformation />
      <p class="uk-text-center uk-margin-large-bottom uk-text-bold">
        <span class="uk-label">Prix de votre commande</span> {{ price }} €
      </p>
      <utils-table>
        <template #head>
          <th>Café</th>
          <th>Poids</th>
          <th>Type de mouture</th>
          <th>Quantité</th>
          <th>Prix</th>
          <th>Supprimer</th>
        </template>
        <template
          v-if="Object.keys(coffeesOrder).length === 0"
          #body
        >
          <tr>
            <td>
              Aucun café n’a été commandé
            </td>
            <td />
            <td />
            <td />
            <td />
            <td />
          </tr>
        </template>
        <template
          v-else
          #body
        >
          <tr
            v-for="coffeeOrder in coffeesOrder"
            :key="coffeeOrder.id"
          >
            <td>{{ coffeeOrder.coffee.farmCoop }}</td>
            <td v-if="coffeeOrder.weight === 200">
              200 grammes
            </td>
            <td v-else>
              1 kilogramme
            </td>
            <td>{{ coffeeOrder.type ? coffeeOrder.type.name : '' }}</td>
            <td>
              <input
                type="number"
                name="amount"
                class="uk-input uk-form-width-small salut"
                :value="coffeeOrder.amount"
                @change="(ev) => setAmount(coffeeOrder.id, ev.target.value)"
              >
            </td>
            <td>{{ uniqPrice(coffeeOrder.id) }} €</td>
            <td>
              <UtilsButton
                width="small"
                type="danger"
                @click="removeCoffeeOrder(coffeeOrder.id)"
              >
                Supprimer
              </UtilsButton>
            </td>
          </tr>
        </template>
      </utils-table>
    </template>
    <template #footer>
      <div class="uk-text-center">
        <UtilsButton
          class="uk-margin-medium-right uk-modal-close"
          type="secondary"
        >
          Annuler
        </UtilsButton>
        <UtilsButton
          v-show="Object.keys(coffeesOrder).length !== 0"
          :disabled="!valide"
          @click="saveOrder"
        >
          Commander
        </UtilsButton>
      </div>
    </template>
  </UtilsModal>
</template>

<script>
import useCoffee from '@/composition/coffee/useCoffee'

import UtilsModal from '@/components/Utils/UtilsModal.vue'
import UtilsTable from '@/components/Utils/UtilsTable.vue'
import UtilsButton from '@/components/Utils/UtilsButton.vue'
import OrderInformation from '@/components/Application/Order/Section/OrderInformation.vue'

export default {
  name: 'CoffeeOrderedSommary',
  components: { UtilsModal, UtilsTable, UtilsButton, OrderInformation },
  setup () {
    const {
      coffeesOrder,
      uniqPrice,
      setAmount,
      removeCoffeeOrder,
      saveOrder: save,
      valide,
      price
    } = useCoffee()

    const saveOrder = () => {
      // eslint-disable-next-line no-undef
      UIkit.modal('#sommary-modal').hide()
      save()
    }

    return {
      coffeesOrder,
      uniqPrice,
      setAmount,
      removeCoffeeOrder,
      saveOrder,
      valide,
      price
    }
  }
}
</script>
