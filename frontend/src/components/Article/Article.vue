<template>
  <article class="uk-article">
    <h1 class="uk-article-title">
      {{ article.title }}
    </h1>
    <p class="uk-article-meta">
      Article écrit par {{ article.author.username }}
    </p>
    <p class="uk-article-meta">
      Catégorie : {{ article.category.name }}
    </p>
    <p v-html="article.content" />
    <div
      v-show="actions"
      class="uk-flex uk-flex-center"
    >
      <div>
        <UtilsButton
          v-show="canChangeArticle"
          @click="showArticleModal(article.id)"
        >
          Modifier
        </UtilsButton>
        <UtilsButton
          v-show="canDeleteArticle"
          class="uk-margin-medium-left"
          type="danger"
          @click="showDeleteArticleModal(article.id)"
        >
          Supprimer
        </UtilsButton>
      </div>
    </div>
  </article>
</template>

<script>
import useArticle from '@/composition/article/useArticle'

import UtilsButton from '@/components/Utils/UtilsButton'

export default {
    name: 'Article',
    components: {
        UtilsButton
    },
    props: {
        article: {
            required: true,
            type: Object
        },
        actions: {
            required: false,
            default: () => false,
            type: Boolean
        }
    },
    setup () {
        const {
            canChangeArticle,
            canDeleteArticle,

            showDeleteArticleModal,
            showArticleModal
        } = useArticle()

        return {
            canChangeArticle,
            canDeleteArticle,

            showDeleteArticleModal,
            showArticleModal
        }
    }
}
</script>
