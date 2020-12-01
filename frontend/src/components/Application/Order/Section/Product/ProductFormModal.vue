<template>
  <UtilsModal
    v-if="!loading"
    id="product-form-modal"
    :container="true"
    :center="true"
    :esc-close="false"
  >
    <template #header>
      <h2 v-if="update" class="uk-modal-title">
        Modifier le produit : {{ product.name }}
      </h2>
      <h2 class="uk-modal-title" v-else>Ajouter un produit</h2>
    </template>
    <template #body>
      <Alerts />
      <form class="uk-margin-large-bottom">
        <FormInput
          type="text"
          name="name"
          label="Nom du produit"
          :value="product.name"
          v-model="product.name"
        />
        <div class="uk-child-width-1-2@l uk-grid-medium uk-flex-center" uk-grid>
          <fieldset class="uk-fieldset uk-text-center">
            <legend class="uk-legend">Poids du produit</legend>
            <div class="uk-inline">
              <button
                type="button"
                uk-icon="plus"
                class="uk-icon-button"
                title="Ajouter un poids"
              ></button>
              <AddWeightDrop @add-weight="addWeight" />
            </div>
            <div class="uk-height-medium uk-overflow-auto">
              <div v-for="weight in weights.edges" :key="weight.node.id">
                <label :for="weight.node.id" class="uk-form-label"
                  >{{ weight.node.weight }} {{ weight.node.unit }} pour
                  {{ weight.node.price }} €</label
                >
                <div class="uk-form-controls">
                  <input
                    type="checkbox"
                    v-model="product.weights"
                    :value="weight.node.id"
                    :name="weight.node.id"
                    class="uk-checkbox"
                  />
                </div>
              </div>
            </div>
          </fieldset>
          <fieldset class="uk-fieldset uk-text-center">
            <legend class="uk-legend uk-margin-small-bottom">
              Options du produit
            </legend>
            <div class="uk-inline">
              <button
                type="button"
                uk-icon="plus"
                class="uk-icon-button"
                title="Ajouter une option"
              ></button>
              <AddOptionDrop @add-option="addOption" />
            </div>
            <div class="uk-height-medium uk-overflow-auto">
              <div v-for="option in options.edges" :key="option.node.id">
                <label :for="option.node.id" class="uk-form-label">{{
                  option.node.name
                }}</label>
                <div class="uk-form-controls">
                  <input
                    v-model="product.options"
                    :value="option.node.id"
                    type="checkbox"
                    :name="option.node.id"
                    class="uk-checkbox"
                  />
                </div>
              </div>
            </div>
          </fieldset>
        </div>
        <div
          class="uk-child-width-1-4@l uk-child-width-1-2@m uk-grid-medium uk-flex-center"
          uk-grid
        >
          <div>
            <div uk-form-custom>
              <input type="file" @change="upload" required />
              <button
                class="uk-button uk-button-default"
                type="button"
                tabindex="-1"
              >
                Image du produit
              </button>
            </div>
            <p class="uk-text-muted">
              Cette image sera affiché sur la page des commandes.
            </p>
          </div>
          <div>
            <label for="display" class="uk-form-label"
              >Afficher le produit</label
            >
            <div class="uk-form-controls">
              <input
                type="checkbox"
                name="display"
                required
                v-model="product.display"
                class="uk-checkbox"
              />
            </div>
            <p class="uk-text-muted">
              Si cette case est décochée, le produit sera caché et ne sera pas
              commandable.
            </p>
          </div>
          <div>
            <FormInputNumber
              :value="product.maximum"
              :v-model="product.maximum"
              name="maximum"
              label="Maximum par commande"
            />
            <p class="uk-text-muted">
              Défini la quantité maximale commandable par adhérent.
            </p>
          </div>
          <div>
            <FormInputNumber
              :value="product.maximumAll"
              v-model="product.maximumAll"
              :max="1000"
              name="maximum-all"
              label="Maximum pour le produit"
            />
            <p class="uk-text-muted">
              Défini la quantité maximal commandable par tout les adhérents.
            </p>
          </div>
        </div>
        <ckeditor :editor="editor" v-model="product.description" />
      </form>
    </template>
    <template #footer>
      <div class="uk-text-center">
        <UtilsButton
          class="uk-margin-medium-right uk-modal-close"
          type="default"
          >Annuler</UtilsButton
        >
        <UtilsButton
          type="primary"
          @click="saveProduct($route.params.application)"
          >{{ update ? "Modifier" : "Ajouter" }} le produit</UtilsButton
        >
      </div>
    </template>
  </UtilsModal>
