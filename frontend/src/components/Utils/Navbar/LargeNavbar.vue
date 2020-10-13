<template>
  <div class="uk-visible@m uk-hidden-touch">
    <div
      class="uk-box-shadow-large"
      uk-sticky="sel-target: .uk-navbar-container; cls-active: uk-navbar-sticky; bottom: #transparent-sticky-navbar"
    >
      <nav
        class="uk-navbar-container"
        uk-sticky="sel-target: .uk-navbar-container; cls-active: uk-navbar-sticky; cls-inactive: uk-navbar-primary uk-primary; top: 200"
        uk-navbar
      >
        <div class="uk-navbar-center">
          <ul class="uk-navbar-nav">
            <li><a href="{% url 'home' %}">Accueil</a></li>
            <a class="uk-navbar-item uk-logo"
              ><img
                src="{% static 'Images/logo.png' %}"
                width="75px"
                height="75px"
            /></a>
            <li>
              <a href="#">Espace adhérent</a>
              <div class="uk-navbar-dropdown">
                <ul class="uk-nav uk-navbar-dropdown-nav">
                  <li>
                    <a href="{% url 'list_user' %}">Liste des adhérents</a>
                  </li>
                  <li>
                    <a href="{% url 'list_article_private' %}">Actualité</a>
                  </li>
                </ul>
              </div>
            </li>
            <li>
              <a href="#administration-space" uk-toggle
                >Espace administration</a
              >
            </li>
            <li>
              <a href="#">Commander</a>
              <div class="uk-navbar-dropdown">
                <ul class="uk-nav uk-navbar-dropdown-nav">
                  <li>
                    <a href="{% url 'citrus:new_command_citrus' %}"
                      >Commander des agrumes</a
                    >
                  </li>
                  <li>
                    <a href="{% url 'new_coffee_command'%}"
                      >Commander du café</a
                    >
                  </li>
                  <li>
                    <a href="{% url 'pasta_command' %}">Commander des pâtes</a>
                  </li>
                </ul>
              </div>
            </li>
            <li
              class="uk-position-relative uk-position-right uk-margin-right uk-margin-large-left"
            >
              <UserOptions></UserOptions>
            </li>
          </ul>
        </div>
      </nav>
    </div>

    <div id="administration-space" uk-offcanvas="overlay: true">
      <div class="uk-offcanvas-bar">
        <ul class="uk-nav uk-nav-default uk-nav-parent-icon" uk-nav>
          <li class="uk-active uk-text-center uk-text-bold">
            <a href="#">Espace administration</a>
          </li>
          <br />
          <li
            class="uk-parent"
            v-for="adminPanelItem in adminPanelItems"
            :key="adminPanelItem.title"
          >
            <a class="uk-nav-header">{{ adminPanelItem.title }}</a>
            <ul class="uk-nav-sub">
              <li
                v-for="subItem in adminPanelItem.subItems"
                :key="subItem.name"
              >
                <a :href="subItem.link">{{ subItem.name }}</a>
              </li>
            </ul>
          </li>

          <li><a href="/admin/">Administration</a></li>
        </ul>
      </div>
    </div>
  </div>
</template>
<script lang="ts">
import { Options, Vue } from 'vue-class-component'
import { NavbarItem } from '@/types/index'

import UserOptions from '@/components/Utils/Navbar/UserOptions.vue'

@Options({
  props: {
    adminPanelItems: Array
  },
  components: {
    UserOptions
  }
})

export default class LargeNavbar extends Vue {
  adminPanelItems!: Array<NavbarItem>
}
</script>
