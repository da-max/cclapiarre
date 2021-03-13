<template>
  <div
    uk-modal
    :class="{ 'uk-flex-top': center, 'uk-modal-container': container }"
    :esc-close="escClose ? 'true' : 'false'"
    :bg-close="bgClose ? 'true' : 'false'"
  >
    <div
      :class="['uk-modal-dialog', { 'uk-margin-auto-vertical': center }]"
    >
      <button
        v-show="close"
        class="uk-modal-close-default"
        type="button"
        uk-close
      />
      <div class="uk-modal-header">
        <slot name="header" />
      </div>
      <div
        class="uk-modal-body"
        uk-overflow-auto
      >
        <slot name="body" />
      </div>
      <div class="uk-modal-footer">
        <slot name="footer" />
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
