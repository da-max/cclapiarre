<template>
  <article
    class="uk-section uk-section-default uk-box-shadow-medium uk-border-rounded"
  >
    <div
      v-if="isAdmin && update"
      class="uk-container uk-text-large uk-text-justify"
    >
      <ckeditor
        v-model="description"
        :editor="editor"
        :config="config"
      />
    </div>
    <div
      v-else
      class="uk-container uk-text-large uk-text-justify"
      v-html="description"
    />
    <footer
      v-show="isAdmin"
      class="uk-margin-medium-top uk-text-center"
    >
      <div v-if="update">
        <UtilsButton
          :disabled="newDescription === description"
          @click="saveDescription"
        >
          Enregistrer
        </UtilsButton>
        <UtilsButton
          type="secondary"
          class="uk-margin-medium-left"
          @click="update = false"
        >
          Annuler
        </UtilsButton>
      </div>
      <div v-else>
        <UtilsButton @click="update = true">
          Modifier
        </UtilsButton>
      </div>
    </footer>
  </article>
</template>

<script>
import { computed, reactive, toRefs } from '@vue/composition-api'

import CKEditor from '@ckeditor/ckeditor5-vue'
import ClassicEditor from 'ckeditor5-build-classic-with-font'
import store from '@/store/index'
import useApplication from '@/composition/application/useApplication'

import UtilsButton from '@/components/Utils/UtilsButton'

export default {
    name: 'OrderHeaderSection',
    components: {
        UtilsButton,
        ckeditor: CKEditor.component
    },
    setup (props, { root }) {
        const { isAdmin, updateApplication } = useApplication(
            root.$route.params.application
        )

        const description = computed({
            get: () => store.state.application.currentApplication.description,
            set (newValue) {
                store.commit('application/CHANGE_DESCRIPTION', newValue)
            }
        })

        const newDescription = computed(() =>
            store.state.application.currentApplication.newDescription
                ? store.state.application.currentApplication.newDescription
                : store.state.application.currentApplication.description
        )
        const state = reactive({
            editor: ClassicEditor,
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
        })

        const saveDescription = async () => {
            await updateApplication()
            state.update = false
        }

        return { ...toRefs(state), isAdmin, description, saveDescription, newDescription }
    }
}
</script>
