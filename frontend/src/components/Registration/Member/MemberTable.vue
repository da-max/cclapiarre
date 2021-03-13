<template>
  <UtilsTable
    v-if="loading === false"
    :middle="true"
  >
    <template #head>
      <th
        v-for="headerItem in headerItems"
        :key="headerItem"
      >
        {{ headerItem }}
      </th>
    </template>
    <template #body>
      <tr
        v-for="member in result.users"
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
        <td v-if="member.phoneNumber">
          {{ member.phoneNumber }}
        </td>
        <td v-else>
          Non défini
        </td>
      </tr>
    </template>
  </UtilsTable>
</template>

<script>
import { useUtilsQuery } from '@/composition/useUtils'
import UtilsTable from '@/components/Utils/UtilsTable'

import MEMBER_ALL from '@/graphql/Member/MemberAll.gql'

export default {
    components: {
        UtilsTable
    },
    setup (props) {
        const { result, loading } = useUtilsQuery(MEMBER_ALL)
        return { result, loading }
    },
    data () {
        return {
            headerItems: ['Nom', 'Prénom', 'Email', 'Numéro de téléphone']
        }
    }
}
</script>
