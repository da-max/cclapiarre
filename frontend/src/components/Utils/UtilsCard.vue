<template>
  <div :class="[`uk-card uk-card-${type}`, { 'uk-card-hover': hover}]">
    <div class="uk-card-header">
      <slot name="header"></slot>
    </div>
    <div class="uk-card-body">
      <slot name="body"></slot>
    </div>
    <div class="uk-card-footer">
      <slot name="footer"></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UtilsCard',
  props: {
    type: {
      required: false,
      default: 'default',
      type: String
    },
    hover: {
      required: false,
      default: false,
      type: Boolean
    }
  }
}
</script>
