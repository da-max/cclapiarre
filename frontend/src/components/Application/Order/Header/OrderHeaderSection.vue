<template>
  <section class="uk-section uk-section-default uk-box-shadow-medium uk-border-rounded">
    <div v-html="description" class="uk-container uk-text-large uk-text-justify"></div>
  </section>
</template>

<script>
export default {
  name: 'OrderHeaderSection',
  props: {
    description: {
      required: true,
      type: String
    }
  }
}
</script>
