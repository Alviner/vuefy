
import { createApp, elementPlus, elementPlusLocale as locale } from 'vendor';

import App from './App.js';
import wsrpc from './api/ws.js';
import router from './router.js ';

const app = createApp({
  ...App,
  beforeCreate: function () {
    wsrpc.connect();
  },
});

app.config.globalProperties.$wsrpc = wsrpc.proxy;
app.config.globalProperties.$json = (any) => JSON.stringify(any, null, 2);

app
  .use(router)
  .use(elementPlus, { locale })
  .mount('#app');

export default app;

