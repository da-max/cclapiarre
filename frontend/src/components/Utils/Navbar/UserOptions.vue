<template>
  <li v-if="li">
    <a href="#" class="uk-text">
      <span uk-icon="icon: user; ratio: 1.5" class="uk-icon-link"></span
      >{{ currentUser.name ? currentUser.name : currentUser.username }}</a
    >
    <div class="uk-navbar-dropdown">
      <ul class="uk-nav uk-navbar-dropdown-nav">
        <li class="uk-nav-header"></li>
        <li
          v-for="userOptionItem in userOptionsItems"
          :key="userOptionItem.title"
        >
          <a href="">{{ userOptionItem.title }}</a>
        </li>
        <li>
          <a href="#" type="button" @click.prevent="logout">Déconnexion</a>
        </li>
      </ul>
    </div>
  </li>
  <div v-else>
    <a class="uk-text uk-navbar-toggle" href="#">
      <span uk-icon="icon: user; ratio: 1.5" class="uk-icon-link"></span
      >{{ currentUser.name ? currentUser.name : currentUser.username }}</a
    >
    <div class="uk-navbar-dropdown" uk-dropdown>
      <ul class="uk-nav uk-navbar-dropdown-nav">
        <li class="uk-nav-header"></li>
        <li
          v-for="userOptionItem in userOptionsItems"
          :key="userOptionItem.title"
        >
          <a href="">{{ userOptionItem.title }}</a>
        </li>
        <li>
          <a href="#" type="button" @click.prevent="logout()">Déconnexion</a>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  data () {
    return {
      userOptionsItems: [
        {
          title: 'Changer de mot de passe',
          link: '#'
        },
        {
          title: 'Changer d’utilisateur',
          link: '#'
        }
      ]
    }
  },
  props: {
    li: {
      default: false,
      required: false
    }
  },

  computed: {
    ...mapState({ currentUser: state => state.auth.currentUser })
  },

  methods: {
    logout () {
      this.$store.dispatch('auth/logoutUser')
    }
  }
}
</script>
