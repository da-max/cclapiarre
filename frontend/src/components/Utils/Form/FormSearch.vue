<template>
  <form class="uk-inline">
    <span
      class="uk-form-icon"
      uk-icon="search"
    />
    <vue-fuse
      placeholder="Rechercher un produit"
      :default-all="defaultAll"
      :list="elements"
      :keys="keys"
      class="uk-input"
      @fuseResultsUpdated="$emit('fuse-results-updated')"
    />
  </form>
</template>

<script>
import VueFuse from 'vue-fuse'

export default {
  name: 'FormSearch',
  components: {
    VueFuse
  },
  props: {
    placehloder: {
      default: 'Rechercher',
      required: false,
      type: String
    },
    defaultAll: {
      default: true,
      required: false,
      type: Boolean
    },
    elements: {
      required: true,
      type: Array
    },
    keys: {
      required: true,
      type: Array
    }
  }
}
</script>
