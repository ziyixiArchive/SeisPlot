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
    <Drawer
      :title="waveform.title"
      placement="left"
      :mask-closable="false"
      v-model="waveform.drawer"
      width="100%"
    >
      <template v-if="waveform.show_setting">
        <Card class="showsetting-card">
          <Form ref="Waveform Plotting Setting" :model="waveform.setting" label-position="top">
            <FormItem label="Select Start Time:">
              <Select
                v-model="waveform.setting.start_time"
                @on-change="waveform.should_communicate_with_backend=true"
              >
                <Option
                  v-for="item in waveform.data.start_time"
                  :value="item.value"
                  :key="item.value"
                >{{ item.key }}</Option>
              </Select>
            </FormItem>
            <FormItem label="Select Reference Model:">
              <Select
                v-model="waveform.setting.model"
                @on-change="waveform.should_communicate_with_backend=true"
              >
                <Option
                  v-for="item in waveform.data.model"
                  :value="item.value"
                  :key="item.value"
                >{{ item.key }}</Option>
              </Select>
            </FormItem>
            <FormItem label="Label Phases:">
              <CheckboxGroup
                v-model="waveform.setting.label_arrival_time"
                @on-change="waveform.should_communicate_with_backend=true"
              >
                <Checkbox label="p">p</Checkbox>
                <Checkbox label="s">s</Checkbox>
                <Checkbox label="P">P</Checkbox>
                <Checkbox label="S">S</Checkbox>
                <Checkbox label="Pn">Pn</Checkbox>
                <Checkbox label="Sn">Sn</Checkbox>
                <Checkbox label="PcP">PcP</Checkbox>
                <Checkbox label="ScS">ScS</Checkbox>
                <Checkbox label="Pdiff">Pdiff</Checkbox>
                <Checkbox label="Sdiff">Sdiff</Checkbox>
                <Checkbox label="PKP">PKP</Checkbox>
                <Checkbox label="SKS">SKS</Checkbox>
                <Checkbox label="PKiKP">PKiKP</Checkbox>
                <Checkbox label="SKiKS">SKiKS</Checkbox>
                <Checkbox label="PKIKP">PKIKP</Checkbox>
                <Checkbox label="SKIKS">SKIKS</Checkbox>
              </CheckboxGroup>
            </FormItem>
            <FormItem label="Filter:">
              <Slider v-model="waveform.setting.filter" range/>
            </FormItem>
            <FormItem label="Select Channal:">
              <Select v-model="waveform.setting.channal">
                <Option
                  v-for="item in waveform.data.channal"
                  :value="item.value"
                  :key="item.value"
                >{{ item.key }}</Option>
              </Select>
            </FormItem>
            <FormItem
              label="Select Vertical Axis:"
              @on-change="waveform.should_communicate_with_backend=true"
            >
              <Select v-model="waveform.setting.axis">
                <Option
                  v-for="item in waveform.data.axis"
                  :value="item.value"
                  :key="item.value"
                >{{ item.key }}</Option>
              </Select>
            </FormItem>
            <FormItem>
              <Button size="small" @click="waveform_submit_config">Submit</Button>
            </FormItem>
          </Form>
        </Card>
      </template>
      <template v-else>
        <Card class="waveformplot-card">
          <vue-plotly
            :data="waveform.plot.data"
            :layout="waveform.plot.layout"
            :options="waveform.plot.options"
            style="margin:auto;height:720px;width:1200px"
          />
        </Card>
      </template>
    </Drawer>
  </div>
</template>

<script>
import plot_utils from "./index_plot_utils.js";
import VuePlotly from "@statnett/vue-plotly";

export default {
  components: {
    VuePlotly
  },
  data() {
    return {
      /* table*/
      columns_name: plot_utils.table.columns_name,
      table_data: [],
      /* drawer*/
      waveform: {
        drawer: false,
        show_setting: true,
        title: "",
        should_communicate_with_backend: true,
        present_index: -1,
        setting: {
          start_time: "reference_time",
          model: "prem",
          label_arrival_time: [],
          filter: [6, 45],
          channal: "z",
          axis: "epicenter_distance"
        },
        data: plot_utils.waveform.data,
        plot: {
          data: [],
          layout: {},
          options: {}
        }
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
    /** button plot*/
    plot: function(index) {
      this.waveform.drawer = true;
      this.waveform.present_index = index;
    },
    /*Waveform */
    waveform_submit_config: function() {
      if (this.waveform.should_communicate_with_backend) {
        this.should_communicate_with_backend = false;
        this.post_setting_to_get_waveform_and_plot();
      } else {
      }

      /**change to waveform page */
      this.waveform.show_setting = false;
    },
    /**plot */
    draw_waveform_based_on_data: function(data) {
      var x = new Array(10000);
      var y = new Array(10000);
      for (var i = 0; i < 10000; i++) {
        x[i] = i;
        y[i] = i;
      }
      this.waveform.plot.data = [{ x: x, y: y }];
    },
    /**get multible waveforms */
    post_setting_to_get_waveform_and_plot: function() {
      return this.$http
        .post(
          this.$config.baseurl +
            "waveform_multiple/" +
            this.table_data[this.waveform.present_index].event_id,
          JSON.stringify(this.waveform.setting)
        )
        .then(result => {
          var data = JSON.parse(result.data);
          this.draw_waveform_based_on_data(data);
        })
        .catch(err => {
          console.log(err);
        });
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

.showsetting-card {
  width: 1200px;
  margin-top: 100px;
  margin-left: auto;
  margin-right: auto;
}

.waveformplot-card {
  width: 1300px;
  margin-top: 50px;
  margin-left: auto;
  margin-right: auto;
}
</style>
