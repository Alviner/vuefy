(function (ctx) {
  const {Home} = ctx.components;
  const {wsrpc} = ctx;
  
  Vue.prototype.$wsrpc = wsrpc.proxy;
  Vue.prototype.$json = (any) => JSON.stringify(any, null, 2);

  Vue.use(VueRouter);
  Vue.use(ELEMENT);

  const router = new VueRouter({
		mode: 'history',
		routes: [
			{
				path: '/',
				name: 'home',
				component: Home,
			},
		]
	});

  ctx.app = new Vue({
    router,
    el: '#app',
  })
})(window)

