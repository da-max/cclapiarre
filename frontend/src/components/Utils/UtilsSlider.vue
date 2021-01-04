<template>
  <div
    uk-slider
    :center="center ? 'true' : 'false'"
    :autoplay="autoplay ? 'true': 'false'"
    tabindex="-1"
    class="uk-position-relative uk-visible-toggle uk-light"
  >
    <ul
      class="uk-slider-items uk-grid"
      uk-height-match="target: > li > div > img"
    >
      <li
        v-for="image in images"
        :key="image.image"
        class="uk-width-3-4"
      >
        <div class="uk-panel">
          <img
            :src="baseUrl + image.image"
            :alt="image.alt"
          >
        </div>
      </li>
    </ul>
    <a
      class="uk-position-center-left uk-position-small uk-hidden-hover"
      href="#"
      uk-slidenav-previous
      uk-slider-item="previous"
    />
    <a
      class="uk-position-center-right uk-position-small uk-hidden-hover"
      href="#"
      uk-slidenav-next
      uk-slider-item="next"
    />
  </div>
</template>

<script>
export default {
  name: 'UtilsSlider',
  props: {
    baseUrl: {
      required: true,
      type: String
    },
    images: {
      required: true,
      type: Array
    },
    autoplay: {
      required: false,
      type: Boolean,
      default: true
    },
    center: {
      required: false,
      type: Boolean,
      default: true
    }
  }
}
</script>
