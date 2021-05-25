<template>
  <main>
    <MemberListHeader class="uk-margin-large-top" />
    <AlertsStyling />
    <MemberListSection class="uk-width-3-5@l uk-width-4-5@s uk-margin-auto" />
  </main>
</template>

<script>
import { useSetupTitle } from '@/composition/useUtils'

import AlertsStyling from '@/components/Utils/Alert/AlertsStyling'
import MemberListSection from '@/components/Registration/Member/MemberListSection'
import MemberListHeader from '@/components/Registration/Member/MemberListHeader'

export default {
    components: {
        MemberListHeader,
        MemberListSection,
        AlertsStyling
    },
    setup () {
        const title = 'Liste des adhérents'
        useSetupTitle(title)

        return { title }
    }
}
</script>
