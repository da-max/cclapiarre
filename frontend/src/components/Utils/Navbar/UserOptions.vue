<template>
  <div>
    <a href="#" uk-icon="icon: user; ratio: 1.5" class="uk-icon-link"> </a>
    <div class="uk-navbar-dropdown">
      <ul class="uk-nav uk-navbar-dropdown-nav">
        <li class="uk-nav-header"></li>
        <li
          v-for="userOptionItem in userOptionsItems"
          :key="userOptionItem.title"
        >
          <a href="{% url 'change_password' %}">{{ userOptionItem.title }}</a>
        </li>
      </ul>
    </div>
  </div>
</template>

<script lang="ts">
import { Options, Vue } from 'vue-class-component'
import { NavbarItem } from '@/types/index'

@Options({
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
        },
        {
          title: 'Déconnexion',
          link: '#'
        }
      ] as NavbarItem
    }
  }
})
export default class UserOptions extends Vue {}
</script>
