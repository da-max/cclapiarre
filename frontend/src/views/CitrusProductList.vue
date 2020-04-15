<template lang="fr">
    <div id='citrus-product-list'>
        <h1 class="uk-text-center uk-margin-large-bottom">Liste des produits</h1>
        <aside class="uk-margin-large-top uk-margin-large-bottom uk-tile uk-tile-default uk-width-3-5@m uk-margin-auto uk-box-shadow-medium uk-text-justify">
            Ci-dessous se trouve la liste des produits disponibles à la commande sur la page <a href="/agrumes/commander-des-agrumes">commander des agrumes</a>. 
            Si les produits ont le status « afficher le produit » le produit sera affiché sur le tableau et les adhérents pourront le commander. Sinon, le produit 
            ne sera pas affiché (et donc pas commandable). Ainsi, <span class="uk-text-bold">il est inutile de supprimer les produits</span>, il suffit de les déclarer comme « invisible ».
        </aside>
        <list-product></list-product>
    </div>
</template>

<script>
import ListProduct from '../components/citrus/ListProduct'

export default {
    name: "CitrusProductList",
    
    components: {
        ListProduct
    }
};
</script>