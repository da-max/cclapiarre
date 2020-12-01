<template>
  <div>
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
        <UserOptions
          v-if="currentUser && currentUser.username"
          class="uk-navbar-right uk-margin-right"
        ></UserOptions>
      </nav>
    </div>

    <div id="menu" uk-offcanvas="overlay: true; mode: push">
      <div class="uk-offcanvas-bar uk-flex uk-flex-column">
        <ul class="uk-nav uk-nav-center uk-margin-auto-vertical" uk-nav>
          <li class="uk-parent">
            <router-link :to="{ name: 'Home' }">Accueil</router-link>
          </li>
          <li class="uk-parent">
            <router-link :to="{ name: 'MemberList' }" class="uk-nav-header"
              >Liste des adhérents</router-link
            >
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

          <li class="uk-parent">
            <a href="#" class="uk-nav-header uk-nav-default"
              ><span
                class="uk-margin-small-right"
                uk-icon="icon: thumbnails"
              ></span
              >Commander</a
            >
            <ul class="uk-nav-sub uk-nav-default">
              <li v-for="orderItem in orderItems" :key="orderItem.id">
                <router-link
                  :to="{
                    name: 'ApplicationOrder',
                    params: { application: orderItem.slug },
                  }"
                >{{ orderItem.name }}</router-link>
              </li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import UserOptions from '@/components/Utils/Navbar/UserOptions'
import { mapState } from 'vuex'

export default {
  props: {
    adminPanelItems: Array,
    orderItems: {
      type: Array,
      required: true
    }
  },
  components: {
    UserOptions
  },
  computed: {
    ...mapState({ currentUser: (state) => state.auth.currentUser })
  }
}
</script>
