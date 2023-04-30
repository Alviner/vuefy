
import 'element-plus/dist/index.css';
import WSRPC from '@wsrpc/client';

import {
  createApp,
} from 'vue/dist/vue.esm-bundler.js';

import {
  createRouter,
  createWebHistory,
  RouterLink,
} from 'vue-router/dist/vue-router.esm-bundler.js';

import elementPlusLocale from 'element-plus/es/locale/lang/ru.mjs';
import elementPlus, {
  ElLoading as Loading,
  ElMessage as Message,
  ElNotification as Notification,
} from 'element-plus';


export {
  WSRPC,

  createApp,

  createWebHistory,
  createRouter,
  RouterLink,

  elementPlus,
  elementPlusLocale,
  Loading,
  Message,
  Notification,
};
