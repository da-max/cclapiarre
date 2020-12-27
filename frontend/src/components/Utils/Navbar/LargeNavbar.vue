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
            <li>
              <router-link :to="{ name: 'Home' }">
                Accueil
              </router-link>
            </li>
            <a
              class="uk-navbar-item uk-logo"
            ><img
              src="../../../assets/logo.png"
              width="75"
              height="75"
            ></a>
            <li>
              <router-link
                :to="{ name: 'MemberList' }"
              >
                Liste des adhérents
              </router-link>
            </li>
            <li>
              <a
                href="#administration-space"
                uk-toggle
              >Espace administration</a>
            </li>
            <li>
              <a href="#">Commander</a>
              <div class="uk-navbar-dropdown">
                <ul class="uk-nav uk-navbar-dropdown-nav">
                  <li>
                    <router-link
                      :to="{ name: 'CoffeeOrder' }"
                    >
                      Café
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
              </div>
            </li>

            <UserOptions
              v-if="currentUser && currentUser.username"
              :li="true"
              class="uk-position-relative uk-position-right uk-margin-right uk-margin-large-left"
            />
          </ul>
        </div>
      </nav>
    </div>

    <div
      id="administration-space"
      uk-offcanvas="overlay: true"
    >
      <div class="uk-offcanvas-bar">
        <ul
          class="uk-nav uk-nav-default uk-nav-parent-icon"
          uk-nav
        >
          <li class="uk-active uk-text-center uk-text-bold">
            <a href="">Espace administration</a>
          </li>
          <br>
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
                :class="{'uk-nav-divider': subItem.divider}"
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

          <li><a href="/admin/">Administration</a></li>
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
