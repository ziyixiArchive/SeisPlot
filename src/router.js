import Vue from "vue";
import Router from "vue-router";

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: "/",
      name: "setting",
      component: () =>
        import(/* webpackChunkName: "login" */ "@/views/login/index.vue")
    },
    {
      path: "/home",
      name: "home",
      component: () =>
        import(/* webpackChunkName: "home" */ "@/views/home/index.vue"),
      children: [
        {
          path: "catalog",
          name: "catalog",
          component: () =>
            import(/* webpackChunkName: "catalog" */ "@/views/home/catalog/index.vue"),
          children: []
        },
        {
          path: "waveform",
          name: "waveform",
          component: () =>
            import(/* webpackChunkName: "waveform" */ "@/views/home/waveform/index.vue")
        },
        {
          path: "map",
          name: "map",
          component: () =>
            import(/* webpackChunkName: "map" */ "@/views/home/map/index.vue")
        },
        {
          path: ":id",
          name: "catalog_id",
          component: () =>
            import(/* webpackChunkName: "catalog" */ "@/views/home/catalog/id.vue")
        }
      ]
    }
  ]
});
