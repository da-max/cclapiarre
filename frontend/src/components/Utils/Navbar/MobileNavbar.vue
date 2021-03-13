<template>
  <div>
    <div
      class="uk-box-shadow-large"
      uk-sticky="sel-target: .uk-navbar-container; cls-active: uk-navbar-sticky"
    >
      <nav
        class="uk-navbar-container uk-navbar"
        uk-sticky="sel-target: .uk-navbar-container; cls-active: uk-navbar-sticky; cls-inactive: uk-navbar-primary uk-primary; top: 200"
        uk-navbar
      >
        <div class="uk-navbar-left">
          <a
            class="uk-navbar-toggle"
            href="#mobile-menu"
            uk-toggle
          >
            <span uk-navbar-toggle-icon />
            <span class="uk-margin-small-left">Menu</span>
          </a>
        </div>
        <div class="uk-navbar-center">
          <router-link
            :to="{name: 'Home' }"
            class="uk-navbar-item uk-logo"
          >
            <img
              src="/static/Images/logo.png"
              width="75"
              height="75"
            >
          </router-link>
        </div>
        <UserOptions
          v-if="currentUser && currentUser.username"
          class="uk-navbar-right uk-margin-right"
        />
      </nav>
    </div>

    <div
      id="mobile-menu"
      uk-offcanvas="overlay: true; mode: push"
    >
      <div class="uk-offcanvas-bar uk-flex uk-flex-column">
        <ul
          class="uk-nav uk-nav-center uk-margin-auto-vertical"
          uk-nav
        >
          <li>
            <router-link :to="{ name: 'Home' }">
              Accueil
            </router-link>
          </li>
          <li class="uk-parent">
            <router-link
              :to="{ name: 'MemberList' }"
            >
              Liste des adhérents
            </router-link>
          </li>
          <li class="uk-parent">
            <a
              href="#"
              class="uk-nav-header"
            ><span
              class="uk-margin-small-right"
              uk-icon="icon: thumbnails"
            />Espace administration</a>

            <ul
              class="uk-nav uk-nav-sub uk-nav-default uk-nav-parent-icon"
              uk-nav
            >
              <li
                v-for="adminPanelItem in adminPanelItems"
                :key="adminPanelItem.title"
                class="uk-parent"
              >
                <a class="uk-nav-header">{{ adminPanelItem.title }}</a>
                <ul class="uk-nav-sub">
                  <li
                    v-for="subItem in adminPanelItem.subItems"
                    :key="subItem.name"
                    :class="{ 'uk-nav-divider': subItem.divider}"
                  >
                    <router-link
                      v-if="subItem.routerLink && !subItem.divider"
                      :to="subItem.routerLink"
                    >
                      {{ subItem.name }}
                    </router-link>
                    <a
                      v-else-if="!subItem.divider"
                      :href="subItem.link"
                    >{{ subItem.name }}</a>
                  </li>
                </ul>
                <div class="uk-nav-divider" />
              </li>
            </ul>
          </li>
          <li class="uk-parent">
            <a
              href="#"
              class="uk-nav-header uk-nav-default"
            ><span
              class="uk-margin-small-right"
              uk-icon="icon: thumbnails"
            />Commander</a>
            <ul class="uk-nav-sub uk-nav-default">
              <li>
                <router-link :to="{ name: 'CoffeeOrder' }">
                  Café
                </router-link>
              </li>
              <li>
                <router-link :to="{name: 'CitrusOrder'}">
                  Agrumes
                </router-link>
              </li>
              <li
                v-for="orderItem in orderItems"
                :key="orderItem.id"
              >
                <router-link
                  :to="{
                    name: 'ApplicationOrder',
                    params: { application: orderItem.slug }
                  }"
                >
                  {{ orderItem.name }}
                </router-link>
              </li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import UserOptions from '@/components/Utils/Navbar/UserOptions'

export default {
    components: {
        UserOptions
    },
    props: {
        adminPanelItems: {
            required: true,
            type: Array
        },
        orderItems: {
            required: true,
            type: Array
        }
    },
    computed: {
        ...mapState({ currentUser: (state) => state.auth.currentUser })
    }
}
</script>
