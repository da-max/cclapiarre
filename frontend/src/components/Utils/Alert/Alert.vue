<template>
  <div
    uk-alert
    :class="
      'uk-border-rounded uk-padding-small uk-box-shadow-small uk-box-shadow-hover-large uk-alert-' +
        status
    "
  >
    <a
      v-show="close"
      class="uk-alert-close"
      uk-close
      @click="deleteAlert(alertId)"
    />
    <div v-show="header">
      <h2 :class="'uk-text-center uk-text-' + status">
        <slot name="header" />
      </h2>
    </div>
    <p>
      <slot name="body" />
    </p>
    <hr>
    <p>
      <slot name="footer">
        Si vous rencontrez un problème, vous pouvez me contacter à l’adresse :
        maxime.benhassen@tutanota.com
      </slot>
    </p>
  </div>
</template>

<script>
import { mapMutations } from 'vuex'

export default {
  name: 'Alert',

  props: {
    status: {
      default: 'primary',
      type: String
    },
    alertId: {
      type: Number,
      required: true
    },
    close: {
      default: true,
      type: Boolean
    },
    header: {
      default: false,
      type: Boolean
    }
  },

  methods: {
    ...mapMutations({ deleteAlert: 'alert/DELETE_ALERT' })
  }
}
</script>

<style lang="scss" scoped>
.uk-alert-close {
  color: black !important;
}
</style>
