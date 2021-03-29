<template>
  <main>
    <ArticleListHeader class="uk-margin-large-top" />
    <AlertsStyling />
    <ArticleListSection />
  </main>
</template>

<script>
import useArticle from '@/composition/article/useArticle'

import AlertsStyling from '@/components/Utils/Alert/AlertsStyling'
import ArticleListHeader from '@/components/Article/ArticleList/ArticleListHeader'
import ArticleListSection from '@/components/Article/ArticleList/ArticleListSection'

export default {
    name: 'ArticleList',
    components: {
        AlertsStyling,
        ArticleListHeader,
        ArticleListSection
    },
    setup () {
        const { getArticles } = useArticle()

        getArticles()
    }
}
</script>
