<template>
  <div
    class="uk-position-relative uk-visible-toggle"
    tabindex="-1"
    uk-slideshow="animation: fade; autoplay: true; autoplay-interval: 6000; ratio: 7:3; max-height: 700"
  >
    <ul class="uk-slideshow-items">
      <li v-for="carousel in carousels" :key="carousel.alt">
        <img :src="'/media/' + carousel.imageUrl" :alt="carousel.alt" uk-cover />
        <div
          class="uk-overlay uk-overlay-primary uk-position-left uk-text-center uk-transition-slide-left uk-width-large"
        >
          <h3 class="uk-margin-remove">{{ carousel.title }}</h3>
          <p class="uk-margin-remove" v-html="carousel.description"></p>
        </div>
      </li>
    </ul>
    <div class="uk-light">
      <a
        href="#"
        uk-slidenav-previous
        uk-slideshow-item="previous"
        class="uk-position-center-left uk-position-small uk-slidenav-large"
      ></a>
      <a
        class="uk-position-center-right uk-position-small uk-slidenav-large"
        href="#"
        uk-slidenav-next
        uk-slideshow-item="next"
      ></a>
    </div>
    <ul class="uk-slideshow-nav uk-dotnav uk-flex-center uk-margin"></ul>
  </div>
</template>

<script>
export default {
  name: 'Carousels',
  props: {
    carousels: {
      required: true,
      type: Array
    }
  }
}
</script>
