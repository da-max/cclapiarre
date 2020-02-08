import Vue from 'vue'
import App from './App.vue'
import VueResource from 'vue-resource'
import router from './router'

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

Vue.config.productionTip = false
Vue.use(VueResource)
Vue.http.options.root = 'http://localhost:8000/'

Vue.http.headers.common['X-CSRFToken'] = getCookie('csrftoken')
Vue.http.interceptors.push((request, next) => {
  next((response) => {
    if (request.after) {
      request.after.call(this, response)
    }
  })
})

new Vue({
  router,
  render: function (h) { return h(App) },
}).$mount('#app')
