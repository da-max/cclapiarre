import Vue from "vue";
import VueRouter from "vue-router";

Vue.use(VueRouter);

const routes = [
  {
    path: "/cafe/commander-du-cafe",
    name: "coffee_command",
    component: function() {
      return import("../views/CoffeeCommand.vue");
    },
  },
  {
    path: "/agrumes/commander-des-agrumes",
    name: "citrus_command",
    component: function() {
      return import("../views/CitrusCommand.vue");
    },
  },
  {
    path: "/agrumes/liste-des-produits",
    name: "citrus_list_product",
    component: function() {
      return import("../views/CitrusProductList.vue");
    },
  },
  {
    path: "/agrumes/modifier-un-produit/:product_id",
    name: "citrus_update_product",
    component: function() {
      return import("../views/CitrusProductUpdate.vue");
    },
  },
  {
    path: "/agrumes/ajouter-un-produit",
    name: "citrus_add_product",
    component: function() {
      return import("../views/CitrusProductAdd.vue");
    },
  },
  {
    path: "/pate/commander-des-pates",
    name: "pasta_command",
    component: function() {
      return import("../views/PastaCommand.vue");
    },
  },
  {
    path: "/cafe/liste-des-commandes",
    name: "coffee_list",
    component: function() {
      return import("../views/CoffeeCommandList.vue");
    },
  },
  {
    path: "**",
    redirect: (to) => {
      window.location.href = "/";
    },
  },
  /* '../views/About.vue')
    }
  },
  {
    path: '/a',
    name: 'pageA',
    component: function () {
      return import('../views/PageA.vue')
    },
    children: [
      {
        path: 'c',
        name: 'a.c',
        component: PageC
      },
      {
        path: 'b',
        name: 'a.b',
        component: PageB
      }
    ]
  }, 
  {
    path: '*',
    redirect: '/'
  }*/
  /*{
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: function () {
      return import(/* webpackChunkName: "about" */
];

const router = new VueRouter({
  mode: "history",
  base: "/",
  routes,
});

export default router;
