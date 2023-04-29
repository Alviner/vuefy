(async function (ctx) {

  function loadScript(jsText) {
    var promise = new Promise(function (resolve, reject) {
      var script = document.createElement("script");
      var src = window.URL.createObjectURL(
        new Blob([jsText], {
          type: "application/javascript",
        })
      );

      script.src = src;
      script.onload = resolve;
      document.head.appendChild(script);
    });
    return promise;
  }
  async function loadJS(url) {
    var response = await fetch(url);
    const source = await response.text();
    await loadScript(source)
  }

  function append2Head(element) {
    document.head.appendChild(element)
  }

  var body = document.getElementsByTagName("body")[0];
  ctx.components = {};
  ctx.mixins = {};

  async function loadComponent(el) {
    var response = await fetch(el.getAttribute("src"));
    const source = await response.text();
    const element = document.createElement("div");
    element.innerHTML = source;
    let component = "";
    Array.from(element.children).forEach(item => {
      switch (item.nodeName) {
        case 'TEMPLATE':
          append2Head(item);
          break;
        case 'SCRIPT':
          component = item.innerHTML;
          break;
        case 'STYLE':
          append2Head(item)
          break;
      }
    })
    await loadScript(component);
  }

  var components = $("script[type='text/x-component']");

  for (let i = 0; i < components.length; i++) {
    let el = components[i];
    await loadComponent(el);
  }


  await loadJS("/static/main.js");
  console.log("Application loaded");
})(window);
