<template>
  <form class="uk-form-horizontal">
    <FormInput
      name="title"
      label="Titre du carousel"
      :value="carousel.title"
      @input="updateTitle"
    />
    <div class="uk-flex uk-flex-around">
      <div>
        <label
          for="image"
          class="uk-form-label"
        >Image</label>
        <div uk-form-custom="target: true">
          <input
            id="image"
            type="file"
            name="image"
            accept="image/*"
            @change="updateImage"
          >
          <input
            class="uk-input uk-form-width-medium"
            type="text"
            placeholder="Image sélectionner"
            disabled
          >
          <UtilsButton
            type="default"
          >
            Sélectionner
          </UtilsButton>
        </div>
      </div>
      <div>
        <FormInputNumber
          :value="carousel.position"
          label="Position du carousel"
          help-text="Plus ce nombre est grand, plus le carousel sera placé loin."
          name="position"
          @input="updatePosition"
        />
      </div>
    </div>
    <div class="uk-margin-medium-top">
      <label
        for="description"
        class="uk-form-label"
      >Description du carousel</label>
      <ckeditor
        id="description"
        :value="carousel.description"
        :editor="editor"
        required="true"
        @input="updateDescription"
      />
    </div>
  </form>
</template>

<script>
import useCarousel from '@/composition/carousel/useCarousel'

import CKEditor from '@ckeditor/ckeditor5-vue'
import ClassicEditor from 'ckeditor5-build-classic-with-font'

import FormInput from '@/components/Utils/Form/FormInput.vue'
import FormInputNumber from '@/components/Utils/Form/FormInputNumber.vue'
import UtilsButton from '@/components/Utils/UtilsButton'

export default {
    name: 'CarouselForm',
    components: {
        FormInput,
        FormInputNumber,
        ckeditor: CKEditor.component,
        UtilsButton
    },
    setup () {
        const {
            carousel,

            updateDescription,
            updateImage,
            updatePosition,
            updateTitle
        } = useCarousel()

        return {
            carousel,

            updateDescription,
            updateImage,
            updatePosition,
            updateTitle,

            // Editor config
            editor: ClassicEditor
        }
    }
}
</script>
