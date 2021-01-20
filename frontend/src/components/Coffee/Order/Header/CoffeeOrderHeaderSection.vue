<template>
  <article
    class="uk-section uk-section-default uk-box-shadow-medium uk-border-rounded"
  >
    <div class="uk-container uk-text-justify">
      <p class="uk-text-primary uk-text-bold">
        Choisissez votre café en fonction de la cafetière à laquelle vous le
        destinez :
      </p>
      <ul class="uk-list uk-list-large uk-list-bullet">
        <li>Moulu expresso pour une cafetière expresso.</li>
        <li>Moulu moka pour une cafetière italienne.</li>
        <li>Moulu piston pour une cafetière à piston.</li>
        <li>Moulu filtre pour une cafetière filtre.</li>
      </ul>
      <p class="uk-text-primary uk-text-bold">
        Vous pouvez aussi acheter votre café en grains et le moudre au fur et à
        mesure de votre consommation, l'arôme n'en sera que meilleur !
      </p>
      <ul class="uk-list uk-list-bullet">
        <li>
          Grain expresso pour cafetière italienne et expresso (la torréfaction
          est légèrement plus forte).
        </li>
        <li>
          Grain filtre pour une cafetière filtre ou piston (la torréfaction est
          légèrement plus douce).
        </li>
      </ul>
    </div>
  </article>
</template>

<script>
export default {
    name: 'CoffeeOrderHeaderSection'
}
</script>

<style>
</style>
