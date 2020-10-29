<template>
  <div>
    <h1 class="uk-text-center uk-margin-large-top uk-margin-large-bottom">Se connecter</h1>
    <LoginSection />
  </div>
</template>

<script>
import LoginSection from '@/components/Registration/Login/LoginSection'

export default {
  name: 'Login',
  components: {
    LoginSection
  }
}
</script>
