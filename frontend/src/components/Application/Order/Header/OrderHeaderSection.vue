<template>
  <article
    class="uk-section uk-section-default uk-box-shadow-medium uk-border-rounded"
  >
    <div
      v-if="isAdmin && update"
      class="uk-container uk-text-large uk-text-justify"
    >
      <ckeditor
        :editor="editor"
        v-model="newDescription"
        :config="config"
      ></ckeditor>
    </div>
    <div
      v-else
      v-html="description"
      class="uk-container uk-text-large uk-text-justify"
    ></div>
    <footer class="uk-margin-medium-top uk-text-center" v-show="isAdmin">
      <div v-if="update">
        <UtilsButton
          :disabled="newDescription === description"
          @click="updateDescription"
        >
          Enregistrer
        </UtilsButton>
        <UtilsButton
          type="secondary"
          class="uk-margin-medium-left"
          @click="update = false"
          >Annuler</UtilsButton
        >
      </div>
      <div v-else>
        <UtilsButton @click="update = true">Modifier</UtilsButton>
      </div>
    </footer>
  </article>
</template>

<script>
import CKEditor from '@ckeditor/ckeditor5-vue'
import ClassicEditor from 'ckeditor5-build-classic-with-font'
import UtilsButton from '@/components/Utils/UtilsButton'

export default {
  name: 'OrderHeaderSection',
  data () {
    return {
      editor: ClassicEditor,
      newDescription: this.description,
      update: false,
      config: {
        toolbar: [
          'heading',
          '|',
          'bold',
          'italic',
          'link',
          'bulletedList',
          'numberedList',
          '|',
          'blockQuote',
          'insertTable',
          'undo',
          'redo',
          '|',
          'fontColor',
          'fontSize',
          'fontBackgroundColor'
        ]
      }
    }
  },
  props: {
    description: {
      required: true,
      type: String
    },
    isAdmin: {
      required: false,
      default: false,
      type: Boolean
    }
  },
  components: {
    UtilsButton,
    ckeditor: CKEditor.component
  },
  methods: {
    updateDescription () {
      this.$emit('update-description', this.newDescription)
      this.update = false
    }
  }
}
</script>
