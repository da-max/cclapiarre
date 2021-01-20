<template>
  <div class="uk-margin-large-top">
    <h1 class="uk-text-center">
      {{ title }}
    </h1>
    <Alerts />
    <MemberSection class="uk-width-3-5@l uk-width-4-5@s uk-margin-auto" />
  </div>
</template>

<script>
import { useSetupTitle } from '@/composition/useUtils'

import Alerts from '@/components/Utils/Alert/Alerts'
import MemberSection from '@/components/Registration/Member/MemberSection'

export default {
    components: {
        MemberSection,
        Alerts
    },
    setup () {
        const title = 'Liste des adhérents'
        useSetupTitle(title)
        return { title }
    }
}
</script>
