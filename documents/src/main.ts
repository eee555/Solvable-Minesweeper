import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus';
import 'element-plus/lib/theme-chalk/index.css';
import axios, { AxiosRequestConfig, AxiosResponse } from 'axios';
import { ElLoading } from 'element-plus';
import VueAxios from 'vue-axios'
// axios.defaults.baseURL = ''
const app = createApp(App);


app.config.globalProperties.$axios = axios;


app.use(VueAxios, axios)
app.use(router);
app.use(ElementPlus);
app.mount('#app');






