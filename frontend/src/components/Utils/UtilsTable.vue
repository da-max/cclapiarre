<template>
  <table
    :class="[
      'uk-table',
      {
        'uk-table-divider': divider,
        'uk-table-striped': striped,
        'uk-table-hover': hover,
        'uk-table-middle': middle
      },
    ]"
  >
    <caption v-show="caption">
      {{ caption }}
    </caption>
    <thead>
      <tr>
        <slot name="head" />
      </tr>
    </thead>
    <tbody>
      <slot name="body" />
    </tbody>
    <tfoot>
      <tr>
        <slot name="foot" />
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
        },
        middle: {
            default: false,
            required: false,
            type: Boolean
        }
    }
}
</script>
