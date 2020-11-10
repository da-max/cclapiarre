<template>
  <table
    :class="[
      'uk-table',
      {
        'uk-table-divider': divider,
        'uk-table-striped': striped,
        'uk-table-hover': hover
      },
    ]"
  >
  <caption v-show="caption">{{ caption }}</caption>
    <thead>
      <tr>
          <slot name="head"></slot>
      </tr>
    </thead>
    <tbody>
      <slot name="body"></slot>
    </tbody>
    <tfoot>
      <tr>
        <slot name="foot"></slot>
      </tr>
    </tfoot>
  </table>
</template>

<script>
export default {
  name: 'UtilsTable',
  props: {
    caption: {
      default: null,
      required: false,
      type: String
    },
    divider: {
      default: true,
      required: false,
      type: Boolean
    },
    striped: {
      default: true,
      required: false,
      type: Boolean
    },
    hover: {
      default: true,
      required: false,
      type: Boolean
    }
  }
}
</script>
