<template>
  <header class="uk-margin-large-top uk-margin-large-bottom">
    <h1 class="uk-text-center">
      Liste des produits
    </h1>
    <article class="uk-section uk-section-default uk-box-shadow-medium uk-border-rounded">
      <div class="uk-container uk-text-justify">
        Ci-dessous se trouve la liste des produits disponibles à la commande sur la page commander des agrumes. Si les produits ont le status « afficher le produit »
        le produit sera affiché sur le tableau et les adhérents pourront le
        commander. Sinon, le produit ne sera pas affiché (et donc pas commandable). Ainsi, il est inutile de supprimer les produits, il suffit de les déclarer comme « invisible ».
      </div>
    </article>
  </header>
</template>

<script>
export default {
  name: 'CitrusProductListHeader'
}
</script>
