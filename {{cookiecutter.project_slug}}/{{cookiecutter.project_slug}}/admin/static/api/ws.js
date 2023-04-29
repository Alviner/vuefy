(function (ctx) {
  const {ELEMENT} = ctx;

  ctx.wsrpc = new WSRPC('/ws/');
  ctx.wsrpc.connect();
  let loading;

  ctx.wsrpc.addEventListener("onconnect", function () {
		console.log("Connection established");
		if (loading) {
			loading.close();
			loading = undefined;
		}
	});

	ctx.wsrpc.addEventListener("onerror", function () {
		console.error("Connection lost");
		loading = ELEMENT.Loading.service({
			lock: true,
			text: 'Потеряно соединение',
			spinner: 'el-icon-loading',
			background: 'rgba(0, 0, 0, 0.7)'
		});
	});

})(window);

