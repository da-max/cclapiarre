<template>
  <div id="commande-coffees">
    <!-- Loader -->
    <loader v-show="loading"></loader>

    <modal
      v-if="Object.keys(old_command).lenght !== 0"
      id="also-command"
      :container="true"
      :bg_close="false"
      :close_button="false"
    >
      <template #header>
        <h3 class="uk-modal-title">Vous avez déjà commandé !</h3>
      </template>
      <template #body>
        <div class="uk-width-3-4@m uk-width-3-4 uk-margin-auto">
          <message status="warning">
            <template #header>
              Attention
            </template>
            <template #body>
              Une commande avec le même numéro de télephone ou la même adresse mail a été trouvé. Cette commande est affichée ci-dessous,
              <span
                class="uk-text-bold"
              >si elle correspond à une commande que vous avez effectué</span>, il est possible de la remplacer.
              <span class="uk-text-bold uk-text-warning">
                Si cette commande n’a pas été
                passé par vous merci de cliquer sur annuler la commande.
              </span>
            </template>
          </message>
        </div>
        <div class="uk-child-width-1-2 uk-grid-divider" uk-grid>
          <div>
            <h4 class="uk-text-center">Ancienne commande</h4>
            <div class="uk-child-width-1-2" uk-grid>
              <div><span class="uk-label">Nom</span> {{ old_command.name }}</div>
              <div><span class="uk-label">Prénom</span> {{ old_command.first_name }}</div>
              <div><span class="uk-label">Email</span> {{ old_command.email }}</div>
              <div><span class="uk-label">Numéro de télephone</span> {{ old_command.phone_number }}</div>
              <div><span class="uk-label">Total</span> {{old_command.total }} €</div>
            </div>
            <ul class="uk-list">
              <li v-for="command in old_command.command" :key="command.id">
                 <div uk-grid class="uk-child-width-1-2">
                  <div>{{ command.coffee.farm_coop }} ({{ command.sort.name }})</div>
                  <div class="uk-text-right"> {{ command.weight}} gr x {{ command.quantity }} = {{ command.total }} €</div>
                 </div>
              </li>
            </ul>
          </div>
          <div>
            <h4 class="uk-text-center">Nouvelle commande</h4>
            <div class="uk-child-width-1-2" uk-grid>
              <div><span class="uk-label">Nom</span> {{ name }}</div>
              <div><span class="uk-label">Prénom</span> {{ first_name }}</div>
              <div><span class="uk-label">Email</span> {{ email }}</div>
              <div><span class="uk-label">Numéro de télephone</span> {{ phone_number }}</div>
              <div><span class="uk-label">Total</span> {{ change_price() }}€</div>
            </div>
            <ul class="uk-list">
              <ul class="uk-list">
              <li v-for="command in coffees_command" :key="command.id">
                <div uk-grid class="uk-child-width-1-2">
                  <div>{{ command.coffee.farm_coop }} ({{ command.type.name }})</div>
                  <div class="uk-text-right" v-if="command.weight == 200"> {{ command.weight }} gr x {{ command.quantity }} = {{ Math.round(command.quantity * command.coffee.two_hundred_gram_price * 100) / 100 }} €</div>
                  <div class="uk-text-right" v-else> {{ command.weight }} gr x {{ command.quantity }} = {{ Math.round(command.quantity * command.coffee.kilogram_price * 100) / 100 }} €</div>
                </div>
              </li>
            </ul>
            </ul>
          </div>
        </div>
      </template>
    </modal>

    <!-- Modal for recap command -->
    <modal id="command-recap" :container="true">
      <template #header>
        <h3 class="uk-modal-title">Récapitulatif de la comande</h3>
      </template>
      <template #body>
        <transition name="slide-top">
          <div
            class="uk-width-3-4@m uk-margin-auto"
            v-show="name == '' || first_name == '' || email == '' || phone_number == ''"
          >
            <message :status="'warning'" :close="false">
              <template #header>Données personnelles</template>
              <template #body>
                Vous n'avez pas remplis
                <span class="uk-text-bold">les champs vous concernant</span>, merci de les compléter, ils ne seront utilisés
                qu'afin de vous contacter.
              </template>
            </message>
          </div>
        </transition>
        <p class="uk-text-center">
          <span class="uk-text-bold">Vos données personnelles</span>
        </p>
        <br />
        <ul class="uk-child-width-1-3@m uk-padding-large uk-flex-center" uk-grid>
          <div>
            <label for="name">Nom :</label>
            <input
              v-model="name"
              type="text"
              class="uk-input uk-form-width-medium"
              placeholder="nom"
              name="name"
            />
          </div>
          <div>
            <label for="first_name">Prénom :</label>
            <input
              v-model="first_name"
              class="uk-input uk-form-width-medium"
              placeholder="prénom"
              type="text"
              name="first_name"
            />
          </div>
          <div>
            <label for="email">Email :</label>
            <input
              v-model="email"
              type="email"
              class="uk-input uk-form-width-medium"
              placeholder="email"
              name="email"
            />
          </div>
          <div>
            <label for="phone-number">Numéro de téléphone :</label>
            <input
              v-model="phone_number"
              type="text"
              class="uk-input uk-form-width-medium"
              placeholder="numéro de téléphone"
              name="phone-number"
            />
          </div>
        </ul>
        <p class="uk-text-bold uk-text-center uk-text-lead">
          <span class="uk-label">Total de votre commande :</span>
          {{ change_price() }} €
        </p>
        <table class="uk-table uk-table-divider uk-table-striped uk-table-hover uk-table-middle">
          <thead>
            <tr>
              <th>Nom du café</th>
              <th>Poids du café</th>
              <th>Type de café</th>
              <th>Quantité de café</th>
              <th>Prix du café</th>
              <th>Supprimer ce café</th>
            </tr>
          </thead>
          <transition-group name="slide-top" tag="tbody">
            <tr v-for="coffee in coffees_command" :key="coffee.id">
              <td>{{ coffee.coffee.farm_coop }}</td>
              <td>{{ coffee.weight }}</td>
              <td>{{ coffee.type.name }}</td>
              <td>
                <input type="number" class="uk-input uk-form-width-small" v-model="coffee.quantity" />
              </td>
              <td
                v-if="coffee.weight == 200 && coffee.coffee"
              >{{ Math.round(coffee.quantity * coffee.coffee.two_hundred_gram_price * 100)/100 }} €</td>
              <td
                v-else-if="coffee.weight == 1000 && coffee.coffee"
              >{{ Math.round(coffee.quantity * coffee.coffee.kilogram_price * 100)/100 }} €</td>
              <td>
                <button
                  class="uk-button uk-button-small uk-button-danger"
                  @click.prevent="deleteCoffee(coffee)"
                >Supprimer ce café</button>
              </td>
            </tr>
          </transition-group>
        </table>
      </template>
      <template #footer>
        <button
          class="uk-button uk-button-primary"
          type="submit"
          :disabled="name === '' || first_name === '' || email === '' || phone_number === ''"
          @click.prevent="commandCoffee()"
        >Commander</button>
        <button
          class="uk-button uk-button-default uk-modal-close uk-margin-large-left"
          type="button"
        >Annuler</button>
      </template>
    </modal>

    <!-- Messages  -->
    <div id="messages" class="uk-width-2-5@m uk-width-3-4 uk-margin-auto">
      <message v-for="message in messages" :status="message.status" :key="message.id">
        <template #header>{{ message.header }}</template>
        <template #body>{{ message.body }}</template>
      </message>
    </div>

    <!-- Form for command -->
    <form class="uk-form-horizontal uk-margin-large-bottom" id="form-coffee">
      <!-- Personnals informations -->
      <fieldset class="uk-fieldset">
        <legend class="uk-legend uk-text-center uk-margin-large-bottom">Informations</legend>
        <div
          class="uk-margin-large-bottom uk-width-1-2@l uk-margin-auto uk-child-width-1-3@l uk-child-width-2-5@m uk-grid uk-flex-center"
          uk-grid
        >
          <div>
            <label for="name" class="uk-form-label">Votre nom</label>
            <input name="name" type="text" v-model="name" class="uk-input" placeholder="nom" />
          </div>
          <div>
            <label for="first-name" class="uk-form-label">Votre prénom</label>
            <input
              type="text"
              name="first-name"
              v-model="first_name"
              class="uk-input"
              placeholder="prénom"
            />
          </div>
          <div>
            <label for="email" class="uk-form-label">Votre email</label>
            <input type="email" name="email" v-model="email" class="uk-input" placeholder="email" />
          </div>
          <div>
            <label for="phone-number" class="uk-form-label">Votre numéro de téléphone</label>
            <input
              v-model="phone_number"
              type="text"
              class="uk-input"
              placeholder="numéro de téléphone"
            />
          </div>
        </div>
        <!-- Total price -->
        <p class="uk-width-1-5@m uk-width-3-5 uk-margin-auto uk-text-bold uk-text-lead">
          <span class="uk-label">Total de votre commande :</span>
          {{ change_price() }} €
        </p>
      </fieldset>

      <!-- Coffee -->
      <transition-group
        name="slide-top"
        tag="div"
        uk-grid
        class="uk-grid-medium uk-width-auto uk-width-5-6@m uk-width-3-4@l uk-margin-auto"
      >
        <div
          v-for="coffee in coffees_command"
          class="uk-margin-xlarge-bottom uk-margin-auto uk-card-default uk-padding-large slite-top-item"
          :key="coffee.id"
          :id="'a' + coffee.id"
        >
          <coffee-select :coffees="coffees" :coffee="coffee"></coffee-select>
          <div class="uk-text-center">
            <button
              class="uk-button uk-button-danger"
              @click.prevent="deleteCoffee(coffee)"
            >Supprimer ce café</button>
          </div>
        </div>
      </transition-group>

      <!-- Footer of form -->
      <div
        class="uk-width-1-2 uk-text-center uk-margin-auto uk-margin-medium-top"
        v-if="coffees_command.length != 0"
      >
        <button
          class="uk-button uk-button-large uk-button-secondary"
          id="command-button"
          @click.prevent="show_recap()"
          v-bind:disabled="!addCoffeeButtonAvailable"
        >{{ text_button_command_coffee }}</button>
      </div>
    </form>

    <!-- List of coffee -->
    <div class="uk-margin-auto uk-width-2-3@l">
      <coffee-card v-for="coffee in coffees" :key="coffee.id">
        <template #header>
          <h3 class="uk-card-title uk-text-center">{{ coffee.farm_coop }}</h3>
        </template>
        <template #body>
          <div uk-grid class="uk-grid-large uk-child-width-expand uk-margin-auto">
            <div>
              <span class="uk-text-bold">Région de culture :</span>
              {{ coffee.region }}
              <br />
              <span class="uk-text-bold">Procéder de fabrication :</span>
              {{ coffee.process }}
              <br />
              <span class="uk-text-bold">Variété :</span>
              {{ coffee.variety }}
            </div>
            <div>
              <span class="uk-text-bold">Origine du café :</span>
              {{ coffee.origin.name }}
              <br />
              <span class="uk-text-bold">Prix au kilo :</span>
              {{ coffee.kilogram_price }} €
              <br />
              <span class="uk-text-bold">Prix pour deux cents grammes :</span>
              {{ coffee.two_hundred_gram_price }} €
            </div>
            <div>
              <span class="uk-text-bold">Mouture disponible :</span>
              <ul class="uk-list uk-list-bullet">
                <li v-for="type in coffee.available_type" :key="type.id">{{ type.name }}</li>
              </ul>
            </div>
          </div>
          <div v-html="coffee.description"></div>
        </template>
        <template #footer>
          <button
            class="uk-button uk-button-primary"
            id="add-coffee"
            v-bind:disabled="!addCoffeeButtonAvailable"
            @click.prevent="addCoffee(coffee)"
          >{{ text_button_add_coffee }}</button>
        </template>
      </coffee-card>
    </div>
  </div>
