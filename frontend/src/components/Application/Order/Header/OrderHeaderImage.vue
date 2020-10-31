<template>
  <div v-if="images.length === 1">
    <img
      :src="'/media/' + images[0].image"
      :alt="images[0].alt"
      uk-img
      class="uk-box-shadow-medium"
    />
  </div>
  <div
    v-else
    uk-slider="center: true; autoplay: true"
    tabindex="-1"
    class="uk-position-relative uk-visible-toggle uk-light"
  >
    <ul class="uk-slider-items uk-grid" uk-height-match="target: > li > div > img">
      <li class="uk-width-3-4" v-for="image in images" :key="image.image">
        <div class="uk-panel">
          <img :src="'/media/' + image.image" :alt="image.alt" />
        </div>
      </li>
    </ul>
    <a
      class="uk-position-center-left uk-position-small uk-hidden-hover"
      href="#"
      uk-slidenav-previous
      uk-slider-item="previous"
    ></a>
    <a
      class="uk-position-center-right uk-position-small uk-hidden-hover"
      href="#"
      uk-slidenav-next
      uk-slider-item="next"
    ></a>
  </div>
</template>

<script>
export default {
  name: 'OrderHeaderImage',
  props: {
    images: {
      required: true,
      type: Array
    }
  }
}
</script>
