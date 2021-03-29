<template>
  <UtilsModal
    id="article-modal"
    :center="true"
    :container="true"
    :esc-close="false"
  >
    <template #header>
      <h1 class="uk-modal-title">
        Ajouter un article
      </h1>
    </template>
    <template #body>
      <ArticleForm />
    </template>
    <template #footer>
      <div class="uk-text-center">
        <UtilsButton
          type="secondary"
          class="uk-modal-close"
        >
          Annuler
        </UtilsButton>
        <UtilsButton
          class="uk-margin-medium-left"
          type="primary"
          @click="addArticle()"
        >
          Ajouter
        </UtilsButton>
      </div>
    </template>
  </UtilsModal>
</template>

<script>
import useArticle from '@/composition/article/useArticle'

import UtilsModal from '@/components/Utils/UtilsModal'
import UtilsButton from '@/components/Utils/UtilsButton'
import ArticleForm from '@/components/Article/ArticleList/ArticleForm.vue'

export default {
    name: 'ArticleAddModal',
    components: {
        ArticleForm,
        UtilsButton,
        UtilsModal
    },
    setup () {
        const { closeArticleModal, saveArticle } = useArticle()

        const addArticle = async () => {
            await saveArticle()
            closeArticleModal()
        }
        return { addArticle }
    }
}
</script>
