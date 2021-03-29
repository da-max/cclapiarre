<template>
  <p
    v-if="articles.length === 0"
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
    <ArticleModal />
  </section>
</template>

<script>
import useArticle from '@/composition/article/useArticle'

import Article from '@/components/Article/Article'
import ArticleModal from '@/components/Article/ArticleList/ArticleModal'

export default {
    name: 'ArticleListSection',
    components: {
        Article,
        ArticleModal

    },
    setup () {
        const { articles } = useArticle()

        return {
            articles
        }
    }
}
</script>
