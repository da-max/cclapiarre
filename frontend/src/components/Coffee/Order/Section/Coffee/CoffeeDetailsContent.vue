<template>
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
        <p class="uk-text-bold">
          Mouture disponible :
        </p>
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
    <div
      class="uk-margin-medium-top"
      v-html="coffee.description"
    />
  </div>
</template>

<script>
export default {
  name: 'CoffeeDetailsContent',
  props: {
    coffee: {
      required: true,
      type: Object
    }
  }
}
</script>
