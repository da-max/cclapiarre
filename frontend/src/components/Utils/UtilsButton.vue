<template>
  <button
    :class="[
      `uk-button uk-button-${type}`,
      {
        'uk-button-large': width === 'large',
        'uk-button-small': width === 'small',
      },
    ]"
    @click.prevent="$emit('click')"
  >
    <slot />
  </button>
</template>

<script>
export default {
  name: 'UtilsButton',
  props: {
    type: {
      type: String,
      default: 'primary',
      required: false
    },
    width: {
      type: String,
      default: ''
    }
  }
}
</script>
