<template id="home-tpl">
  <div class="flex min-h-screen">
    <side-menu></side-menu>
    <div>
      <h1>
        Версия {{ version }}
      </h1>

      <h2>Ответ http ручки ping</h2>
      <pre>{{ $json(pingData) }}</pre>

      <h3>Ответ ws ручки окружения</h3>
      <pre>{{ $json(envData) }}</pre>
    </div>
  </div>
</template>

<script>
import SideMenu from '../components/SideMenu.vue';

export default {
  template: '#home-tpl',
  components: {SideMenu},
  data () {
    return {
      envData: undefined,
      pingData: undefined,
      version: undefined,
    };
  },
  computed: {},
  async created () {
    await this.loadEnv();
    await this.getVersion();
  },
  methods: {
    async loadEnv () {
      try {
        this.envData = await this.$wsrpc.env.load();
      } catch (e) {
        console.error(e);
      }
    },
    async getVersion () {
      try {
        const resp = await fetch('/api/v1/ping');
        this.version = resp.headers.get('X-VERSION');
        this.pingData = await resp.json();
      } catch (e) {
        console.error(e);
      }
    },
  },
};
</script>
