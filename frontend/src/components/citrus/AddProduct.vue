<template>
  <div id="add-product">
    <loader v-show="loading" />

    <modal id="warning-display">
      <template #header>
        <h3>Enregistrer ?</h3>
      </template>
      <template #body>
        <p class="uk-text-bold uk-text-warning">
          Attention, le produit que vous voulez ajouter a l’option « afficher ce
          produit » désactivé. Ainsi, il ne sera pas affiché sur le tableau des
          commandes et ne pourra donc pas être commandé.<br />
          Êtes-vous sûr de vouloir ajouter ce produit ?
        </p>
        <p v-if="product.display == false">
          Cliquez
          <a
            class="uk-text-bold uk-text-primary"
            @click.prevent="product.display = true"
            >ici</a
          >
          afin d’afficher le produit sur le tableau des commandes.
        </p>
      </template>
      <template #footer>
        <button
          class="uk-button uk-button-primary uk-modal-close uk-margin-large-right"
          type="button"
          @click.prevent="addProduct(false)"
        >
          Ajouter ce produit
        </button>
        <button
          class="uk-button uk-button-default uk-modal-close"
          type="button"
        >
          Annuler
        </button>
      </template>
    </modal>

    <div
      id="vue-messages"
      class="uk-width-2-5@l uk-width-3-4 uk-margin-auto uk-margin-xlarge-bottom"
    >
      <message v-show="queryError" :close="false" status="danger">
        <template #header>Erreur interne</template>
        <template #body>
          Une erreur est survenue, cela vient de nous, merci d'actualiser la
          page et de nous contacter si vous rencontrez de nouveau cette erreur.
        </template>
      </message>

      <message v-show="permissionError" :close="false" status="danger">
        <template #header>Accès interdit</template>
        <template #body
          >Il semblerait qui vous n’ayez pas l’autorisation d’accéder à cette
          fonctionnalité du site.</template
        >
      </message>

      <message
        v-for="message in messages"
        :key="message.id"
        :status="message.status"
      >
        <template #header>
          <div v-html="message.header"></div>
        </template>
        <template #body>
          <div v-html="message.body"></div>
        </template>
      </message>
    </div>

    <form
      method="post"
      class="uk-width-3-5@m uk-width-4-5@s uk-margin-auto uk-form-horizontal"
      @submit.prevent="addProduct()"
    >
      <div uk-grid class="uk-child-width-1-2@l uk-grid-large uk-grid-divider">
        <div>
          <label for="name" class="uk-form-label">Nom du produit</label>
          <div class="uk-form-controls">
            <input
              type="text"
              name="name"
              v-model="product.name"
              :class="['uk-input', { 'uk-form-danger': product.name == '' }]"
              placeholder="Nom du produit"
            />
          </div>
          <br />
          <label for="price" class="uk-form-label"
            >Prix du produit (en €)</label
          >
          <div class="uk-form-controls">
            <input
              type="number"
              name="price"
              :class="['uk-input', { 'uk-form-danger': product.price <= '0' }]"
              min="0"
              v-model="product.price"
            />
          </div>
          <br />
          <label for="display" class="uk-form-label">Afficher ce produit</label>
          <div class="uk-form-controls">
            <input
              type="checkbox"
              name="display"
              v-model="product.display"
              class="uk-checkbox"
            />
          </div>
          <p class="uk-text-muted">
            Si cette case est cochée, le produit sera affiché sur le tableau :
            <router-link :to="{ name: 'citrus_command' }"
              >commander des agrumes</router-link
            >
          </p>
          <br />
          <label for="maybe_not_available" class="uk-form-label"
            >Produit peut être indisponible</label
          >
          <div class="uk-form-controls">
            <input
              type="checkbox"
              name="maybe_bot_available"
              class="uk-checkbox"
              v-model="product.maybe_not_available"
            />
          </div>
          <p class="uk-text-muted">
            Si cette case est cochée, ce produit va être considérer comme,
            possiblement, indisponible. Un message d’avertissement sera donc
            affiché afin de prévenir les adhérents.
          </p>
        </div>

        <div>
          <label for="weight" class="uk-form-label">
            Poids du produit
            <span class="uk-text-muted" v-show="product.weight == 1"
              >(ce produit se vend à l’unité)</span
            >
          </label>
          <div class="uk-form-controls">
            <input
              type="number"
              name="weight"
              v-model="product.weight"
              :class="['uk-input', { 'uk-form-danger': product.weight <= '0' }]"
              min="0"
              max="100"
            />
          </div>
          <p class="uk-text-muted">
            Si le produit se vend à l’unité, le poids doit être égale à 1.
          </p>
          <br />
          <label for="maximum" class="uk-form-label"
            >Quantité maximale commandable par adhérent</label
          >
          <div class="uk-form-controls">
            <input
              type="number"
              name="maximum"
              :class="[
                'uk-input',
                { 'uk-form-danger': product.maximum <= '0' },
              ]"
              v-model="product.maximum"
              min="0"
            />
          </div>
          <p class="uk-text-muted">
            Défini une quantité maximale, pour ce produit, commandable par
            adhérent. En plus de cette quantité, chaque adhérent ne peut pas
            commander plus de 6 caisses de produit. Si ce produit n’est pas
            vendu par caisse (il a donc un poids de 1), ce nombre est défini à
            100.
          </p>
          <br />
          <label for="step" class="uk-form-label">Pas d’augmentation</label>
          <div class="uk-form-controls">
            <input
              type="number"
              name="step"
              v-model="product.step"
              :class="['uk-input', { 'uk-form-danger': product.step <= '0' }]"
              min="0"
              max="1"
              step="0.01"
            />
          </div>
          <p class="uk-text-muted">
            Ce nombre défini le pas d’augmentation du produit, ainsi, les
            adhérents pourront commander uniquement un multiple de ce nombre.
          </p>
        </div>
      </div>
      <div class="uk-margin-large-top uk-margin-auto">
        <label for class="uk-form-label">Description du produit</label>
        <div class="uk-form-controls">
          <ckeditor :editor="editor" v-model="product.description"></ckeditor>
        </div>
        <p class="uk-text-muted">Ce champs est optionnel.</p>
      </div>
      <div class="uk-text-center uk-margin-large-top">
        <input
          type="submit"
          value="Enregistrer le produit"
          class="uk-button uk-button-primary"
          id="submit_button"
        />
      </div>
    </form>
  </div>
