<template>
  <div id="citrus-product-add">
    <h1 class="uk-text-center">Ajouter un produit</h1>
    <breadcrumb :elements="breadcrumb"></breadcrumb>
    <layout-boxe>
      <template #body>
        Ci-dessous se trouve un formulaire afin d’ajouter un produit, afin
        d’enregistrer le produit, pensez à cliquer sur le bouton « enregistrer
        le produit ».
        <span class="uk-text-bold"
          >Le produit sera affiché sur le tableau uniquement si le produit a la
          case « afficher sur le tableau » cochée.</span
        >
      </template>
    </layout-boxe>
    <add-product></add-product>
  </div>
</template>

<script>
import Breadcrumb from '../components/utility/Breadcrumb';
import LayoutBoxe from '../components/utility/LayoutBoxe';
import AddProduct from '../components/citrus/AddProduct';

export default {
  name: 'CitrusProductAdd',

  components: {
    Breadcrumb,
    LayoutBoxe,
    AddProduct
  },

  data() {
    return {
      breadcrumb: [
        {
          name: 'Accueil',
          link: '/'
        },
        {
          name: 'Agrumes',
          link: 'uk-disabled'
        },
        {
          name: 'Liste des produits',
          link: '/agrumes/liste-des-produits'
        },
        {
          name: 'Ajouter un produit'
        }
      ]
    };
  },
  mounted() {
    document.title = 'Ajouter un produit | CC La Piarre';
  }
};
</script>
