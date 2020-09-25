import Vue from 'vue';
import VueRouter from 'vue-router';

Vue.use(VueRouter);

const routes = [
  {
    path: '/cafe/commander-du-cafe',
    name: 'coffee_command',
    component: () => import('../views/CoffeeCommand.vue')
  },
  {
    path: '/agrumes/commander-des-agrumes',
    name: 'citrus_command',
    component: () => import('../views/CitrusCommand.vue')
  },
  {
    path: '/agrumes/liste-des-produits',
    name: 'citrus_list_product',
    component: () => import('../views/CitrusProductList.vue')
  },
  {
    path: '/agrumes/modifier-un-produit/:productId',
    name: 'citrus_update_product',
    component: () => import('../views/CitrusProductUpdate.vue')
  },
  {
    path: '/agrumes/ajouter-un-produit',
    name: 'citrus_add_product',
    component: () => import('../views/CitrusProductAdd.vue')
  },
  {
    path: '/pate/commander-des-pates',
    name: 'pasta_command',
    component: () => import('../views/PastaCommand.vue')
  },
  {
    path: '/cafe/liste-des-commandes',
    name: 'coffee_list',
    component: () => import('../views/CoffeeCommandList.vue')
  },
  {
    path: '**',
    redirect: to => {
      window.location.href = '/';
    }
  }
];

const router = new VueRouter({
  mode: 'history',
  base: '/',
  routes
});

export default router;
