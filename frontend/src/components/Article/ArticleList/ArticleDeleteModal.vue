<template>
  <UtilsModal id="article-delete-modal">
    <template #header>
      Supprimer l’article ?
    </template>
    <template #body>
      <p>
        Vous êtes sur le point de supprimer l’article {{ article.title }},
        <span class="uk-text-danger">attention, cette action est irréversible</span>
      </p>
    </template>
    <template #footer>
      <div class="uk-text-center">
        <UtilsButton
          type="secondary"
          class="uk-modal-close uk-margin-medium-right"
        >
          Annuler
        </UtilsButton>
        <UtilsButton
          type="danger"
          @click="removeArticle"
        >
          Supprimer
        </UtilsButton>
      </div>
    </template>
  </UtilsModal>
</template>

<script>
import useArticle from '@/composition/article/useArticle'

import UtilsButton from '@/components/Utils/UtilsButton'
import UtilsModal from '@/components/Utils/UtilsModal'

export default {
    name: 'ArticleDeleteModal',
    components: {
        UtilsModal,
        UtilsButton
    },
    setup () {
        const { article, closeDeleteArticleModal, deleteArticle } = useArticle()

        const removeArticle = () => {
            deleteArticle()
            closeDeleteArticleModal()
        }

        return { article, removeArticle }
    }
}
</script>
