<template>
  <div id="coffeeCommandList">
    <loader v-show="loading"></loader>

    <modal
      id="update-command"
      :container="true"
      :center="true"
      v-if="Object.keys(update_command) != 0"
    >
      <template v-slot:header>
        <h3>Modifier la commande de {{ update_command.first_name }} {{ update_command.name }}</h3>
      </template>
      <template v-slot:body>
        <form action="#">
          <table class="uk-table uk-table-divider uk-table-striped">
            <thead>
              <tr>
                <th>Nom du café</th>
                <th>Poids</th>
                <th>Type de mouture</th>
                <th>Quantité</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="command in update_command.command" :key="command.id">
                <td>
                  <select name="coffees" class="uk-select" v-model="command.coffee.farm_coop">
                    <option>{{ command.coffee.farm_coop }}</option>
                    <option v-for="coffee in coffees.filter(c => c.farm_coop != command.coffee.farm_coop)" :key="coffee.id">{{ coffee.farm_coop }}</option>
                  </select>
                </td>
                <td>{{ command.weight }}</td>
                <td>{{ command.sort.name }}</td>
                <td>{{ command.quantity }}</td>
              </tr>
            </tbody>
          </table>
        </form>
      </template>
    </modal>

    <modal id="delete-all">
      <template v-slot:header>
        <h3 class="uk-modal-title">Supprimer toutes les commandes ?</h3>
      </template>
      <template v-slot:body>
        Vous êtes sur le point de supprimer toutes les commandes de café,
        <span
          class="uk-text-warning uk-text-bold"
        >attention, cette action est irréversible !</span>
      </template>
      <template v-slot:footer>
        <a
          class="uk-button uk-button-danger uk-margin-right"
          @click.prevent="delete_all_command()"
        >Supprimer</a>
        <button type="button" class="uk-button uk-button-default uk-modal-close">Annuler</button>
      </template>
    </modal>
    <header
      class="uk-text-center uk-margin-large-bottom"
      uk-scrollspy="cls:uk-animation-fade; delay:200; target: > *"
    >
      <h1 class="uk-text-center">Liste des commandes de café</h1>
      <div class="uk-margin-large-top" v-if="Object.keys(commands).length != 0">
        <a
          href
          type="button"
          class="uk-button uk-button-secondary uk-padding-small"
        >Télécharger la liste des commandes au format PDF</a>
        <a
          type="button"
          class="uk-button uk-button-danger uk-padding-small uk-margin-medium-left"
          uk-toggle="target: #delete-all"
          href="#"
        >Supprimer toutes les commandes</a>
      </div>
      <div class="uk-margin-large-top" v-else>
        <p class="uk-text-large uk-text-muted">Aucune commande n’est enregistrée.</p>
      </div>
    </header>
    <section>
      <div
        id="vue-messages"
        class="uk-width-2-5@m uk-width-3-4 uk-margin-auto uk-margin-xlarge-bottom"
      >
        <!-- Display if error = true -->
        <message v-show="query_error" :close="false" status="danger">
          <template v-slot:header>Erreur interne</template>
          <template v-slot:body>
            Une erreur est survenue, cela vient de nous, merci d'actualiser la page et de
            nous contacter si vous rencontrez de nouveau cette erreur.
          </template>
        </message>

        <!-- Dsiplay if permission_error = true -->
        <message v-show="permission_error" :close="false" status="danger">
          <template v-slot:header>Accès interdit</template>
          <template
            v-slot:body
          >Il semblerait qui vous n'ayez pas l'autorisation d'accéder à cette fonctionnalité du site.</template>
        </message>

        <message v-for="message in messages" :key="message.id" :status="message.status">
          <template v-slot:header>
            <div v-html="message.header"></div>
          </template>
          <template v-slot:body>
            <div v-html="message.body"></div>
          </template>
        </message>
      </div>
    </section>

    <section class="uk-width-2-3@m uk-width-1-2@xl uk-width-3-4@s uk-margin-auto">
      <div
        class="uk-card uk-card-default uk-card-large"
        v-for="command in commands"
        :key="command.id"
      >
        <div class="uk-card-header uk-text-bold uk-child-width-auto uk-margin-small-bottom" uk-grid>
          <div>
            <span class="uk-label">Nom</span>
            {{ command.name }}
          </div>
          <div>
            <span class="uk-label">Prénom</span>
            {{ command.first_name }}
          </div>
          <div>
            <span class="uk-label">Email</span>
            {{ command.email }}
          </div>
          <div>
            <span class="uk-label">Numéro de téléphone</span>
            {{ command.phone_number }}
          </div>
          <div>
            <span class="uk-label">Prix à payer</span>
            {{ command.total }} €
          </div>
        </div>
        <div class="uk-card-body">
          <ul class="uk-list uk-list-divider">
            <li v-for="c in command.command" :key="c.id">
              <a
                class="uk-button uk-button-text"
                type="button"
                href="#"
                :uk-toggle="'target: #coffee-info-' + c.id"
              >{{ c.coffee.farm_coop }}</a>
              ({{ c.sort.name }})
              <p class="uk-text-right">{{ c.weight }} g x {{ c.quantity }} = {{ c.total }}</p>
              <modal :id="'coffee-info-' + c.id" :container="true" :center="true">
                <template v-slot:header>
                  <h3 class="uk-text-center">{{ c.coffee.farm_coop }}</h3>
                </template>
                <template v-slot:body>
                  <div uk-grid class="uk-grid-large uk-child-width-expand uk-margin-auto">
                    <div>
                      <span class="uk-text-bold">Région de culture :</span>
                      {{ c.coffee.region }}
                      <br />
                      <span class="uk-text-bold">Procéder de fabrication :</span>
                      {{ c.coffee.process }}
                      <br />
                      <span class="uk-text-bold">Variété :</span>
                      {{ c.coffee.variety }}
                    </div>
                    <div>
                      <span class="uk-text-bold">Origine du café :</span>
                      {{ c.coffee.origin.name }}
                      <br />
                      <span class="uk-text-bold">Prix au kilo :</span>
                      {{ c.coffee.kilogram_price }} €
                      <br />
                      <span class="uk-text-bold">Prix pour deux cents grammes :</span>
                      {{ c.coffee.two_hundred_gram_price }} €
                    </div>
                    <div>
                      <span class="uk-text-bold">Mouture disponible :</span>
                      <ul class="uk-list uk-list-bullet">
                        <li v-for="type in c.coffee.available_type" :key="type.id">{{ type.name }}</li>
                      </ul>
                    </div>
                  </div>
                  <div v-html="c.coffee.description"></div>
                </template>
              </modal>
              <modal :id="'delete-command-' + command.id">
                <template v-slot:header>
                  <h3>Supprimer la commande de {{ command.first_name }} {{ command.name }}</h3>
                </template>
                <template v-slot:body>
                  Vous êtes sur le point de supprimer la commande {{ command.first_name }} {{ command.name }},
                  <span
                    class="uk-text-warning uk-text-bold"
                  >attention, cette commande est irréversible.</span>
                </template>
                <template v-slot:footer>
                  <button
                    class="uk-button uk-button-danger uk-margin-medium-right"
                    @click.prevent="delete_command(command.id)"
                  >Supprimer la commande</button>
                  <button class="uk-button uk-button-default uk-modal-close">Annuler</button>
                </template>
              </modal>
            </li>
          </ul>
        </div>
        <div class="uk-card-footer">
          <button
            class="uk-button uk-button-secondary"
            @click.prevent="get_update_command(command.id)"
          >Modifier cette commande</button>
          <button
            class="uk-button uk-button-danger uk-margin-medium-left"
            :uk-toggle="'#delete-command-' + command.id"
          >Supprimer cette commande</button>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import Modal from "../components/utility/Modal";
