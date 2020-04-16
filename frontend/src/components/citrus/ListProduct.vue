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
					<option value="" selected>------ ------</option>
					<option v-for="(name, value) in ACTIONS" :value="value" :key="value">{{ name }}</option>
				</select>
				<input type="button" v-if="action !== ''" value="Appliquer" class="uk-button uk-button-primary uk-margin-medium-left">
			</div>

			<table class="uk-table uk-table-divider uk-striped uk-table-hover uk-table-middle">
				<thead>
					<tr>
						<th class="uk-table-shrink">
							<input type="checkbox" class="uk-checkbox" title='Sélectionner tous les produits' v-model="check_all" />
						</th>
						<th>Nom du produit</th>
						<th>Poids du produit</th>
						<th>Prix du produit</th>
						<th>Produit affiché</th>
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
		</div>
	</div>
</template>

<script>
import Loader from "../utility/Loader";
import Message from "../utility/Message";

export default {
	name: "ListProduct",

	data() {
		return {
			// Utility
			loading: false,
			query_error: false,
			permission_error: false,
			messages: Object(),

			products: Array(),
			products_check: Object(),
			action: String(),
			ACTIONS: {
				'hide': 'Cacher ces produits',
				'show': 'Afficher ces produits',
			}
		};
	},

	components: {
		Loader,
		Message,
		LineListProduct
	},

	computed: {
		check_all: {
			get() {
				return false;
			},
			set(value) {
					console.log(value);

				this.products.forEach(product => {									
					product.check = value;
				});
			}
		}
	},

	mounted() {
		this.$product = this.$resource(
			"api/citrus/product{/id}",
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

		this.$product.query({ query: "all" }).then(
			response => {
				response.body.forEach(product => {
					product.check = false
				});
				this.products = response.body;
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