<template>
  <header class="uk-margin-large-top">
    <h1 class="uk-text-center">
      Agrumes
    </h1>
    <div
      class="uk-margin-large-top uk-margin-auto uk-width-1-2@l uk-width-4-5@m"
    >
      <img
        src="/static/Images/Citrus/citrus.jpg"
        alt=""
        uk-img
        class="uk-box-shadow-large"
      >
    </div>
    <div class="uk-margin-xlarge-top uk-width-3-5@m uk-margin-auto">
      <article class="uk-section uk-section-default uk-box-shadow-medium uk-border-rounded uk-text-large">
        <div class="uk-container uk-text-justify">
          <p>
            Voici le tableau des produits proposés pour la commande.
            Pour le moment, vous pouvez commander des oranges, clémentines et mandarines par tranche de 3kg.
            Les cédrats et les citrons peuvent être commandés par tranche de 3kg, les pamplemousses par
            tranche de 2,5kg. Si ces tranches ne vous conviennent pas, envoyez-nous un courriel ou
            demandez à votre voisin.e/ami.e pour avoir accès à des quantités encore plus petites....
            Pour voir le prix et la quantité proposée, il faut cliquer sur chacun des produits.
          </p>
        </div>
      </article>
    </div>
  </header>
</template>

<script>
import { reactive, toRefs } from '@vue/composition-api'

export default {
  name: 'CitrusOrderHeader',
  setup () {
    const state = reactive({
      images: [
        {
          image: 'citrus.jpg',
          alt: 'Image de présentation de l’application agrumes.'
        }
      ]
    })
    return { ...toRefs(state) }
  }
}
</script>
