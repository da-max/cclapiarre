<template>
  <div>
    <SmallNavbar
      :admin-panel-items="adminPanelItems"
      :order-items="allApplications"
      class="uk-hidden@m uk-hidden-touch"
    />
    <LargeNavbar
      class="uk-hidden-touch"
      :admin-panel-items="adminPanelItems"
      :order-items="allApplications"
    />
    <MobileNavbar
      class="uk-hidden-notouch"
      :admin-panel-items="adminPanelItems"
      :order-items="allApplications"
    />
  </div>
</template>

<script>
import MobileNavbar from '@/components/Utils/Navbar/MobileNavbar'
import LargeNavbar from '@/components/Utils/Navbar/LargeNavbar'
import SmallNavbar from '@/components/Utils/Navbar/SmallNavbar'
import { mapState } from 'vuex'

export default {
  components: {
    MobileNavbar,
    LargeNavbar,
    SmallNavbar
  },
  data () {
    return {
      adminPanelItems: [
        {
          title: 'Articles',
          subItems: [
            {
              name: 'Liste des articles',
              link: '/article/liste-des-articles'
            },
            {
              name: 'Créer un article',
              link: '/article/creer-un-article'
            }
          ]
        },
        {
          title: 'Évènements',
          subItems: [
            {
              name: 'Liste des évènements',
              link: '/evenement/liste-des-evenements'
            },
            {
              name: 'Créer un évènement',
              link: '/evenement/creer-un-evenement'
            }
          ]
        },
        {
          title: 'Café',
          subItems: [
            {
              name: 'Liste des cafés',
              link: '/cafe/liste-des-cafes'
            },
            {
              name: 'Ajouter un café',
              link: '/cafe/creer-un-cafe'
            },
            {
              name: 'Divider 1',
              divider: true
            },
            {
              name: 'Liste des commandes',
              routerLink: { name: 'CoffeeOrderList' }
            },
            {
              name: 'Commande globale',
              link: '/cafe/commande-globale'
            },
            {
              name: 'Divider 2',
              divider: true
            },
            {
              name: 'Liste des origines',
              link: '/cafe/liste-des-origines'
            },
            {
              name: 'Ajouter une origine',
              link: '/cafe/creer-une-origine'
            }
          ]
        },
        {
          title: 'Carousel',
          subItems: [
            {
              name: 'Liste des carousels',
              link: '/carousel/liste-des-carousels'
            },
            {
              name: 'Créer un carousel',
              link: '/carousel/creer-un-carousel'
            }
          ]
        },
        {
          title: 'Paramètres',
          subItems: [
            {
              name: 'Liste des règles d’accès aux pages',
              link: '/parametre/liste-des-acces'
            },
            {
              name: 'Ajouter une règles d’accès à une page',
              link: '/parametre/creer-une-regle-d-acces'
            }
          ]
        },
        {
          title: 'Agrumes',
          subItems: [
            {
              name: 'Liste des produits',
              routerLink: { name: 'CitrusList' }
            }
          ]
        }
      ]
    }
  },
  computed: {
    ...mapState({ allApplications: (state) => state.application.applications })
  }
}
</script>
