<template>
  <form class="uk-form-horizontal">
    <FormInput
      v-model="article.title"
      name="title"
      label="Titre de l’article"
      :value="article.title"
    />
    <div>
      <label
        for="categories"
        class="uk-form-label"
      >Catégories</label>
      <div class="uk-form-controls">
        <select
          id="categories"
          v-model="article.category"
          class="uk-select"
          name="categories"
        >
          <option :value="null">
            ---
          </option>
          <option
            v-for="category in categories"
            :key="category.id"
            :value="category.id"
          >
            {{ category.name }}
          </option>
        </select>
      </div>
    </div>
    <div class="uk-margin-medium-top">
      <label
        for="description"
        class="uk-form-label"
      >Contenu de l’article</label>
      <ckeditor
        id="description"
        v-model="article.content"
        :value="article.content"
        required="true"
        :editor="editor"
      />
    </div>
  </form>
</template>
<script>
import useArticle from '@/composition/article/useArticle'

import CKEditor from '@ckeditor/ckeditor5-vue'
import ClassicEditor from 'ckeditor5-build-classic-with-font'

import FormInput from '@/components/Utils/Form/FormInput.vue'

export default {
    name: 'ArticleForm',
    components: {
        FormInput,
        ckeditor: CKEditor.component
    },
    setup () {
        const { article, categories, getCategories } = useArticle()

        getCategories()

        return {
            article,
            categories,
            editor: ClassicEditor
        }
    }

}
</script>
