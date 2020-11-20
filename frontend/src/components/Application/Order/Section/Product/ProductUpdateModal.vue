<template>
  <UtilsModal
    v-if="!loading"
    :container="true"
    :center="true"
    :esc-close="false"
  >
    <template #header>
      <h2 class="uk-modal-title">Modifier le produit : {{ productUpdated.name }}</h2>
    </template>
    <template #body>
      <form class="uk-margin-large-bottom">
        <FormInput
          type="text"
          name="name"
          label="Nom du produit"
          :value="product.name"
          v-model="productUpdated.name"
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
            <div class="uk-height-small uk-overflow-auto">
              <div v-for="weight in weights.edges" :key="weight.node.id">
                <label :for="weight.node.id" class="uk-form-label"
                  >{{ weight.node.weight }} {{ weight.node.unit }} pour
                  {{ weight.node.price }} €</label
                >
                <div class="uk-form-controls">
                  <input
                    type="checkbox"
                    v-model="productUpdated.weights"
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
            <div class="uk-height-small uk-overflow-auto">
              <div v-for="option in options.edges" :key="option.node.id">
                <label :for="option.node.id" class="uk-form-label">{{
                  option.node.name
                }}</label>
                <div class="uk-form-controls">
                  <input
                    v-model="productUpdated.options"
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
              <input type="file" @change="upload" />
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
                v-model="productUpdated.display"
                class="uk-checkbox"
              />
            </div>
            <p class="uk-text-muted">
              Si cette case est décochée, le produit sera caché et ne sera pas
              commandable.
            </p>
          </div>
          <div>
            <FormInput
              :value="productUpdated.maximum"
              :v-model="productUpdated.maximum"
              type="number"
              name="maximum"
              label="Maximum par commande"
            />
            <p class="uk-text-muted">
              Défini la quantité maximale commandable par adhérent.
            </p>
          </div>
          <div>
            <FormInput
              :value="productUpdated.maximumAll"
              v-model="productUpdated.maximumAll"
              type="number"
              name="maximum-all"
              label="Maximum pour le produit"
            />
            <p class="uk-text-muted">
              Défini la quantité maximal commandable par tout les adhérents.
            </p>
          </div>
        </div>
        <ckeditor :editor="editor" v-model="productUpdated.description" />
      </form>
    </template>
    <template #footer>
      <div class="uk-text-center">
        <UtilsButton type="primary" @click="updateProduct($route.params.application)">Modifier le produit</UtilsButton>
      </div>
    </template>
  </UtilsModal>
</template>

<script>
import CKEditor from '@ckeditor/ckeditor5-vue'
import ClassicEditor from 'ckeditor5-build-classic-with-font'

import store from '@/store/index'

import useOption from '@/composition/application/product/useOption'
import useWeight from '@/composition/application/product/useWeight'
import useProduct from '@/composition/application/product/useProduct'
import { useUtilsMutation } from '@/composition/useUtils'

import UtilsModal from '@/components/Utils/UtilsModal'
import UtilsButton from '@/components/Utils/UtilsButton'
import FormInput from '@/components/Utils/Form/FormInput'
import AddOptionDrop from '@/components/Application/Order/Section/Product/Option/AddOptionDrop'
import AddWeightDrop from '@/components/Application/Order/Section/Product/Weight/AddWeightDrop'
import { computed } from '@vue/composition-api'

export default {
  name: 'ProductUpdateModal',
  setup (props, ctx) {
    // Computed
    // ==========

    const optionSelected = (optionId) =>
      !!props.product.options.edges.find(
        (option) => option.node.id === optionId
      )

    const { productUpdated, productUpdate } = useProduct()

    productUpdated.value = computed(() => {
      const options = props.product.options.edges.map(
        (option) => option.node.id
      )
      const weights = props.product.weights.edges.map(
        (weight) => weight.node.id
      )
      return { ...props.product, options, weights }
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

    getWeightByApplicationSlug((ctx) => ({
      applicationSlug: ctx.$route.params.application
    }))

    getOptionsByApplicationSlug((ctx) => ({
      applicationSlug: ctx.$route.params.application
    }))

    const addOption = (data) => {
      const input = {
        name: data.newOption,
        application: store.getters['application/idApplicationBySlug'](
          data.application
        )
      }
      useUtilsMutation(optionAdd, input)
    }

    const addWeight = (data) => {
      const input = {
        ...data.newWeight,
        application: store.getters['application/idApplicationBySlug'](
          data.application
        )
      }
      useUtilsMutation(weightAdd, input)
    }

    const updateProduct = (applicationSlug) => {
      const input = {
        ...productUpdated.value,
        application: store.getters['application/idApplicationBySlug'](applicationSlug)
      }
      console.log(productUpdated.value)
      useUtilsMutation(productUpdate, input)
    }

    const upload = (ev) => {
      productUpdated.value.image = ev.target.files[0]
    }

    return {
      editor: ClassicEditor,
      options,
      weights,
      loading: weightLoading && optionLoading,
      productUpdated,
      optionSelected,
      newOption,
      addOption,
      addWeight,
      upload,
      updateProduct
    }
  },
  props: {
    product: {
      required: true,
      type: Object
    }
  },
  components: {
    UtilsModal,
    FormInput,
    AddOptionDrop,
    AddWeightDrop,
    ckeditor: CKEditor.component,
    UtilsButton
  }
}
</script>
