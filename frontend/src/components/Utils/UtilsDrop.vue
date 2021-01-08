<template>
  <div :uk-drop="`mode: ${mode}; pos: ${pos}`">
    <div class="uk-card uk-card-default">
      <slot />
    </div>
  </div>
</template>

<script>
export default {
  name: 'UtilsDrop',
  props: {
    mode: {
      required: false,
      type: String,
      default: 'hover'
    },
    pos: {
      required: false,
      type: String,
      default: 'right-center'
    }
  }
}
</script>
