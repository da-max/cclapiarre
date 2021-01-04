<template>
  <div>
    <div class="uk-text-center">
      <h5>Poids disponible</h5>
      <ul class="uk-list">
        <li
          v-for="weight in weights.edges"
          :key="weight.node.id"
        >
          {{ weight.node.weight }} {{ weight.node.unit }} pour
          {{ weight.node.price }} €
        </li>
      </ul>
    </div>
    <div v-if="options.edges.length !== 0">
      <h5>Options disponible</h5>
      <ul class="uk-list">
        <li
          v-for="option in options.edges"
          :key="option.node.id"
        >
          {{ option.node.name }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProductItemInformation',
  props: {
    weights: {
      required: true,
      type: Object
    },
    options: {
      required: false,
      type: Object,
      default: () => ({})
    }
  }
}
</script>
