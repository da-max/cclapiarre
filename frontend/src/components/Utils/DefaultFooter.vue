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
      <li>
        <a
          class="uk-button uk-button-text"
          href="https://www.court-circuit-05.com/"
          >Lien vers Court Circuit buëch</a
        >
      </li>
      <li>
        <a class="uk-button uk-button-text" href="">A propos du site</a>
      </li>
      <li>
        <a class="uk-button uk-button-text" href="mailto:da-max@tutanota.com"
          >Contacter Court-circuit La Piarre : <br />da-max@tutanota.com</a
        >
      </li>
    </ul>
    <ul
      class="uk-padding-bottom uk-text-muted uk-text-small uk-margin-auto uk-text-center uk-width-1-3 uk-list"
    >
      <li>
        Ce site est gracieusement hébergé par
        <a href="https://deblan.fr" class="uk-link">Deblan.fr</a>.
      </li>
      <li>
        Site développé et maintenu par
        <a href="http://fedabian.fr">Maxime Ben Hassen</a>.
      </li>
      <li>
        Ce projet est placé sous licence libre
        <a href="https://www.gnu.org/licenses/agpl-3.0.html">AGPL-3</a>.
      </li>
      <li>Version :</li>
      <li>
        <a href="https://gitlab.com/Damax/cclapiarre"
          ><i class="fab fa-gitlab fa-2x uk-link-heading"></i
        ></a>
      </li>
    </ul>
  </footer>
</template>

<script lang="ts">
import { Vue } from 'vue-class-component'

export default class DefaultFooter extends Vue {}
</script>
