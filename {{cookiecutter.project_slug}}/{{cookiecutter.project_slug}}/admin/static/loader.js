(function (ctx) {
  function append2Head(element) {
    document.head.append(element)
  }

  async function processSFC(response) {
    const source = await response.text();
    const element = document.createElement("div");
    element.innerHTML = source;
    let component = "export default {}";
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
    return new Response(new Blob([component], {type: 'application/javascript'}))
  }

  ctx.esmsInitOptions = {
    fetch: async function (url, options) {
      const res= await fetch(url, options);
      if (!res.ok) {
        return res
      }

      if (res.url.endsWith('.vue')) {
        return await processSFC(res)
      }
      return res;
    },
  }
/*global globalThis*/
/*eslint no-undef: "error"*/
})(globalThis);
