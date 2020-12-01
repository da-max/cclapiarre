<template>
  <div>
    <SmallNavbar
      :admin-panel-items="adminPanelItems"
      :orderItems="allApplications"
      class="uk-hidden@m uk-hidden-touch"
    ></SmallNavbar>
    <LargeNavbar
      class="uk-hidden-touch"
      :admin-panel-items="adminPanelItems"
      :orderItems="allApplications"
    ></LargeNavbar>
    <MobileNavbar
      class="uk-hidden-notouch"
      :admin-panel-items="adminPanelItems"
      :orderItems="allApplications"
    ></MobileNavbar>
  </div>
</template>

<script>
import MobileNavbar from '@/components/Utils/Navbar/MobileNavbar'
import LargeNavbar from '@/components/Utils/Navbar/LargeNavbar'
import SmallNavbar from '@/components/Utils/Navbar/SmallNavbar'
import { mapState } from 'vuex'

export default {
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
  computed: {
    ...mapState({ allApplications: (state) => state.application.applications })
  },
  components: {
    MobileNavbar,
    LargeNavbar,
    SmallNavbar
  }
}
</script>
