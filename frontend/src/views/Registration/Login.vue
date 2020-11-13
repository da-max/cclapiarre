<template>
  <div>
    <h1 class="uk-text-center uk-margin-large-top uk-margin-large-bottom">
      {{ title }}
    </h1>
    <div class="uk-width-2-5@l uk-width4-5@s uk-margin-auto">
      <Alerts />
    </div>
    <LoginSection />
  </div>
</template>

<script>
import Alerts from '@/components/Utils/Alert/Alerts'
import LoginSection from '@/components/Registration/Login/LoginSection'
import { useSetupTitle } from '@/composition/useUtils'

export default {
  setup (props) {
    const title = 'Se connecter'
    useSetupTitle(title)
    return {
      title
    }
  },
  components: {
    LoginSection,
    Alerts
  }
}
</script>
