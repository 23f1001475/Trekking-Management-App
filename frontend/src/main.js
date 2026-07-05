import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import "./styles/style.css"

import 'bootstrap/dist/css/bootstrap.min.css'   //for css styles button form card grid etc.
import 'bootstrap/dist/js/bootstrap.bundle.min.js'   //for js functionality it is needed when using bootstrap components like modal dropdown navbar collapseetc.


const app = createApp(App)

app.use(router)

app.mount('#app')
