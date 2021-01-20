<template>
  <li v-if="li">
    <a
      href="#"
      class="uk-text"
    >
      <span
        uk-icon="icon: user; ratio: 1.5"
        class="uk-icon-link"
      />{{ currentUser.name ? currentUser.name : currentUser.username }}</a>
    <div class="uk-navbar-dropdown">
      <ul class="uk-nav uk-navbar-dropdown-nav">
        <li class="uk-nav-header" />
        <li
          v-for="userOptionItem in userOptionsItems"
          :key="userOptionItem.title"
        >
          <router-link :to="userOptionItem.link">
            {{ userOptionItem.title }}
          </router-link>
        </li>
        <li>
          <a
            href="#"
            type="button"
            @click.prevent="logout"
          >Déconnexion</a>
        </li>
      </ul>
    </div>
  </li>
  <div v-else>
    <a
      class="uk-text uk-navbar-toggle"
      href="#"
    >
      <span
        uk-icon="icon: user; ratio: 1.5"
        class="uk-icon-link"
      />{{ currentUser.name ? currentUser.name : currentUser.username }}</a>
    <div
      class="uk-navbar-dropdown"
      uk-dropdown
    >
      <ul class="uk-nav uk-navbar-dropdown-nav">
        <li class="uk-nav-header" />
        <li
          v-for="userOptionItem in userOptionsItems"
          :key="userOptionItem.title"
        >
          <router-link :to="userOptionItem.link">
            {{ userOptionItem.title }}
          </router-link>
        </li>
        <li>
          <a
            href="#"
            type="button"
            @click.prevent="logout()"
          >Déconnexion</a>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
    props: {
        li: {
            type: Boolean,
            default: false,
            required: false
        }
    },
    data () {
        return {
            userOptionsItems: [
                {
                    title: 'Changer d’utilisateur',
                    link: { name: 'Login' }
                }
            ]
        }
    },

    computed: {
        ...mapState({ currentUser: state => state.auth.currentUser })
    },

    methods: {
        logout () {
            this.$store.commit('alert/ADD_ALERT', {
                header: true,
                headerContent: `Au revoir ${this.$store.state.auth.currentUser.username}`,
                body: 'Vous êtes maintenant déconnecté. Merci d’être passé.',
                status: 'success',
                close: true
            })
            this.$store.dispatch('auth/logoutUser')
            this.$router.push('/')
        }
    }
}
</script>
