<template>
	<div id="list-product">
		<loader v-show="loading"></loader>

		<div id="vue-messages" class="uk-width-2-5@m uk-width-3-4 uk-margin-auto uk-margin-xlarge-bottom">
			<message v-show="query_error" :close="false" status="danger">
				<template #header>Erreur interne</template>
				<template #body>
					Une erreur est survenue, cela vient de nous, merci d'actualiser la
					page et de nous contacter si vous rencontrez de nouveau cette erreur.
				</template>
			</message>

			<message v-show="permission_error" :close="false" status="danger">
				<template #header>Accès interdit</template>
				<template #body>
					Il semblerait qui vous n'ayez pas l'autorisation d'accéder à cette
					fonctionnalité du site.
				</template>
			</message>

			<message v-for="message in messages" :key="message.id" :status="message.status">
				<template #header>
					<div v-html="message.header"></div>
				</template>
				<template #body>
					<div v-html="message.body"></div>
				</template>
			</message>
		</div>
		<div class="uk-width-3-5@m uk-margin-auto">
			<div class="uk-margin-medium-bottom">
				<select name="actions" class="uk-select uk-form-width-medium" v-model="action">
					<option value selected>------ ------</option>
					<option v-for="(name, value) in ACTIONS" :value="value" :key="value">{{ name }}</option>
				</select>
				<input
					type="button"
					v-if="action !== ''"
					value="Appliquer"
					class="uk-button uk-button-primary uk-margin-medium-left"
					id="action-button"
					@click="apply_action()"
				/>
			</div>

			<table class="uk-table uk-table-divider uk-striped uk-table-hover uk-table-middle">
				<thead>
					<tr>
						<th class="uk-table-shrink">
							<input
								type="checkbox"
								class="uk-checkbox"
								title="Sélectionner tous les produits"
								v-model="check_all"
							/>
						</th>
						<th>Nom du produit</th>
						<th>
							<span
								uk-tooltip="Si le poids du produit est de 1, cela veut dire que le produit ne se vend pas au poids."
							>Poids du produit</span>
						</th>
						<th>Prix du produit</th>
						<th>
							<span
								uk-tooltip="Défini si ce produit est affiché, ou pas, sur le tableau des commandes."
							>Produit affiché</span>
						</th>
						<th class="uk-table-shrink">Actions</th>
					</tr>
				</thead>
				<tbody>
					<tr v-for="product in products" :key="product.id">
						<td>
							<input type="checkbox" class="uk-checkbox" v-model="product.check" />
						</td>
						<td>{{ product.name }}</td>
						<td>{{ product.weight }} kg</td>
						<td>{{ product.price }} €</td>
						<td v-if="product.display == true">
							<span uk-icon="check"></span>
						</td>
						<td v-else>
							<span uk-icon="close"></span>
						</td>
						<td>
							<a
								href="#"
								:title="'Modifier le produit : ' + product.name"
								uk-icon="icon: refresh; ratio: 1.20"
								class="uk-margin-small-right"
							></a>
							<a :title="'Supprimer le produit : ' + product.name" uk-icon="icon: trash; ratio: 1.20"></a>
						</td>
					</tr>
				</tbody>
			</table>
			<div class="uk-text-center uk-margin-large-top">
				<button
					class="uk-button uk-button-default"
					type="button"
					@click="get_more_product()"
					v-show="display_button_get_more_product"
				>Afficher plus de produit</button>
			</div>
		</div>
	</div>
</template>

<script>
import Loader from "../utility/Loader";
import Message from "../utility/Message";

export default {
	name: "ListProduct",

	props: ["page"],

	data() {
		return {
			// Utility
			loading: false,
			query_error: false,
			permission_error: false,
			messages: Object(),
			display_button_get_more_product: true,

			products: Array(),
			action: String(),

			offset: 0,

			// LIMIT const is number of product add when an user click on button "Afficher plus de produit"
			LIMIT: 10,
			ACTIONS: {
				hide: "Cacher ces produits",
				show: "Afficher ces produits"
			}
		};
	},

	components: {
		Loader,
		Message
	},

	computed: {
		check_all: {
			get() {
				return false;
			},
			set(value) {
				this.products.forEach(product => {
					product.check = value;
				});
			}
		}
	},

	methods: {
		get_more_product() {
			this.offset += parseInt(this.LIMIT);
			this.$product
				.query({ limit: this.LIMIT, offset: this.offset })
				.then(response => {
					this.products = this.products.concat(response.body.results);
					if (response.next === undefined) {
						this.display_button_get_more_product = false;
					}
				});
		},

		apply_action() {
			
			if (this.products.find(product => product.check === true)  === undefined) {
				UIkit.notification("Aucun produit sélctionné. <br>L’action ne peut être appliquée.", {status: "warning", pos: "bottom-right"})
			}
			else {
				let products_check = this.products.filter(product => product.check === true)
				if (this.action === 'hide') {
					products_check.forEach(product => {
						product.display = false	
					})
				}
				else if (this.action === 'show') {
					products_check.forEach(product => {
						product.display = true
					})
				}

				products_check.forEach(product => {
					this.$product.update({id: product.id}, product).then((response) => {
						console.log(response);
					})
				})


			}
		}
	},

	mounted() {
		this.$product = this.$resource(
			"api/citrus/product{/id}",
			{ query: "all" },
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

		this.$product.query({ limit: this.LIMIT }).then(
			response => {
				response.body.results.forEach(product => {
					product.check = false;
				});
				this.products = response.body.results;

				if (response.next !== undefined) {
					this.display_button_get_more_product = false;
				}
			},
			response => {
				if (this.status === "Forbidden" && this.status_code === 403) {
					this.permission_error = true;
				} else {
					this.query_error = true;
				}
			}
		);
	}
};
</script>