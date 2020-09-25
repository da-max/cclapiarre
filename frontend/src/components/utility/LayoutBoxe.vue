<template>
  <aside
    id="layout-boxes"
    :class="[
      'uk-tile uk-tile-' + background,
      {
        ' uk-width-3-5@m uk-margin-auto ': width_3_5,
        ' uk-box-shadow-medium ': shadow,
        ' uk-text-justify ': justify,
        ' uk-margin-large-top uk-margin-large-bottom ': margin
      }
    ]"
  >
    <slot name="body"></slot>
  </aside>
</template>

<script>
export default {
  name: 'LayoutBoxe',
  props: {
    background: { type: String, default: 'default' },
    width35: { type: Boolean, default: true },
    shadow: { type: Boolean, default: true },
    justify: { type: Boolean, default: true },
    margin: { type: Boolean, default: true },
    animation: { type: Boolean, default: true },
    animationName: { type: String, default: 'fade' }
  },

  mounted() {
    if (this.animation) {
      UIkit.scrollspy('#layout-boxes', {
        cls: 'uk-animation-' + this.animation_name
      });
    }
  }
};
</script>
