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
			<div uk-grid class="uk-margin-large-top">
				<div class="uk-width-2-3">
					<ul v-show="pagination.next !== null || pagination.previous !== null" class="uk-pagination">
						<li><a href="#" type='button'><span uk-pagination-previous></span></a></li>
						<li>{{ pagination.active }}</li>
						<li><a href="" type='button'>{{ pagination.next }}</a></li>
						<li><a href="#" type='button'><span uk-pagination-next></span></a></li>
					</ul>
				</div>
				<form action="#" class="uk-form-horizontal uk-width-1-3 uk-text-right">
					<label for="pagination_limit" class="uk-form-label">Produits par page</label>
					<div class="uk-form-controls uk-margin-small-bottom">
						<select class="uk-select uk-form-width-small" name="pagination_limit" v-model="pagination.limit">
							<option selected value="">-------</option>
							<option value="10">10</option>
							<option value="20">20</option>
							<option value="50">50</option>
							<option value="100">100</option>
						</select>
					</div>
					<input type="button" value="Valider" v-show="pagination.limit !== ''" class="uk-button uk-button-primary uk-button-small" @click="update_limit()">
				</form>
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

			products: Array(),
			action: String(),
			pagination: {
				active: 1,
				next: null,
				previous: null,
				count: Number(),
				limit: 20
			},
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
		},

		ratio () {
			return this.pagination.count / this.pagination.limit
		}
	},

	methods: {
		update_limit () {
			this.$product.get({'limit': this.pagination.limit}).then((response) => {
				this.pagination.next = response.body.next
				this.pagination.previous = response.body.next
				this.pagination.count = response.body.count
				this.products = response.body.results
			})
		}
	},

	mounted() {
		this.$product = this.$resource(
			"api/citrus/product{/id}",
			{query: 'all'},
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

		this.$product.query({limit: this.pagination.limit}).then(
			response => {
				this.pagination.next = response.body.next
				this.pagination.previous = response.body.next
				this.pagination.count = response.body.count

				response.body.results.forEach(product => {
					product.check = false;
				});
				this.products = response.body.results;
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