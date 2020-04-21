<template>
	<div id="citrus-product-update">
        <h1 class="uk-text-center">Modifier un produit</h1>
        <layout-boxe>
            <template #body>
                Ci-dessous se trouve un formulaire afin de modifier un produit, afin de valider la modification, penser à cliquer sur le bouton 
                « enregistrer les modifications ». <span class="uk-text-bold">Ces modifications seront affichées sur le tableau, uniquement si le produit à 
                    la case « afficher sur le tableau » cochée.
                </span>
            </template>
        </layout-boxe>
        <update-product :product_id="$route.params.product_id"></update-product>

    </div>
</template>

<script>
import LayoutBoxe from '../components/utility/LayoutBoxe'
import UpdateProduct from '../components/citrus/UpdateCitrus'

export default {
	name: "CitrusProductUpdate",

    components: {
        LayoutBoxe,
        UpdateProduct
    }
};
</script>