<template>
  <div id="citrus-command">
    <h1 class="uk-text-center uk-margin-large-top uk-margin-large-bottom">
      Commander des agrumes
    </h1>
    <breadcrumd :elements="breadcrumb"></breadcrumd>
    <div class="uk-padding uk-margin-auto uk-width-3-5 uk-margin-xlarge-bottom">
      <img
        src="../assets/Images/Citrus/citrus.jpg"
        alt="Photo d'agrumes"
        class="uk-box-shadow-large"
        uk-img
      />
    </div>
    <section class="uk-width-3-5@m uk-margin-auto">
      <div class="uk-card uk-card-default">
        <p
          class="uk-card-body uk-text-large uk-text-justify"
          uk-scrollspy="cls:uk-animation-fade; delay: 100;"
        >
          Voici le tableau des produits proposés pour la commande. Pour le
          moment, vous pouvez commander des oranges, clémentines et mandarines
          par tranche de 3kg. Les cédrats et les citrons peuvent être commandés
          par tranche de 3kg, les pamplemousses par tranche de 2,5kg. Si ces
          tranches ne vous conviennent pas, envoyez-nous un courriel ou demandez
          à votre voisin.e/ami.e pour avoir accès à des quantités encore plus
          petites.... Pour voir le prix et la quantité proposée, il faut cliquer
          sur chacun des produits.
        </p>
      </div>
    </section>

    <table-command></table-command>
  </div>
</template>

<script>
import TableCommand from '../components/citrus/TableCommand';
import Breadcrumd from '../components/utility/Breadcrumb';

export default {
  name: 'CitrusCommand',

  components: {
    TableCommand,
    Breadcrumd
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
          link: '#',
          class: 'uk-disabled'
        },
        {
          name: 'Commader des agrumes'
        }
      ]
    };
  },

  mounted() {
    document.title = 'Commander des agrumes | CC La Piarre';
  }
};
</script>
