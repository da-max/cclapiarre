<template>
  <main>
    <ArticleListHeader class="uk-margin-large-top" />
    <AlertsStyling />
    <ArticleListSection />
  </main>
</template>

<script>
import ArticleListHeader from '@/components/Article/ArticleList/ArticleListHeader'
import ArticleListSection from '@/components/Article/ArticleList/ArticleListSection'
import AlertsStyling from '@/components/Utils/Alert/AlertsStyling'

export default {
    name: 'ArticleList',
    components: {
        ArticleListHeader,
        ArticleListSection,
        AlertsStyling
    }
}
</script>
