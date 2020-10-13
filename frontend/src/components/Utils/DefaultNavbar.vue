<template>
  <div>
    <SmallNavbar
      :admin-panel-items="adminPanelItems"
      class="uk-hidden@m uk-hidden-touch"
    ></SmallNavbar>
    <LargeNavbar
      class="uk-hidden-touch"
      :admin-panel-items="adminPanelItems"
    ></LargeNavbar>
    <MobileNavbar
      class="uk-hidden-notouch"
      :admin-panel-items="adminPanelItems"
    ></MobileNavbar>
  </div>
</template>

<script lang="ts">
import { Options, Vue } from 'vue-class-component'
import { NavbarItem } from '@/types/index'
import MobileNavbar from '@/components/Utils/Navbar/MobileNavbar.vue'
import LargeNavbar from '@/components/Utils/Navbar/LargeNavbar.vue'
import SmallNavbar from '@/components/Utils/Navbar/SmallNavbar.vue'

@Options({
  data (): Object {
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
      ] as NavbarItem[]
    }
  },
  components: {
    MobileNavbar,
    LargeNavbar,
    SmallNavbar
  }
})
export default class DefaultNavbar extends Vue {}
</script>
