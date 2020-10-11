<template>
  <div class="uk-hidden-touch">
    <div
      class="uk-box-shadow-large"
      uk-sticky="sel-target: .uk-navbar-container; cls-active: uk-navbar-sticky; bottom: #transparent-sticky-navbar"
    >
      <nav
        class="uk-navbar-container uk-navbar"
        uk-sticky="sel-target: .uk-navbar-container; cls-active: uk-navbar-sticky; cls-inactive: uk-navbar-primary uk-primary; top: 200"
        uk-navbar
      >
        <div class="uk-navbar-left">
          <a class="uk-navbar-toggle" href="#menu" uk-toggle>
            <span uk-navbar-toggle-icon></span>
            <span class="uk-margin-small-left">Menu</span>
          </a>
        </div>
        User
        <div class="uk-navbar-right uk-margin-right">
          <a href="#" class="uk-text uk-navbar-toggle"
            ><span uk-icon="icon: user; ratio: 1.5"></span
          ></a>
          <div class="uk-navbar-dropdown" uk-dropdown>
            <ul class="uk-nav uk-navbar-dropdown-nav">
              <li class="uk-nav-header"></li>
              <li>
                <a href="{% url 'change_password' %}"
                  >Changer de mot de passe</a
                >
              </li>
              <li>
                <a href="{% url 'disconnection_connection' %}"
                  >Changer d'utilisateur</a
                >
              </li>
              <li class="uk-nav-divider"></li>
              <li><a href="{% url 'disconnection' %}">Déconnexion</a></li>
            </ul>
          </div>
        </div>
      </nav>
    </div>

    <div id="menu" uk-offcanvas="overlay: true; mode: push">
      <div class="uk-offcanvas-bar uk-flex uk-flex-column">
        <ul class="uk-nav uk-nav-center uk-margin-auto-vertical" uk-nav>
          <li class="uk-parent">
            <a href="#" class="uk-nav-header">Liste des adhérents</a>
          </li>

          <li class="uk-parent">
            <a href="#" class="uk-nav-header"
              ><span
                class="uk-margin-small-right"
                uk-icon="icon: thumbnails"
              ></span
              >Espace administration</a
            >

            <ul
              class="uk-nav uk-nav-sub uk-nav-default uk-nav-parent-icon"
              uk-nav
            >
              <li
                class="uk-parent"
                v-for="adminPanelItem in adminPanelItems"
                :key="adminPanelItem.title"
              >
                <a class="uk-nav-header">{{ adminPanelItem.title }}</a>
                <ul class="uk-nav-sub" v-if="adminPanelItem.subItems">
                  <li
                    v-for="subItem in adminPanelItem.subItems"
                    :key="subItem.name"
                  >
                    <a href="">{{ subItem.name }}</a>
                  </li>
                </ul>
              </li>
            </ul>
          </li>

          <br />

          <li class="uk-parent">
            <a href="#" class="uk-nav-header uk-nav-default"
              ><span
                class="uk-margin-small-right"
                uk-icon="icon: thumbnails"
              ></span
              >Commander</a
            >
            <ul class="uk-nav-sub uk-nav-default">
              <li>
                <a href="">Commander des agrumes</a>
              </li>
              <li>
                <a href="">Commander du café</a>
              </li>
              <li>
                <a href="">Commander des pâtes</a>
              </li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Options, Vue } from 'vue-class-component'

@Options({
  data (): Object {
    return {
      adminPanelItems: [
        {
          title: 'Articles',
          subItems: [
            {
              name: 'Liste des articles',
              link: ''
            },
            {
              name: 'Créer un article',
              link: ''
            }
          ]
        },
        {
          title: 'Évènements',
          subItems: [
            {
              name: 'Liste des évènements',
              link: ''
            },
            {
              name: 'Créer un évènement',
              link: ''
            }
          ]
        },
        {
          title: 'Carousel',
          subItems: [
            {
              name: 'Liste des carousels',
              link: ''
            },
            {
              name: 'Créer un carousel',
              link: ''
            }
          ]
        }
      ]
    }
  }
})
export default class DefaultNavbar extends Vue {}
</script>
