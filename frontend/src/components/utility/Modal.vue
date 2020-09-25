<template>
  <div
    id="modal"
    :class="{ 'uk-flex-top ': center, 'uk-modal-container': container }"
    uk-modal
    v-if="bgClose"
    bg-close="true"
  >
    <div class="uk-modal-dialog">
      <button
        class="uk-modal-close-default"
        :class="{ 'uk-magin-auto-vertical': center }"
        type="button"
        uk-close
        v-show="closeButton"
      ></button>
      <div class="uk-modal-header">
        <slot name="header"></slot>
      </div>
      <div class="uk-modal-body" uk-overflow-auto>
        <slot name="body"></slot>
      </div>
      <div class="uk-modal-footer uk-text-center uk-padding">
        <slot name="footer">
          <button
            class="uk-button uk-button-default uk-modal-close"
            type="button"
          >
            Fermer
          </button>
        </slot>
      </div>
    </div>
  </div>
  <div
    id="modal"
    :class="{ 'uk-flex-top ': center, 'uk-modal-container': container }"
    uk-modal
    v-else
    bg-close="false"
  >
    <div class="uk-modal-dialog">
      <button
        class="uk-modal-close-default"
        :class="{ 'uk-magin-auto-vertical': center }"
        type="button"
        uk-close
        v-show="closeButton"
      ></button>
      <div class="uk-modal-header">
        <slot name="header"></slot>
      </div>
      <div class="uk-modal-body" uk-overflow-auto>
        <slot name="body"></slot>
      </div>
      <div class="uk-modal-footer uk-text-center uk-padding">
        <slot name="footer">
          <button
            class="uk-button uk-button-default uk-modal-close"
            type="button"
          >
            Fermer
          </button>
        </slot>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Modal',

  props: {
    closeButton: { type: Boolean, default: true },
    center: { type: Boolean, default: false },
    container: { type: Boolean, default: false },
    bgClose: { type: Boolean, default: true }
  }
};
</script>
