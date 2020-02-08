<template>
    <div id='command-pasta'>
        <!-- Loader -->
        <loader v-show="loading" />

        <!-- Modal for sommary of command -->
        <modal id='sommary-command' :container='true'>
            <template v-slot:header>
                <h3 class='uk-modal-title'>Récapitulatif de la commande</h3>
            </template>
            <template v-slot:body>
                <transition name="slide-top">
                    <div class='uk-width-3-4 uk-margin-auto' v-show="name == '' || first_name == '' || email == '' || phone_number == ''" >
                        <message status='warning' :close='false'>
                            <template v-slot:header>
                                Données personnelles
                            </template>
                            <template v-slot:body>
                                Vous n'avez pas remplis <span class="uk-text-blod">les champs vous concernant</span>, merci de les compléter,
                                ils ne seront utilisés qu'afin de vous contacter et seront supprimés une fois la commande passée.
                            </template>
                        </message>
                    </div>
                </transition>
                <p class="uk-text-center"><span class="uk-text-bold">Vos données personnelles</span></p>
                    <div class="uk-child-width-1-3@m uk-padding-large uk-padding-medium-top uk-flex-center" uk-grid>
                        <div><label for="name">Nom :</label><input type="text" v-model='name' class="uk-input uk-form-width-medium" placeholder="nom" name="name"></div>
                        <div><label for="first_name">Prénom :</label><input type="text" v-model='first_name' class="uk-input uk-form-width-medium" placeholder="prénom" name="first_name"></div>
                        <div><label for="email">Email :</label><input type="text" v-model='email' class="uk-input uk-form-width-medium" placeholder="email" name="email"></div>
                        <div><label for="phone_number">Numéro de téléphone :</label><input type="text" v-model='phone_number' class="uk-input uk-form-width-medium" placeholder="numéro de téléphone" name="phone_number"></div>
                    </div>
                <p class="uk-text-bold uk-text-center uk-text-lead"><span class="uk-label">Total de votre commande : </span> {{ change_price() }} €</p>
                <table class="uk-table uk-table-divider uk-table-stripped uk-table-hovr uk-table-middle">
                    <thead>
                        <tr>
                            <th>Nom du produit</th>
                            <th>Poids séléctionné</th>
                            <th>Quantité commandé</th>
                            <th>Prix du produit</th>
                            <th>Supprimer ce produit</th>
                        </tr>
                    </thead>
                    <transition-group name='slide-top' tag='tbody'>
                        <tr v-for="product in command" :key="product.id">
                            <td>{{ product.name }}</td>
                            <td>{{ product.weight  + ' ' + get(product, 'unit') }}</td>
                            <td><input type="number" class="uk-input uk-form-width-small" v-model="product.amount"></td>
                            <td>{{ get(product, 'price') * product.amount }} €</td>
                            <td><button type="button" class="uk-button uk-button-danger uk-button-small" @click.prevent="deleteProduct(product)">Supprimer ce produit</button></td>
                        </tr>
                    </transition-group>
                </table>
            </template>
            <template v-slot:footer>
                <button class="uk-button uk-button-primary" type="submit" :disabled="name === '' || first_name === '' || email === '' || phone_number === '' || command.length == 0" @click.prevent="commandProduct()">Commander</button>
                <button class="uk-button uk-button-default uk-modal-close uk-margin-large-left" type="button">Annuler</button>
            </template>
        </modal>

         <!-- Messages  -->
        <div id="messages" class="uk-width-2-5@m uk-width-3-4 uk-margin-auto">
            <message v-for="message in messages" :status="message.status" :key="message.id">
                <template v-slot:header>{{ message.header }}</template>
                <template v-slot:body>{{ message.body }}</template>
            </message>
        </div>

        <!-- Form for command -->
        <form class="uk-form-horizontal uk-margin-large-bottom" id="form-coffee">
            <!-- Personnals informations -->
            <fieldset class="uk-fieldset uk-margin-medium-bottom">
                <legend class="uk-legend uk-text-center uk-margin-large-bottom">Informations</legend>
                <div class="uk-margin-large-bottom uk-width-1-2@l uk-margin-auto uk-child-width-1-3@l uk-child-width-2-5@m uk-grid uk-flex-center" uk-grid>
                    <div><label for='name' class="uk-form-label">Votre nom</label><input name="name" type="text" v-model="name" class="uk-input" placeholder="nom"></div>
                    <div><label for='first-name' class="uk-form-label">Votre prénom</label><input type="text" name="first-name" v-model="first_name" class="uk-input" placeholder="prénom"></div>
                    <div><label for="email" class="uk-form-label">Votre email</label><input type="email" name="email" v-model="email" class="uk-input" placeholder="email"></div>                
                    <div><label for='phone-number' class="uk-form-label">Votre numéro de téléphone</label><input v-model='phone_number' type='text' class="uk-input" placeholder="numéro de téléphone"></div>
                </div>
                <!-- Total price -->
                <p class="uk-width-1-5@m uk-width-3-5 uk-margin-auto uk-text-bold uk-text-lead"><span class="uk-label">Total de votre commande : </span> {{ change_price() }} €</p>
            </fieldset>

                <!-- Command of product -->
                <transition-group name='slide-top' tag='div' uk-grid class="uk-grid-medium uk-width-auto uk-width-3-4@m uk-margin-auto">
                    <div v-for="product in command" class="uk-margin-xlarge-bottom uk-margin-auto uk-card-default uk-padding-large slide-top-item" :key="product.id" :id="'a' + product.id">
                        <pasta-select :products='products' :product='product' />
                        <div class="uk-text-center">
                            <button class="uk-button uk-button-danger" @click.prevent='deleteProduct(product)'>Supprimer ce produit</button>
                        </div>
                    </div>
                </transition-group>

            <!-- Footer of form -->
            <div class="uk-width-1-2 uk-text-center uk-margin-auto" v-if="command.length != 0">
                <button class="uk-button uk-button-large uk-button-secondary" id="command-button" @click.prevent="show_recap()" v-bind:disabled="!addProductButtonAvailable">{{ text_button_command_product }}</button>
            </div>
        </form>

        <!-- List of product -->
        <div class="uk-width-3-4@m uk-child-width-1-2@m uk-text-center uk-margin-auto uk-grid-match" uk-grid uk-height-match="target: > div > .uk-card-footer > *">
            <div v-for="product in products" :key='product.id'>
                <pasta-card>
                    <template v-slot:header>
                        <h3 class='uk-card-title uk-text-center'>{{ product.name }} <img v-show="product.organic_agriculture" class="uk-margin-left" uk-img src="../../assets/Images/Pasta/ab_symbole.png"  alt="logo agriculture biologique" width="50"></h3>
                    </template>
                    <template v-slot:body>
                        <div class="uk-text-justify">
                            <span class="uk-text-bold">Poids disponible : </span>
                            <ul class='uk-list uk-list-bullet'>
                                <li v-for="type in product.available_product" :key="type.weight">
                                    {{ type.weight }} {{ type.unit }} pour {{ type.price }} €<br>
                                    <div class="uk-text-muted">
                                        {{ type.category.name }}<br>
                                        {{ type.category.description }}
                                    </div>
                                </li>
                            </ul>
                        </div>
                        <div v-html="product.description"></div>
                    </template>
                    <template v-slot:footer>
                       <button class='uk-button uk-button-primary add-product' v-bind:disabled="!addProductButtonAvailable" @click.prevent="addProduct(product)">{{ text_button_add_product }}</button>
                    </template>
                </pasta-card>
            </div>
        </div>
    </div>
