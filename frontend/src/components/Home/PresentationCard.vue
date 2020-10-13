<template>
  <aside
    class="uk-card uk-card-default uk-card-hover"
    uk-scrollspy="cls:uk-animation-scale-down"
  >
    <div class="uk-card-header">
      <h2 class="uk-card-title">A propos de court-circuit</h2>
    </div>
    <div class="uk-card-body">
      <ul>
        <li>Date de création :</li>
        <li>
          Lieu <strong>Veynes</strong> et ses alentours dans un périmétre de
          30Km
        </li>
        <li>Nombres d'adhérents : 350</li>
        <li>
          Objectif : Permettre à chacun de consommer des
          <em
            >produits de qualité en respectant la nature et en permettant aux
            producteurs de vivre décemment</em
          >
        </li>
      </ul>
    </div>
    <div class="uk-card-footer uk-text-center">
      Ce site est exclusivement réservé au relais <em>collaboratif</em> de
      court-circuit La Piarre, ci-dessous le lien pour accéder au site de
      l'association court-circuit<br />
      <br /><a
        class="uk-button uk-button-primary"
        href="https://www.court-circuit-05.com/"
        >Site de court-circuit</a
      >
    </div>
  </aside>
</template>

<script lang="ts">
import { Vue } from 'vue-class-component'

export default class PresentationCard extends Vue {}
</script>
