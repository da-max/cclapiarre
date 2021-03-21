<template>
  <p
    v-if="loading"
    class="uk-text-center"
  >
    Chargement en cours...
  </p>
  <p
    v-else-if="articles.length === 0"
    class="uk-text-center"
  >
    Aucun article.
  </p>
  <section
    v-else
    class="uk-width-1-2@m uk-margin-auto"
  >
    <Article
      v-for="article in articles"
      :key="article.key"
      :article="article"
      :actions="true"
      class="uk-padding uk-background-default"
    />
  </section>
</template>

<script>
import useArticle from '@/composition/article/useArticle'

import Article from '@/components/Article/Article'

export default {
    name: 'ArticleListSection',
    components: {
        Article
    },
    setup () {
        const { allArticle } = useArticle()

        const { articles, loading } = allArticle()

        return {
            articles,
            loading
        }
    }
}
</script>
