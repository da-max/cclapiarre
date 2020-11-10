<template>
  <div
    uk-modal
    :class="{ 'uk-flex-top': center, 'uk-modal-container': container }"
    :esc-close="escClose ? 'true' : 'false'"
    :bg-close="bgClose ? 'true' : 'false'"
  >
    <div
      :class="['uk-modal-dialog', { 'uk-margin-auto-vertical': center }]"
      uk-overflow-auto
    >
      <button
        v-show="close"
        class="uk-modal-close-default"
        type="button"
        uk-close
      ></button>
      <div class="uk-modal-header">
        <slot name="header"></slot>
      </div>
      <div class="uk-modal-body">
        <slot name="body"></slot>
      </div>
      <div class="uk-modal-footer">
        <slot name="footer"></slot>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UtilsModal',
  props: {
    close: {
      default: true,
      required: false,
      type: Boolean
    },
    center: {
      default: false,
      required: false,
      type: Boolean
    },
    container: {
      default: false,
      required: false,
      type: Boolean
    },
    escClose: {
      default: true,
      required: false,
      type: Boolean
    },
    bgClose: {
      default: false,
      required: false,
      type: Boolean
    }
  }
}
</script>
