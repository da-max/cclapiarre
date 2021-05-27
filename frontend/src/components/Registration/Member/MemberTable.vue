<template>
  <UtilsTable
    :middle="true"
  >
    <template #head>
      <th
        v-for="headerItem in headerItems"
        :key="headerItem"
      >
        {{ headerItem }}
      </th>
      <th v-show="canDeleteMember || canChangeMember">
        Actions
      </th>
    </template>
    <template #body>
      <tr
        v-for="member in members"
        :key="member.id"
      >
        <td v-if="member.lastName">
          {{ member.lastName }}
        </td>
        <td v-else>
          Non défini
        </td>
        <td v-if="member.firstName">
          {{ member.firstName }}
        </td>
        <td v-else>
          Non défini
        </td>
        <td v-if="member.email">
          {{ member.email }}
        </td>
        <td v-else>
          Non défini
        </td>
        <td v-if="member.information && member.information.phoneNumber">
          {{ member.information.phoneNumber }}
        </td>
        <td v-else>
          Non défini
        </td>
        <td>
          <a
            v-show="canChangeMember"
            type="button"
            class="uk-icon-link"
            uk-icon="refresh"
            @click="showMemberModal(member)"
          />
          <a
            v-show="canDeleteMember"
            type="button"
            class="uk-icon-link"
            uk-icon="trash"
            @click="showDeleteMemberModal(member)"
          />
        </td>
      </tr>
    </template>
  </UtilsTable>
</template>

<script>
import UtilsTable from '@/components/Utils/UtilsTable'
import useMember from '@/composition/registration/useMember'

export default {
    components: {
        UtilsTable
    },
    setup () {
        const {
            canDeleteMember,
            canChangeMember,
            getMembers,
            members,
            showDeleteMemberModal,
            showMemberModal
        } = useMember()

        getMembers()

        return {
            canChangeMember,
            canDeleteMember,
            members,
            showDeleteMemberModal,
            showMemberModal
        }
    },
    data () {
        return {
            headerItems: ['Nom', 'Prénom', 'Email', 'Numéro de téléphone']
        }
    }
}
</script>