</template>

<script>
import Loader from '../utility/Loader'
import Message from '../utility/Message'
import Modal from '../utility/Modal'

import PastaCard from './PastaCard'
import PastaSelect from './PastaSelect'

export default {
    name: 'CommandPasta',

    components: {
        // utility
        Loader,
        Message,
        Modal,

        // Product
        PastaCard,
        PastaSelect

    },

    data() {
        return {
            // Utility
            loading: false,
            messages: [],

            // Personnals informations
            first_name: String(),
            name: String(),
            email: String(),
            phone_number: String(),

            // Command
            index: 0,
            command: [],
            products: [],
            text_button_command_product: 'Commander',
            text_button_add_product: 'Ajouter ce produit à ma commande'

        }
    },

    computed: {
        addProductButtonAvailable () {
            for (let i = 0; i < this.command.length; i++) {
                const product = this.command[i];
                if (product.name == 'Séléctionner un produit' || product.weight == 'Séléctionner un poids' || product.amount == 0) {
                    this.text_button_add_product = "Veuillez d'abord compléter votre commande avant d'ajouter d'autres produits"
                    this.text_button_command_product = "Veuillez d'abord compléter les produits que vous avez séléctionner avant de valider votre commande"
                    return false
                }
            }
            this.text_button_command_product = 'Commander'
            this.text_button_add_product = 'Ajouter ce produit à ma commande'
            return true
        },
    },

    methods: {
        change_price() {
            let price = 0
            this.command.forEach(product => {
                if (product.default_product !== undefined && product.weight !== 'Séléctionner le poids')
                {   
                    price += Object.values(product.default_product.available_product).filter(p => p.weight == product.weight)[0]['price'] * product.amount
                }

            })
            return Math.round(price * 1000) / 1000
        },

        get (product, why) {
            if (product.default_product !== undefined && product.weight !== 'Séléctionner le poids'){
                return Object.values(product.default_product.available_product).filter(p => p.weight == product.weight)[0][why]
            }
            return 0
        },

        addProduct (product) {
            this.command.push({
                id: this.index,
                name: product.name,
                weight: 'Séléctionner le poids',
                amount: 0
            })
            this.index ++
            UIkit.scroll('.add-product').scrollTo('#form-coffee')
        },

        deleteProduct (product) {
            this.command = this.command.filter(p => p !== product)
            this.index --
        },

        show_recap () {
            UIkit.modal('#sommary-command').show()
        },

        commandProduct () {
            UIkit.modal('#sommary-command').hide()
            this.loading = true
            let formData = new FormData()

            if (this.name != '' && this.first_name != '' && this.email != '' && this.phone_number != '')
            {
                formData.append('name', this.name)
                formData.append('first_name', this.first_name)
                formData.append('email', this.email)
                formData.append('phone_number', this.phone_number)
            }

            this.command.forEach(product => {
                let metaData = product.name + '\\' + product.weight + '\\' + product.amount
                formData.append(product.id, metaData)
                
            })

            this.$resource('pate/create-command').save({}, formData).then(response => {
                const status = response.body['status']
                const header = response.body['header']
                const body = response.body['body']

                if (status === 'success') {
                    this.command = []
                    this.index = 0
                    this.name = ''
                    this.first_name = ''
                    this.email = ''
                    this.phone_number = ''
                }

                this.messages.push({
                    id: parseInt(Math.random() * 1000),
                    status: status,
                    header: header,
                    body: body
                })
                this.loading = false
                UIkit.scroll('#command-button', {offset: 250}).scrollTo['#messages']
            })
        }
    },

    mounted() {
        this.$pasta = this.$resource('pate/get-products', {}, {}, {
            before: () => {this.loading = true},
            after: () => {this.loading = false}
        }),

        this.$pasta.query().then(
            (response) => {
                this.products = response.data
            },
            (response) => {
                this.messages.push({
                    id: parseInt(Math.random() * 1000),
                    status: 'danger',
                    header: 'Erreur interne',
                    body: "La liste des produits n'a pas pu être récupéré, merci  de réessayer et de me contacter si besoin."
                })
            }
        )
    },

}
</script>