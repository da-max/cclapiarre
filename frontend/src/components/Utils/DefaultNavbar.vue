<template>
  <div v-if="!loading">
    <SmallNavbar
      :admin-panel-items="adminPanelItems"
      :orderItems="result.allApplications"
      class="uk-hidden@m uk-hidden-touch"
    ></SmallNavbar>
    <LargeNavbar
      class="uk-hidden-touch"
      :admin-panel-items="adminPanelItems"
      :orderItems="result.allApplications"
    ></LargeNavbar>
    <MobileNavbar
      class="uk-hidden-notouch"
      :admin-panel-items="adminPanelItems"
      :orderItems="result.allApplications"
    ></MobileNavbar>
  </div>
</template>

<script>
import MobileNavbar from '@/components/Utils/Navbar/MobileNavbar'
import LargeNavbar from '@/components/Utils/Navbar/LargeNavbar'
import SmallNavbar from '@/components/Utils/Navbar/SmallNavbar'
import ApplicationAll from '@/graphql/Application/ApplicationAll.gql'

import { useQuery } from '@vue/apollo-composable'

export default {
  setup () {
    const { result, loading } = useQuery(ApplicationAll)
    console.log(result)
    return { result, loading }
  },
  data () {
    return {
      adminPanelItems: [
        {
          title: 'Articles',
          subItems: [
            {
              name: 'Liste des articles',
              link: ''
            },
            {
              name: 'Créer un article',
              link: ''
            }
          ]
        },
        {
          title: 'Évènements',
          subItems: [
            {
              name: 'Liste des évènements',
              link: ''
            },
            {
              name: 'Créer un évènement',
              link: ''
            }
          ]
        },
        {
          title: 'Carousel',
          subItems: [
            {
              name: 'Liste des carousels',
              link: ''
            },
            {
              name: 'Créer un carousel',
              link: ''
            }
          ]
        }
      ]
    }
  },
  components: {
    MobileNavbar,
    LargeNavbar,
    SmallNavbar
  }
}
</script>
