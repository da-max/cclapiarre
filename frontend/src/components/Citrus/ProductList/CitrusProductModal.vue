<template>
  <UtilsModal
    :container="true"
    :center="true"
    :esc-close="false"
  >
    <template #header>
      <h2 class="uk-modal-title">
        {{ citrusUpdate.name ? `Modifier le produit : ${product.name}` : 'Ajouter un produit' }}
      </h2>
    </template>
    <template #body>
      <Alerts />
      <form
        class="uk-margin-large-bottom uk-form-horizontal"
      >
        <fieldset
          uk-grid
          class="uk-fieldset uk-child-width-1-2@l uk-grid-medium uk-flex-center "
        >
          <FormInput
            v-model="product.name"
            type="text"
            name="name"
            label="Nom du produit"
            :value="product.name"
          />
          <FormInputNumber
            v-model="product.weight"
            name="weight"
            label="Poids du produit"
            :value="product.weight"
            :step="0.01"
          >
            Si le produit se vend à l’unité, le poids doit être égale à 1.
          </FormInputNumber>
          <FormInputNumber
            v-model="product.price"
            name="price"
            label="Prix du produit (en €)"
            :value="product.price"
            :step="0.01"
          />
          <div>
            <label
              for="display"
              class="uk-form-label"
            >Afficher ce produit</label>
            <div class="uk-form-controls uk-text-center">
              <input
                id="display"
                v-model="product.display"
                name="display"
                type="checkbox"
                class="uk-checkbox"
              >
            </div>
            <p class="uk-text-muted">
              Si cette case est cochée, le produit sera affiché sur le tableau : commander des agrumes.
            </p>
          </div>
          <FormInputNumber
            v-model="product.maximum"
            name="maximum"
            label="Quantité maximale commandable par adhérent"
            :value="product.maximum"
            :step="0.1"
          >
            Défini une quantité maximale, pour ce produit, commandable par adhérent. En plus de cette quantité, chaque
            adhérent ne peut pas commander plus de 6 caisses de produit. Si ce produit n’est pas vendu par caisse (il a
            donc un poids de 1), ce nombre est défini à 100.
          </FormInputNumber>
          <div>
            <label
              for="maybeNotAvailable"
              class="uk-form-label"
            >Ce produit peut-être indisponible</label>
            <div class="uk-form-controls">
              <input
                id="maybeNotAvailable"
                v-model="product.maybeNotAvailable"
                type="checkbox"
                class="uk-checkbox"
                name="maybeNotAvailable"
              >
            </div>
            <p class="uk-text-muted">
              Si cette case est cochée, ce produit va être considérer comme, possiblement, indisponible.
              Un message d’avertissement sera donc affiché afin de prévenir les adhérents.
            </p>
          </div>
          <FormInputNumber
            v-model="product.step"
            :step="0.01"
            name="step"
            label="Pas d’augmentation"
            :value="product.step"
          >
            Ce nombre défini le pas d’augmentation du produit, ainsi,
            les adhérents pourront commander uniquement un multiple de ce nombre.
          </FormInputNumber>
        </fieldset>
        <div class="uk-margin-large-top">
          <label
            for="description"
            class="uk-form-label"
          >Description du produit</label>
          <ckeditor
            id="description"
            v-model="product.description"
            :editor="editor"
          />
        </div>
      </form>
    </template>
    <template #footer>
      <div class="uk-text-center">
        <UtilsButton
          type="default"
          class="uk-margin-medium-right uk-modal-close"
        >
          Annuler
        </UtilsButton>
        <UtilsButton type="primary">
          {{ citrusUpdate.name ? 'Modifier' : 'Ajouter' }} le produit
        </UtilsButton>
      </div>
    </template>
  </UtilsModal>
</template>

<script>
import { computed } from '@vue/composition-api'
import CKEditor from '@ckeditor/ckeditor5-vue'
import ClassicEditor from 'ckeditor5-build-classic-with-font'

import useCitrus from '@/composition/citrus/useCitrus'

import UtilsModal from '@/components/Utils/UtilsModal'
import Alerts from '@/components/Utils/Alert/Alerts'
import FormInput from '@/components/Utils/Form/FormInput'
import FormInputNumber from '@/components/Utils/Form/FormInputNumber'
import UtilsButton from '@/components/Utils/UtilsButton'

export default {
  name: 'CitrusProductModal',
  components: { UtilsButton, FormInputNumber, FormInput, Alerts, UtilsModal, ckeditor: CKEditor.component },
  setup () {
    const { citrusUpdate } = useCitrus()
    const product = computed(() => {
      if (citrusUpdate.value.name) {
        return { ...citrusUpdate.value }
      } else {
        return {
          name: '',
          description: '',
          weight: 0,
          price: 0,
          display: true,
          maybeNotAvailable: false,
          step: 1,
          maximum: 100
        }
      }
    })

    return {
      editor: ClassicEditor,
      citrusUpdate,
      product
    }
  }
}

</script>
