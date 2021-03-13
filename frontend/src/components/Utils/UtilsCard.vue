<template>
  <div
    :class="[
      `uk-card uk-card-${type}`,
      {
        'uk-card-hover': hover,
        ' uk-button-small': width === 'small',
        ' uk-button-large': width === 'large',
      },
    ]"
  >
    <div
      v-show="!mediaPos && header"
      class="uk-card-header"
    >
      <slot name="header" />
    </div>
    <div class="uk-card-body">
      <slot name="body" />
    </div>
    <div
      v-show="mediaPos"
      :class="`uk-card-media-${mediaPos}`"
    >
      <slot name="media" />
    </div>
    <div
      v-if="footer"
      class="uk-card-footer"
    >
      <slot name="footer" />
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
        },
        width: {
            required: false,
            default: 'medium',
            type: String
        },
        header: {
            required: false,
            default: true,
            type: Boolean
        },
        footer: {
            required: false,
            default: true,
            type: Boolean
        }
    }
}
</script>
