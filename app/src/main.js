import {createApp} from 'vue'
import App from './App.vue'
import router from './router'
// import store from './store'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

import '@/assets/resetElStyle.scss'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import VMdPreview from '@kangc/v-md-editor/lib/preview';
import vuepressTheme from '@kangc/v-md-editor/lib/theme/vuepress';
import '@kangc/v-md-editor/lib/theme/style/vuepress.css';
import createLineNumbertPlugin from '@kangc/v-md-editor/lib/plugins/line-number/index';
import createCopyCodePlugin from '@kangc/v-md-editor/lib/plugins/copy-code/index';
import '@kangc/v-md-editor/lib/plugins/copy-code/copy-code.css';
import Prism from 'prismjs';

const app = createApp(App);

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}
VMdPreview.use(vuepressTheme, {
    Prism
});

VMdPreview.use(createLineNumbertPlugin());
VMdPreview.use(createCopyCodePlugin());
app.use(VMdPreview);
app.use(ElementPlus)
// app.use(store)
app.use(router)
app.mount('#app')