</template>

<script>
import Loader from "../utility/Loader";
import Modal from "../utility/Modal";
import Message from "../utility/Message";
import ClassicEditor from "@ckeditor/ckeditor5-build-classic";

export default {
  name: "AddProduct",

  components: {
    Loader,
    Message,
    ClassicEditor,
    Modal,
  },

  data() {
    return {
      product: Object(),

      // Utility
      editor: ClassicEditor,
      queryError: false,
      permissionError: false,
      messages: Array(),
      loading: false,
    };
  },

  methods: {
    addProduct(first = true) {
      if (first === true && this.product.display !== true) {
        this.product.display = false;
        UIkit.modal("#warning-display").show();
      } else {
        this.$product.save(this.product).then(
          (response) => {
            this.messages.push({
              id: Date.now(),
              header: "Produit enregistré",
              body: "Le produit a bien été ajouté.",
              status: "success",
            });
            UIkit.scroll("#submit_button", { offset: 150 }).scrollTo(
              "#vue-messages"
            );
          },
          (response) => {
            if (
              response.status === 403 &&
              response.statusText === "Forbidden"
            ) {
              this.permission_error = true;
            } else if (response.status === 400) {
              this.messages.push({
                id: parseInt(Math.random() * 1000),
                header: "Erreur",
                body:
                  "Une erreur est survenue lors de l’enregistrement du produit, merci d’actualiser la page puis de réessayer.",
                status: "danger",
              });
            } else {
              this.query_error = true;
            }
            UIkit.scroll("#submit_button", { offset: 150 }).scrollTo(
              "#vue-messages"
            );
          }
        );
      }
    },
  },

  mounted() {
    this.$product = this.$resource(
      "api/citrus/product",
      {},
      {},
      {
        before: () => {
          this.loading = true;
        },
        after: () => {
          this.loading = false;
        },
      }
    );
  },
};
</script>
