<template>
  <div class="uk-margin-large-top">
    <h1 class="uk-text-center">Liste des adhérents</h1>
  </div>
</template>

<script>
import gql from 'graphql-tag'
export default {
  name: 'List',
  mounted () {
    document.title = 'Liste des adhérents | CC La Piarre'
  },
  apollo: {
    allMembers: gql`query {
      allInformationsUsers {
        id,
        name
      }
    }`
  }
}
</script>
