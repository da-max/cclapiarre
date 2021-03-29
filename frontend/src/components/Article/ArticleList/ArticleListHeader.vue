<template>
  <header>
    <h1 class="uk-text-center">
      Liste des articles
    </h1>
    <div class="uk-text-center uk-margin-large-top">
      <UtilsButton
        @click="showArticleModal"
      >
        Ajouter un article
      </UtilsButton>
    </div>
  </header>
</template>

<script>
import useArticle from '@/composition/article/useArticle'

import UtilsButton from '@/components/Utils/UtilsButton'
export default {
    name: 'ArticleListHeader',
    components: {
        UtilsButton
    },
    setup () {
        const { showArticleModal } = useArticle()

        return {
            showArticleModal
        }
    }
}
</script>
