<template>
  <section class="uk-text-center">
    <h3>Informations</h3>
    <div
      uk-grid
      class="uk-child-width-1-2@m uk-flex-center uk-text-bold"
    >
      <p>
        <span class="uk-label">Nom d’utilisateur</span> {{ information.username ? information.username : username }}
      </p>
      <p>
        <span class="uk-label">Email</span> {{ information.email ? information.email : email }}
      </p>
      <p>
        <span class="uk-label">Prénom</span> {{ information.firstName ? information.firstName : firstName }}
      </p>
      <p>
        <span class="uk-label">Nom</span> {{ information.lastName ? information.lastName : lastName }}
      </p>
    </div>
  </section>
</template>

<script>
import { mapState } from 'vuex'
export default {
    name: 'OrderInformation',
    props: {
        information: {
            required: false,
            type: Object,
            default: () => ({})
        }
    },
    computed: {
        ...mapState({
            username: (state) => state.auth.currentUser.username,
            email: (state) => state.auth.currentUser.email,
            firstName: (state) => state.auth.currentUser.firstName ? state.auth.currentUser.firstName : 'Non défini',
            lastName: (state) => state.auth.currentUser.lastName ? state.auth.currentUser.lastName : 'Non défini'
        })
    }
}
</script>
