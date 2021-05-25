<template>
  <UtilsModal id="member-delete-modal">
    <template #header>
      <h2 class="uk-modal-title">
        Supprimer l’adhérent : {{ member.username }} ?
      </h2>
    </template>
    <template #body>
      <p>
        Vous êtes sur le point de supprimer l’adhérent {{ member.username }},
        <span class="uk-text-danger">attention, cette action est irréversible.</span>
      </p>
    </template>
    <template #footer>
      <div class="uk-text-center">
        <UtilsButton
          type="secondary"
          class="uk-modal-close uk-margin-medium-right"
        >
          Annuler
        </UtilsButton>
        <UtilsButton
          type="danger"
          @click="deleteMember"
        >
          Supprimer
        </UtilsButton>
      </div>
    </template>
  </UtilsModal>
</template>

<script>
import useMember from '@/composition/registration/useMember'
import { useHideModal } from '@/composition/useUtils'

import UtilsModal from '@/components/Utils/UtilsModal'
import UtilsButton from '@/components/Utils/UtilsButton'

export default {
    name: 'MemberDeleteModal',
    components: {
        UtilsButton,
        UtilsModal
    },
    setup () {
        const { member, removeMember } = useMember()

        const deleteMember = () => {
            useHideModal('#member-delete-modal')
            removeMember()
        }

        return { member, deleteMember }
    }
}
</script>
