<template>
  <div class="catalog-table">
    <Table :columns="columns_name" :data="table_data">
      <template slot-scope="{ row }" slot="index">
        <strong>{{ row.event_id }}</strong>
      </template>
      <template slot-scope="{ row, index }" slot="action">
        <Button type="default" size="small" style="margin-right: 5px" @click="show(index)">View</Button>
        <Button type="default" size="small" style="margin-right: 5px" @click="plot(index)">Plot</Button>
      </template>
    </Table>
    <Drawer :title="waveform.title" placement="left" :closable="false" v-model="waveform.drawer"></Drawer>
  </div>
</template>

<script>
import plot_utils from "./index_plot_utils.js";

export default {
  data() {
    return {
      /* table*/
      columns_name: [
        {
          title: "ID",
          slot: "index",
          align: "center",
          fixed: "left"
        },
        {
          title: "Event",
          align: "center",
          children: [
            {
              title: "Start Time",
              key: "event_time",
              align: "center"
            },
            {
              title: "Latitude",
              key: "event_latitude",
              align: "center"
            },
            {
              title: "Longitude",
              key: "event_longitude",
              align: "center"
            },
            {
              title: "Depth",
              key: "event_depth",
              align: "center"
            },
            {
              title: "Magnitude",
              key: "event_magnitude",
              align: "center"
            }
          ]
        },
        {
          title: "Action",
          slot: "action",
          align: "center"
        }
      ],
      table_data: [],
      /* drawer*/
      waveform: {
        drawer: false,
        show_setting: true,
        title: ""
      }
    };
  },
  mounted() {
    if (this.$store.state.events === undefined) {
      this.get_catalog();
    } else {
      this.table_data = this.$store.state.events;
    }
  },
  methods: {
    /* get catalog data*/
    get_catalog: function() {
      this.$http
        .get(this.$config.baseurl + "catalog")
        .then(result => {
          console.log(result);
          var result_ordered = JSON.parse(result.data).sort((a, b) => {
            if (a.event_time < b.event_time) {
              return -1;
            } else {
              return 1;
            }
          });
          this.table_data = result_ordered;
          this.$store.commit("renew_events", result_ordered);
        })
        .catch(err => {
          console.log(err);
        });
    },
    /* button: view*/
    show: function(index) {
      var row_catalog = {
        id: this.table_data[index].event_id,
        start_time: this.table_data[index].event_time,
        latitude: this.table_data[index].event_latitude,
        longitude: this.table_data[index].event_longitude,
        depth: this.table_data[index].event_depth,
        magnitude: this.table_data[index].event_magnitude
      };
      this.$store.commit("renew_catalog", row_catalog);
      this.$router.push({
        name: "catalog_id",
        params: { id: this.table_data[index].event_id }
      });
    },
    plot: function(index) {
      console.log(index);
    }
  }
};
</script>

<style>
.catalog-table {
  margin-top: 30px;
  margin-left: 5%;
  margin-right: 5%;
}
</style>
