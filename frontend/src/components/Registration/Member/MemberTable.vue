<template>
  <UtilsTable v-if="loading === false">
    <template #head>
      <th v-for="headerItem in headerItems" :key="headerItem">
        {{ headerItem }}
      </th>
    </template>
    <template #body>
      <tr v-for="member in result.allInformationsUsers" :key="member.id">
        <td>
          {{ member.user.lastName }}
        </td>
        <td>
          {{ member.user.firstName }}
        </td>
        <td>
          {{ member.user.email }}
        </td>
        <td>{{ member.phoneNumber }}</td>
      </tr>
    </template>
  </UtilsTable>
</template>

<script>
import UtilsTable from '@/components/Utils/UtilsTable'
import { useQuery } from '@vue/apollo-composable'

import MemberAll from '@/graphql/Member/MemberAll.gql'

export default {
  setup (props) {
    const { result, loading } = useQuery(MemberAll)
    return { result, loading }
  },
  data () {
    return {
      headerItems: ['Nom', 'Prénom', 'Email', 'Numéro de téléphone']
    }
  },
  components: {
    UtilsTable
  }
}
</script>