</template>

<script>
import CKEditor from '@ckeditor/ckeditor5-vue'
import ClassicEditor from 'ckeditor5-build-classic-with-font'
import { computed } from '@vue/composition-api'

import store from '@/store/index'

import useOption from '@/composition/application/product/useOption'
import useWeight from '@/composition/application/product/useWeight'
import useApplication from '@/composition/application/useApplication'
import { useUtilsMutation } from '@/composition/useUtils'

import Alerts from '@/components/Utils/Alert/Alerts'
import UtilsModal from '@/components/Utils/UtilsModal'
import UtilsButton from '@/components/Utils/UtilsButton'
import FormInput from '@/components/Utils/Form/FormInput'
import FormInputNumber from '@/components/Utils/Form/FormInputNumber'
import AddOptionDrop from '@/components/Application/Order/Section/Product/Option/AddOptionDrop'
import AddWeightDrop from '@/components/Application/Order/Section/Product/Weight/AddWeightDrop'

export default {
  name: 'ProductFormModal',
  setup (props, { root }) {
    // Computed
    // ==========
    const { application } = useApplication(root.$route.params.application)

    const updated = computed(() => props.update && Object.keys(props.productUpdate).length !== 0)
    const productOptions = computed(() => {
      if (updated.value) {
        return props.productUpdate.options.edges.map(
          (option) => option.node.id
        )
      }
      return []
    })
    const productWeights = computed(() => {
      if (updated.value) {
        return props.productUpdate.weights.edges.map(
          (weight) => weight.node.id)
      }
      return []
    })
    const product = computed(() => {
      if (updated.value) {
        return { ...props.productUpdate, options: productOptions.value, weights: productWeights.value }
      }
      return {
        name: '',
        description: '',
        weights: [],
        options: [],
        maximum: 100,
        maximumAll: 1000,
        display: true
      }
    })

    const {
      options,
      newOption,
      loading: optionLoading,
      getOptionsByApplicationSlug,
      optionAdd
    } = useOption()

    const {
      weights,
      getWeightByApplicationSlug,
      weightAdd,
      loading: weightLoading
    } = useWeight()

    // Methods
    // =========

    getWeightByApplicationSlug(() => ({
      applicationSlug: root.$route.params.application
    }))

    getOptionsByApplicationSlug(() => ({
      applicationSlug: root.$route.params.application
    }))

    const addOption = (data) => {
      const input = {
        name: data.newOption,
        application: application.id
      }
      useUtilsMutation(optionAdd, input)
    }

    const addWeight = (data) => {
      const input = {
        ...data.newWeight,
        application: application.value.id
      }
      useUtilsMutation(weightAdd, input)
    }

    const saveProduct = () => {
      // eslint-disable-next-line no-undef
      UIkit.modal('#product-form-modal').hide()
      const input = {
        ...product.value,
        application: application.value.id
      }

      store.dispatch('application/saveProduct', { product: input, update: props.update })
    }

    const upload = (ev) => {
      product.value.image = ev.target.files[0]
    }

    const loading = computed(() => !!(weightLoading.value || optionLoading.value))

    return {
      editor: ClassicEditor,
      options,
      weights,
      loading,
      product,
      newOption,
      addOption,
      addWeight,
      upload,
      saveProduct
    }
  },
  props: {
    productUpdate: {
      required: false,
      type: Object,
      default: () => ({})
    },
    update: {
      required: false,
      default: false,
      type: Boolean
    }
  },
  components: {
    UtilsModal,
    FormInput,
    AddOptionDrop,
    AddWeightDrop,
    ckeditor: CKEditor.component,
    UtilsButton,
    FormInputNumber,
    Alerts
  }
}
</script>
