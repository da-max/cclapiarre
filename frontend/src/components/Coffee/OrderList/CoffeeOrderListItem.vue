<template>
  <UtilsCard>
    <template #header>
      <div class="uk-flex uk-flex-center uk-grid-large">
        <div>
          <span class="uk-label">Prénom</span>
          {{ order.node.user.firstName || 'Non défini' }}
        </div>
        <div>
          <span class="uk-label">Nom</span>
          {{ order.node.user.lastName || 'Non défini' }}
        </div>
        <div>
          <span class="uk-label">Email</span> {{ order.node.user.email }}
        </div>
        <div>
          <span class="uk-label">Prix total</span>
          {{ totalPrice }}€
        </div>
      </div>
    </template>
    <template #body>
      <ul class="uk-list uk-list-striped">
        <li
          v-for="amount in order.node.amounts.edges"
          :key="amount.node.id"
          class="uk-flex uk-flex-between"
        >
          <div>
            <UtilsButton
              type="text"
              @click="$emit('display-details', amount.node.coffee)"
            >
              {{ amount.node.coffee.farmCoop }}
            </UtilsButton>
            ({{ amount.node.sort.name }})
          </div>
          <div>
            {{
              amount.node.weight === 'A_200' ? '200 grammes' : '1 kilogramme'
            }}
            ×
            {{ amount.node.amount }} =
            {{
              amount.node.weight === 'A_200'
                ? amount.node.amount * amount.node.coffee.twoHundredGramPrice
                : amount.node.amount * amount.node.coffee.kilogramPrice
            }}€
          </div>
        </li>
      </ul>
    </template>
    <template #footer>
      <div class="uk-flex uk-flex-center">
        <UtilsButton
          v-show="canDeleteOrder"
          type="danger"
          @click="$emit('confirm-remove', order)"
        >
          Supprimer
        </UtilsButton>
      </div>
    </template>
  </UtilsCard>
</template>

<script>
import { computed } from '@vue/composition-api'
import useCoffee from '@/composition/coffee/useCoffee'

import UtilsCard from '@/components/Utils/UtilsCard.vue'
import UtilsButton from '@/components/Utils/UtilsButton.vue'

export default {
    name: 'CoffeeOrderListItem',
    components: {
        UtilsCard,
        UtilsButton
    },
    props: {
        order: {
            required: true,
            type: Object
        }
    },
    setup (props) {
        const { canDeleteOrder } = useCoffee()

        const totalPrice = computed(() => {
            let price = 0
            props.order.node.amounts.edges.forEach((amount) => {
                if (amount.node.weight === 'A_200') {
                    price += amount.node.amount * amount.node.coffee.twoHundredGramPrice
                } else {
                    price += amount.node.amount * amount.node.coffee.kilogramPrice
                }
            })
            return price
        })

        return {
            canDeleteOrder,
            totalPrice
        }
    }
}
</script>