import Loader from "../components/utility/Loader";
import Message from "../components/utility/Message";

export default {
  name: "CoffeeCommandList",

  components: {
    Modal,
    Loader,
    Message
  },

  data() {
    return {
      commands: {},
      update_command: {},
      coffees: {},

      messages: [],

      loading: false,
      query_error: false,
      permission_error: false
    };
  },
  methods: {
    delete_command(id_command) {
      UIkit.modal("#delete-command-" + id_command).hide();

      this.$command.remove({ id: id_command }).then(
        response => {
          this.messages.push(response.data);
          this.get_command();
        },
        response => {
          this.query_error = true;
          this.get_command();
        }
      );
    },

    delete_all_command() {
      this.$command.remove({ id: "destroy-all" }).then(
        response => {
          this.messages.push(reponse.data);
          this.get_command();
        },
        response => {
          this.commands();
          this.query_error = true;
        }
      );
    },

    get_command() {
      this.$command.query().then(
        response => {
          this.commands = response.data;
        },
        response => {
          if (response.status == 403 && response.statusText == "Forbidden") {
            this.permission_error = true;
          } else {
            this.query_error = true;
          }
        }
      );
    },

    get_update_command(id_command) {
      this.$coffee.query().then((response) => {
        this.coffees = response.data
      }, response => {
        this.query_error = true
      })
      this.update_command = this.commands.find(c => {
        return c.id === id_command;
      });
      UIkit.modal("#update-command").show();
    }
  },

  mounted() {
    this.$command = this.$resource(
      "api/coffee/command{/id}",
      {},
      {},
      {
        before: () => {
          this.loading = true;
        },
        after: () => {
          this.loading = false;
        }
      }
    );

    this.$coffee = this.$resource(
      "api/coffee/coffee",
      {},
      {},
      {
        before: () => {
          this.loading = true;
        },
        after: () => {
          this.loading = false;
        }
      }
    )

    this.get_command();
  }
};
</script>
