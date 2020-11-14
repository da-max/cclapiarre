<template>
  <div :class="[`uk-card uk-card-${type}`, { 'uk-card-hover': hover }]">
    <div class="uk-card-header" v-show="!mediaPos">
      <slot name="header"></slot>
    </div>
    <div class="uk-card-body">
      <slot name="body"></slot>
    </div>
    <div
      v-show="mediaPos"
      :class="`uk-card-media-${mediaPos}`"
    >
      <slot name="media"></slot>
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
    },
    mediaPos: {
      required: false,
      default: null,
      type: String
    }
  }
}
</script>
