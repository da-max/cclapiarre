<template>
  <footer
    id="footer"
    uk-scrollspy="cls: uk-animation-scale-up; delay: 100"
    class="uk-box-shadow-large uk-box-shadow-top uk-padding uk-padding-large-top uk-padding-medium-bottom uk-margin-xlarge-top uk-background-muted uk-position-bottom uk-position-relative"
  >
    <ul
      class="uk-child-width-expand@s uk-grid-large uk-text-center uk-padding uk-padding-bottom"
      uk-grid
    >
      <li
        v-for="utilsLink in utilsLinks"
        :key="utilsLink.name"
      >
        <a
          class="uk-button uk-button-text"
          :href="utilsLink.link"
        >{{
          utilsLink.name
        }}</a>
      </li>
    </ul>
    <ul
      class="uk-padding-bottom uk-text-muted uk-text-small uk-margin-auto uk-text-center uk-list"
    >
      <li>
        Ce site est gracieusement hébergé par
        <a
          href="https://deblan.fr"
          class="uk-link"
        >Deblan.fr</a>.
      </li>
      <li>
        Site développé et maintenu par
        <a href="http://fedabian.fr">Maxime Ben Hassen</a>.
      </li>
      <li>
        Ce projet est placé sous licence libre
        <a href="https://www.gnu.org/licenses/agpl-3.0.html">AGPL-3</a>.
      </li>
      <li>Version : {{ version }}</li>
      <li>
        <a
          href="https://gitlab.com/Damax/cclapiarre"
        ><i class="fab fa-gitlab fa-2x uk-link-heading" /></a>
      </li>
    </ul>
  </footer>
</template>

<script>
import { version } from '../../../package.json'

export default {
    data () {
        return {
            utilsLinks: [
                {
                    name:
            'Contacter court-circuit buëch méouge : ccbuechmeouge@gmail.com',
                    link: 'mailto:ccbuechmeouge@gmail.com'
                },
                {
                    name: 'À propos du site',
                    link: '/changements'
                },
                {
                    name:
            'Contacter Court-circuit La Piarre : courtcircuit.lapiarre@gmail.com',
                    link: 'mailto:courtcircuit.lapiarre@gmail.com'
                }
            ],
            version
        }
    }
}
</script>
