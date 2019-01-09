import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    events: undefined,
    catalog: {
      id: undefined,
      start_time: undefined,
      latitude: undefined,
      longitude: undefined,
      depth: undefined,
      magnitude: undefined
    }
  },
  mutations: {
    renew_events(state, events) {
      state.events = events;
    },
    renew_catalog(state, catalog) {
      state.catalog = catalog;
    }
  },
  actions: {}
});
