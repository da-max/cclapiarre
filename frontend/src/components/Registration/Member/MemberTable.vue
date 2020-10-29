<template>
  <UtilsTable>
    <template #head>
      <th v-for="headerItem in headerItems" :key="headerItem">
        {{ headerItem }}
      </th>
    </template>
    <template #body>
      <tr v-for="member in data.data.allInformationsUsers" :key="member.id">
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
import { useDataFetcher } from '@/composition/useDataFetcher'

import MemberAll from '@/graphql/Member/MemberAll.gql'

export default {
  setup (props) {
    const { error, data } = useDataFetcher({ query: MemberAll })
    console.log(error, data)
    return { error, data }
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
