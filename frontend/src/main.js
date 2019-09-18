// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import ElementUI from 'element-ui'
import VueResource from 'vue-resource'
import Router from 'vue-router'
import VueQuillEditor from 'vue-quill-editor'
/* eslint-disable */
import VueObserveVisibility from 'vue-observe-visibility'
import App from './App'
import router from './router'
import swal from 'sweetalert'
import 'element-ui/lib/theme-chalk/index.css'
import 'quill/dist/quill.core.css'
import 'quill/dist/quill.snow.css'
import 'quill/dist/quill.bubble.css'
import CONFIG from './config'

Vue.use(ElementUI)
Vue.use(VueResource)
Vue.use(VueQuillEditor)
Vue.use(VueObserveVisibility)
Vue.use(Router)
Vue.config.productionTip = false
Vue.http.options.root = CONFIG.API_URL

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
