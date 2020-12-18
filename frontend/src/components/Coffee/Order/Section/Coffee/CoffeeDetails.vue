<template>
  <UtilsModal :center="true" :container="true" :bgClose="true"
    ><template #header v-if="Object.keys(coffee).length !== 0">
      <h3 class="uk-modal-title">{{ coffee.farmCoop }}</h3>
    </template>
    <template #body v-if="Object.keys(coffee).length !== 0">
      <div>
        <div
          class="uk-child-width-1-3@l uk-flex uk-flex-center uk-grid-large"
          uk-grid
        >
          <div>
            <p>
              <span class="uk-text-bold">Région de culture :</span>
              {{ coffee.region }}
            </p>
            <p>
              <span class="uk-text-bold">Procéder de fabrication :</span>
              {{ coffee.process }}
            </p>
            <p>
              <span class="uk-text-bold">Variété :</span> {{ coffee.variety }}
            </p>
          </div>
          <div>
            <p>
              <span class="uk-text-bold">Origine du café :</span>
              {{ coffee.origin.name }}
            </p>
            <p>
              <span class="uk-text-bold">Prix au kilo :</span>
              {{ coffee.kilogramPrice }}€
            </p>
            <p>
              <span class="uk-text-bold">Prix pour 200 grammes :</span>
              {{ coffee.twoHundredGramPrice }}€
            </p>
          </div>
          <div>
            <p class="uk-text-bold">Mouture disponible :</p>
            <ul class="uk-list uk-list-disc">
              <li
                v-for="type in coffee.availableType.edges"
                :key="type.node.id"
              >
                {{ type.node.name }}
              </li>
            </ul>
          </div>
        </div>
        <div v-html="coffee.description" class="uk-margin-medium-top"></div>
      </div>
    </template>
    <template #footer>
      <div class="uk-text-center">
        <UtilsButton class="uk-modal-close" type="default">Fermer</UtilsButton>
      </div>
    </template>
  </UtilsModal>
</template>

<script>
import UtilsModal from '@/components/Utils/UtilsModal'
import UtilsButton from '@/components/Utils/UtilsButton'

export default {
  name: 'CoffeeDetails',
  components: {
    UtilsModal,
    UtilsButton
  },
  props: {
    coffee: {
      required: true,
      type: Object
    }
  }
}
</script>
