<template>
  <div
    class="uk-card uk-card-default uk-width-2-5@l uk-width-4-5@s uk-margin-auto uk-padding-large"
  >
    <div class="uk-card-header">
      <span
        class="uk-text-warning uk-text-bold"
      >L'accès est réservé aux adhérents</span>, merci de rentrer votre NOM (en majuscule).prénom et le mot de passe qui
      vous a été communiqué.
    </div>
    <div class="uk-card-body">
      <LoginForm />
    </div>
  </div>
</template>

<script>
import LoginForm from '@/components/Registration/Login/LoginForm'

export default {
    name: 'LoginSection',
    components: {
        LoginForm
    }
}
</script>
