<template>
  <main>
    <Carousels
      v-if="!loading"
      :carousels="result.allCarousels"
    />
    <div class="uk-width-2-5@l uk-width4-5@s uk-margin-auto uk-margin-large-top">
      <Alerts />
    </div>
    <div
      uk-grid
      class="uk-margin-auto uk-width-4-5@xl uk-width-expands uk-margin-medium-top"
    >
      <div class="uk-width-2-3@l uk-width-auto">
        <Article
          v-for="article in articles"
          :key="article.id"
          :article="article"
          :separator="true"
        />
      </div>
      <div class="uk-width-1-3@l uk-width-auto uk-text-justify uk-padding">
        <PresentationCard />
      </div>
    </div>
  </main>
</template>

<script>
import { useSetupTitle } from '@/composition/useUtils'
import { useQuery } from '@vue/apollo-composable'
import useArticle from '@/composition/article/useArticle'

import Article from '@/components/Article/Article'
import Alerts from '@/components/Utils/Alert/Alerts'
import Carousels from '@/components/Home/Carousels'
import PresentationCard from '@/components/Home/PresentationCard'

import CAROUSEL_ALL from '@/graphql/Carousel/CarouselAll.gql'

export default {
    components: {
        Alerts,
        Article,
        Carousels,
        PresentationCard
    },
    setup (props) {
        useSetupTitle('Accueil')
        const { result, loading } = useQuery(CAROUSEL_ALL)
        const { articles, getArticles } = useArticle()

        getArticles()
        return {
            articles,
            result,
            loading
        }
    }
}
</script>
