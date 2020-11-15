<template>
  <div id="alerts">
    <div
      v-for="alert in $store.state.alert.alerts"
      :key="alert.id"
      class="uk-margin-medium-top"
    >
      <alert
        :alert-id="alert.id"
        :close="alert.close || null"
        :header="alert.header || false"
        :status="alert.status || null"
      >
        <template #header>
          {{ alert.headerContent }}
        </template>
        <template #body>
          {{ alert.body }}
        </template>
      </alert>
    </div>
  </div>
</template>

<script>
import Alert from '@/components/Utils/Alert/Alert'
export default {
  name: 'Alerts',

  components: {
    Alert
  }
}
</script>
