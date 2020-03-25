<template>
  <div id="table-update-coffee">
    <form action="#">
      <p class="uk-text-center">
        <span class="uk-text-bold">Vos données personnelles</span>
      </p>
      <transition name="slide-top">
        <div
          class="uk-width-3-4@m uk-width-3-4 uk-margin-auto"
          v-show="command.name == '' || command.first_name == '' || command.email == '' || command.phone_number == ''"
        >
          <message :status="'warning'" :close="false">
            <template v-slot:header>Données personnelles</template>
            <template v-slot:body>
              Vous n'avez pas remplis
              <span
                class="uk-text-bold"
              >les champs concernant la personne qui commande</span>, merci de les compléter, ils ne seront utilisés
              qu'afin de contacter la personne.
            </template>
          </message>
        </div>
      </transition>
      <div class="uk-child-width-1-3@m uk-padding-large uk-flex-center" uk-grid>
        <div>
          <label class="uk-label uk-margin-right" for="name">Nom</label>
          <input
            v-model="command.name"
            type="text"
            class="uk-input uk-form-width-medium"
            placeholder="nom"
            name="name"
          />
        </div>
        <div>
          <label class="uk-label uk-margin-right" for="first_name">Prénom</label>
          <input
            v-model="command.first_name"
            class="uk-input uk-form-width-medium"
            placeholder="prénom"
            type="text"
            name="first_name"
          />
        </div>
        <div>
          <label class="uk-label uk-margin-right" for="email">Email</label>
          <input
            v-model="command.email"
            type="email"
            class="uk-input uk-form-width-medium"
            placeholder="email"
            name="email"
          />
        </div>
        <div>
          <label class="uk-label uk-margin-right" for="phone-number">Numéro de téléphone</label>
          <input
            v-model="command.phone_number"
            type="text"
            class="uk-input uk-form-width-medium"
            placeholder="numéro de téléphone"
            name="phone-number"
          />
        </div>
        <div>
          <span class="uk-label uk-magin-right">Prix à payer</span>
          {{ total_price }} €
        </div>
      </div>
      <table class="uk-table uk-table-divider uk-table-striped">
        <thead>
          <tr>
            <th>Nom du café</th>
            <th>Poids</th>
            <th>Type de mouture</th>
            <th>Quantité</th>
            <th>Prix</th>
            <th>Supprimer</th>
          </tr>
        </thead>
        <transition-group name="slide-top" tag="tbody">
          <tr v-for="com in command.command" :key="com.id">
            <td>
              <select name="coffees" class="uk-select" v-model="com.coffee">
                <option :value="com.coffee">{{ com.coffee.farm_coop }}</option>
                <option
                  v-for="coffee in coffees.filter(cof => cof.farm_coop != com.coffee.farm_coop)"
                  :key="coffee.id"
                  :value="coffee"
                >{{ coffee.farm_coop }}</option>
              </select>
              <button
                class="uk-button uk-button-text"
                type="button"
                @click.prevent="display_info_coffee(com.coffee.id)"
              >En savoir plus</button>
            </td>
            <td>
              <select name="weight" class="uk-select" v-model="com.weight">
                <option :value="com.weight">{{ com.weight }}</option>
                <option v-for="wei in weight.filter(w => w != com.weight)" :key="wei">{{ wei }}</option>
              </select>
            </td>
            <td>
              <select name="sort" class="uk-select" v-model="com.sort">
                <option :value="com.sort">{{ com.sort.name }}</option>
                <option
                  v-for="sort in com.coffee.available_type.filter(t => t.name != com.sort.name)"
                  :key="sort.id"
                  :value="sort"
                >{{ sort.name }}</option>
              </select>
            </td>
            <td>
              <input type="number" class="uk-input" v-model="com.quantity" />
            </td>
            <td>{{ price(com) }} €</td>
            <td>
              <button
                class="uk-button uk-button-danger uk-button-small"
                type="button"
                @click.prevent="delete_command(com.id)"
              >Supprimer ce café de la commande</button>
            </td>
          </tr>
        </transition-group>
      </table>
      <button class="uk-button uk-button-text" @click.prevent="add_command()">
        Ajouter un café à la commande
        <span uk-icon="plus"></span>
      </button>
    </form>
    <modal
      v-show="Object.keys(coffee_info).lenght != 0"
      id="coffee-info"
      :container="true"
      :center="true"
      :close_button="false"
      :bg_close="false"
    >
      <template #header>
        <h3 class="uk-text-center">{{ coffee_info.farm_coop }}</h3>
      </template>
      <template #body>
        <div uk-grid class="uk-grid-large uk-child-width-expand uk-margin-auto">
          <div>
            <span class="uk-text-bold">Région de culture :</span>
            {{ coffee_info.region }}
            <br />
            <span class="uk-text-bold">Procéder de fabrication :</span>
            {{ coffee_info.process }}
            <br />
            <span class="uk-text-bold">Variété :</span>
            {{ coffee_info.variety }}
          </div>
          <div>
            <span class="uk-text-bold">Origine du café :</span>
            {{ coffee_info.origin.name }}
            <br />
            <span class="uk-text-bold">Prix au kilo :</span>
            {{ coffee_info.kilogram_price }} €
            <br />
            <span class="uk-text-bold">Prix pour deux cents grammes :</span>
            {{ coffee_info.two_hundred_gram_price }} €
          </div>
          <div>
            <span class="uk-text-bold">Mouture disponible :</span>
            <ul class="uk-list uk-list-bullet">
              <li v-for="type in coffee_info.available_type" :key="type.id">{{ type.name }}</li>
            </ul>
          </div>
        </div>
        <div v-html="coffee_info.description"></div>
      </template>
      <template #footer>
        <button class="uk-button uk-button-default" uk-toggle="#update-command">Retour</button>
      </template>
    </modal>
  </div>
</template>

<script>
import Modal from "../utility/Modal";
import Message from "../utility/Message";

export default {
  name: "TableUpdateCommand",

  props: {
    command: { type: Object, default: {} },
    coffees: { type: Array, default: [] }
  },

  components: {
    Modal,
    Message
  },

  data() {
    return {
      coffee_info: {
        origin: "origin"
      },
      weight: ["200", "1000"]
    };
  },

  computed: {
    total_price () {
      let price = 0
      this.command.command.forEach(com => {
        console.log(com);
        if (com.weight == 200) {
          price += parseFloat(com.coffee.two_hundred_gram_price) * parseFloat(com.quantity)
        }
        else {
          price += parseFloat(com.coffee.kilogram_price) * parseFloat(com.quantity)
        }
        
      });      
      return price

    }
  },

  methods: {
    add_command() {
      this.command.command.push({
        coffee: this.coffees[0],
        id: Date.now(),
        quantity: 0,
        sort: this.coffees[0].available_type[0],
        total: 0,
        weight: 200
      });
    },

    delete_command(id_command) {
      this.command.command = this.command.command.filter(com => {
        return com.id !== id_command;
      });
    },

    display_info_coffee(id_coffee) {
      this.coffee_info = this.coffees.find(co => {
        return co.id == id_coffee;
      });
      UIkit.modal("#coffee-info").show();
    },

    price(command) {
      if (command.weight == 200) {
        return (
          parseFloat(command.coffee.two_hundred_gram_price) *
          parseFloat(command.quantity)
        );
      } else {
        return (
          parseFloat(command.coffee.kilogram_price) *
          parseFloat(command.quantity)
        );
      }
    }
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