</template>
<script>
import CoffeeSelect from "./CoffeeSelect";
import CoffeeCard from "./CoffeeCard";
import Message from "../utility/Message";
import Loader from "../utility/Loader";
import Modal from "../utility/Modal";

export default {
  name: "CommandCoffees",

  components: {
    CoffeeSelect,
    CoffeeCard,
    Message,
    Loader,
    Modal
  },

  data() {
    return {
      index: 0,
      coffees_command: [],
      coffees: [],
      text_button_add_coffee: "Ajouter ce café à ma commande",
      text_button_command_coffee: "Commander",
      loading: false,
      messages: [],
      name: "",
      first_name: "",
      email: "",
      phone_number: String(),
      price: 0,
      old_command: {}
    };
  },

  computed: {
    addCoffeeButtonAvailable() {
      for (let i = 0; i < this.coffees_command.length; i++) {
        const coffee = this.coffees_command[i];
        if (
          coffee.farm_coop == "Sélectionner un café" ||
          coffee.weight == "Sélectionner le poids" ||
          coffee.type == "Sélectionner le type de café" ||
          coffee.quantity == 0
        ) {
          this.text_button_add_coffee =
            "Veuillez d'abord compléter votre commande avant d'ajouter d'autre café.";
          this.text_button_command_coffee =
            "Veuillez d'abord compléter les cafés que vous avez séléctionner avant de valider votre commande";
          return false;
        }
      }
      this.text_button_command_coffee = "Commander";
      this.text_button_add_coffee = "Ajouter ce café à ma commande";
      return true;
    }
  },

  methods: {
    change_price() {
      let price = 0;
      this.coffees_command.forEach(coffee => {
        if (coffee.weight == 200 && coffee.coffee !== undefined) {
          price += coffee.coffee.two_hundred_gram_price * coffee.quantity;
        } else if (coffee.weight == 1000 && coffee.coffee !== undefined) {
          price += coffee.coffee.kilogram_price * coffee.quantity;
        }
      });
      return Math.round(price * 1000) / 1000;
    },

    addCoffee(coffee) {
      this.coffees_command.push({
        id: this.index,
        coffee: coffee,
        weight: "Sélectionner le poids",
        type: "Sélectionner le type de café",
        quantity: 0
      });
      let offset = -45 + (this.index ^ (4 * -30));
      UIkit.scroll("#add-coffee", { offset: offset }).scrollTo("#form-coffee");
      this.index++;
    },

    deleteCoffee(coffee) {
      this.coffees_command = this.coffees_command.filter(c => c !== coffee);
      this.index--;
    },

    show_recap() {
      UIkit.modal("#command-recap").show();
    },

    commandCoffee() {
      UIkit.modal("#command-recap").hide();
      this.loading = true;
      let data = Object();

      if (
        this.name != "" &&
        this.first_name != "" &&
        this.email != "" &&
        this.phone_number != ""
      ) {
        data.name = this.name;
        data.first_name = this.first_name;
        data.email = this.email;
        data.phone_number = this.phone_number;
      }

      data.command = Array();

      this.coffees_command.forEach(command => {
        let metadata = {
          id_coffee: command.coffee.id,
          weight: parseInt(command.weight),
          sort: command.type.id,
          quantity: parseInt(command.quantity)
        };
        data.command.push(metadata);
      });

      this.$command.save({}, data).then(
        response => {
          if (response.data[0] && response.data[0].status == "also_command") {
            this.old_command = response.data[1];
            UIkit.modal("#also-command").show();
          } else {
            this.messages.push(response.data);
            if (response.data.status == "success") {
              this.coffees_command = [];
              this.name = this.first_name = this.email = this.phone_number = "";
            }
          }
        },
        reponse => {
          this.messages.push({
            id: parseInt(Math.random() * 1000),
            status: "danger",
            header: "Erreur interne",
            body:
              "Une erreur est survenue, merci de réessayer et de me contacter si besoin."
          });
          UIkit.scroll("#command-button", { offset: 250 }).scrollTo(
            "#messages"
          );
        }
      );
    }
  },

  mounted() {
    (this.$coffee = this.$resource(
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
    )),
      (this.$command = this.$resource(
        "api/coffee/command",
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
      ));
    this.$coffee.query().then(
      response => {
        this.coffees = response.data;
      },
      response => {
        this.messages.push({
          id: parseInt(Math.random() * 1000),
          status: "danger",
          header: "Erreur interne",
          body:
            "La liste des cafés n'a pas pu ếtre récupéré, merci de recharger la page est de me contacter si besoin."
        });
        UIkit.scroll("#command-button", { offset: 250 }).scrollTo("#messages");
      }
    );
  }
};
</script>

<style>
.slide-top-enter-active {
  animation: slide-top 1s;
}

.slide-top-leave-active {
  animation: slide-top 0.5s reverse;
}

@keyframes slide-top {
  0% {
    opacity: 0;
    transform: translateY(-20%);
  }

  100% {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>