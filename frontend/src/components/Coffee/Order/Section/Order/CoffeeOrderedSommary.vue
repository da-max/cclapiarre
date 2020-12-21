<template>
  <UtilsModal :container="true" :center="true">
    <template #header>
      <h2 class="uk-modal-title">Récapitulatif de la commande</h2>
    </template>
    <template #body>
      <utils-table>
        <template #head>
          <th>Café</th>
          <th>Poids</th>
          <th>Type de mouture</th>
          <th>Quantité</th>
          <th>Prix</th>
          <th>Supprimer</th>
        </template>
        <template #body v-if="Object.keys(coffeesOrder).length === 0">
          <tr>
            <td>
              Aucun café n’a été commandé
            </td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
          </tr>
        </template>
        <template #body v-else>
          <tr v-for="coffeeOrder in coffeesOrder" :key="coffeeOrder.id">
            <td>{{ coffeeOrder.coffee.farmCoop }}</td>
            <td v-if="coffeeOrder.weight === 200">200 grammes</td>
            <td v-else>1 kilogramme</td>
            <td>{{ coffeeOrder.type ? coffeeOrder.type.name : '' }}</td>
            <td>
              <input
                type="number"
                name="amount"
                class="uk-input uk-form-width-small salut"
                :value="coffeeOrder.amount"
                @change="(ev) => setAmount(coffeeOrder.id, ev.target.value)"
              />
            </td>
            <td>{{ uniqPrice(coffeeOrder.id) }} €</td>
            <td>
              <UtilsButton
                width="small"
                type="danger"
                @click="removeCoffeeOrder(coffeeOrder.id)"
                >Supprimer</UtilsButton
              >
            </td>
          </tr>
        </template>
      </utils-table>
    </template>
  </UtilsModal>
</template>

<script>
import useCoffee from '@/composition/coffee/useCoffee'

import UtilsModal from '@/components/Utils/UtilsModal.vue'
import UtilsTable from '@/components/Utils/UtilsTable.vue'
import UtilsButton from '@/components/Utils/UtilsButton.vue'

export default {
  name: 'CoffeeOrderedSommary',
  components: { UtilsModal, UtilsTable, UtilsButton },
  setup () {
    const {
      coffeesOrder,
      uniqPrice,
      setAmount,
      removeCoffeeOrder
    } = useCoffee()

    return { coffeesOrder, uniqPrice, setAmount, removeCoffeeOrder }
  }
}
</script>
