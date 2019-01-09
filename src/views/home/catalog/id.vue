<template>
  <div class="catalog-table">
    <Card>
      <Collapse v-model="value2" simple>
        <Panel name="1">Event Information
          <Table :columns="columns_event" :data="event_table" slot="content"></Table>
        </Panel>
      </Collapse>
    </Card>
    <Card>
      <Table :columns="columns_station" :data="station_table">
        <template slot-scope="{ row }" slot="station_name">
          <strong>{{ row.station_name }}</strong>
        </template>
        <template slot-scope="{ row, index }" slot="action">
          <Button type="default" size="small" style="margin-right: 5px" @click="map_show(index)">Map</Button>
          <Button
            type="default"
            size="small"
            style="margin-right: 5px"
            @click="waveform_show(index)"
          >Waveform</Button>
        </template>
      </Table>
    </Card>
    <Drawer :title="waveform.button_show?'Waveform':'Map'" v-model="map.drawer" width="90%">
      <Card class="map-canvas-div">
        <vue-plotly
          :data="map.data"
          :layout="map.layout"
          :options="map.options"
          class="map-plotly"
        />
      </Card>
      <Row v-if="waveform.button_show">
        <Col span="2">
          <Button
            type="info"
            shape="circle"
            @click="waveform.drawer_value=true"
            size="small"
          >Plot Configuration
            <Icon type="ios-settings"/>
          </Button>
        </Col>
        <Col span="22">&nbsp</Col>
      </Row>
    </Drawer>
    <Drawer title="Waveform Setting" v-model="waveform.drawer_value" width="30%">
      <Card class="map-canvas-div">
        <Form ref="waveform settings" :model="waveform.setting">
          <FormItem label="Select Start Time:">
            <Select
              v-model="waveform.setting.start_time"
              style="width:200px"
              @on-change="setting_change"
            >
              <Option
                v-for="item in waveform.data.start_time"
                :value="item.value"
                :key="item.value"
              >{{ item.key }}</Option>
            </Select>
          </FormItem>
          <FormItem label="Select Model:">
            <Select
              v-model="waveform.setting.model"
              style="width:200px"
              @on-change="setting_change"
            >
              <Option
                v-for="item in waveform.data.model"
                :value="item.value"
                :key="item.value"
              >{{ item.key }}</Option>
            </Select>
          </FormItem>

          <FormItem label="Label Arrival Time Point:">
            <CheckboxGroup v-model="waveform.setting.label_arrival_time">
              <Checkbox label="p">p</Checkbox>
              <Checkbox label="s">s</Checkbox>
              <Checkbox label="P">P</Checkbox>
              <Checkbox label="S">S</Checkbox>
              <Checkbox label="Pn">Pn</Checkbox>
              <Checkbox label="Sn">Sn</Checkbox>
              <Checkbox label="PcP">PcP</Checkbox>
              <Checkbox label="ScS">ScS</Checkbox>
            </CheckboxGroup>
          </FormItem>
          <FormItem>
            <CheckboxGroup v-model="waveform.setting.label_arrival_time">
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
            <Slider
              v-model="waveform.setting.filter"
              range
              style="width:300px;margin-left: 40px;"
              @on-change="setting_change"
            />
          </FormItem>
          <FormItem label="Select Display Channal">
            <Select v-model="waveform.setting.channal" style="width:200px">
              <Option
                v-for="item in waveform.data.channal"
                :value="item.value"
                :key="item.value"
              >{{ item.key }}</Option>
            </Select>
          </FormItem>
          <FormItem>
            <Button size="small" @click="submit_waveform_setting">Submit</Button>
          </FormItem>
        </Form>
      </Card>
    </Drawer>
  </div>
</template>

<script>
import VuePlotly from "@statnett/vue-plotly";
import * as math from "mathjs";

export default {
  components: {
    VuePlotly
  },
  data() {
    return {
      value2: "1",
      columns_station: [
        {
          title: "Station Name",
          slot: "station_name",
          align: "center"
        },
        {
          title: "Latitude",
          key: "station_latitude",
          align: "center"
        },
        {
          title: "Longitude",
          key: "station_longitude",
          align: "center"
        },
        {
          title: "Great Circle Distance",
          key: "station_gcarc",
          align: "center"
        },
        {
          title: "Plot",
          slot: "action",
          align: "center"
        }
      ],
      columns_event: [
        {
          title: "ID",
          key: "ID",
          align: "center"
        },
        {
          title: "start_time",
          key: "start_time",
          align: "center"
        },
        {
          title: "latitude",
          key: "latitude",
          align: "center"
        },
        {
          title: "longitude",
          key: "longitude",
          align: "center"
        },
        {
          title: "depth",
          key: "depth",
          align: "center"
        },
        {
          title: "magnitude",
          key: "magnitude",
          align: "center"
        }
      ],
      event_table: [
        {
          ID: this.$store.state.catalog.id,
          start_time: this.$store.state.catalog.start_time,
          latitude: this.$store.state.catalog.latitude,
          longitude: this.$store.state.catalog.longitude,
          depth: this.$store.state.catalog.depth,
          magnitude: this.$store.state.catalog.magnitude
        }
      ],
      station_table: [],
      map: {
        drawer: false,
        data: undefined,
        layout: undefined,
        options: undefined
      },
      // waveform_drawer_value: false,
      waveform: {
        button_show: false,
        drawer_value: false,
        present_index: -1,
        past_wave: {},
        traveltime_result: {},
        setting: {
          start_time: "reference_time",
          label_arrival_time: [],
          filter: [6, 45],
          channal: "z",
          model: "prem",
          changed: true
        },
        data: {
          start_time: [
            {
              value: "reference_time",
              key: "Reference Time"
            },
            {
              value: "shock_time",
              key: "Shock Time"
            },
            {
              value: "p_arrival_time",
              key: "P Arrival Time"
            },
            {
              value: "s_arrival_time",
              key: "S Arrival Time"
            }
          ],
          channal: [
            {
              value: "z",
              key: "vertical"
            },
            {
              value: "r",
              key: "radial"
            },
            {
              value: "t",
              key: "tangential"
            }
          ],
          model: [
            {
              value: "prem",
              key: "prem"
            },
            {
              value: "iasp91",
              key: "iasp91"
            },
            {
              value: "ak135",
              key: "ak135"
            }
          ]
        }
      }
    };
  },
  mounted() {
    this.get_event_data();
  },
  methods: {
    get_event_data: function() {
      this.$http
        .get(this.$config.baseurl + "catalog/" + this.$store.state.catalog.id)
        .then(result => {
          this.station_table = JSON.parse(result.data);
        })
        .catch(err => {
          console.log(err);
        });
    },
    map_show: function(index) {
      this.waveform.button_show = false;

      var data = [
        {
          type: "scattergeo",
          lat: [
            parseFloat(this.$store.state.catalog.latitude),
            this.station_table[index].station_latitude
          ],
          lon: [
            parseFloat(this.$store.state.catalog.longitude),
            this.station_table[index].station_longitude
          ],
          mode: "lines+markers+text",
          line: {
            width: 2,
            color: "red"
          },
          text: [
            "source",
            "station: " + this.station_table[index].station_name
          ],
          marker: {
            size: 7,
            color: ["#bebada", "#fdb462"],
            line: {
              width: 1
            }
          },
          textposition: ["top right", "top right"]
        }
      ];

      var lat = [
        parseFloat(this.$store.state.catalog.latitude),
        this.station_table[index].station_latitude
      ];
      var lon = [
        parseFloat(this.$store.state.catalog.longitude),
        this.station_table[index].station_longitude
      ];
      var lat_max = Math.max(...lat);
      var lat_min = Math.min(...lat);
      var lon_max = Math.max(...lon) + 1;
      var lon_min = Math.min(...lon) - 1;

      lat_max = lat_max + 10 > 90 ? 90 : lat_max + 10;
      lat_min = lat_min - 10 < -90 ? -90 : lat_min - 10;

      var layout = {
        title:
          this.$store.state.catalog.id +
          " " +
          this.station_table[index].station_name,
        showlegend: false,
        width: 1500,
        height: 800,
        geo: {
          resolution: 50,
          showland: true,
          showlakes: true,
          landcolor: "rgb(204, 204, 204)",
          countrycolor: "rgb(204, 204, 204)",
          lakecolor: "rgb(255, 255, 255)",
          projection: {
            type: "equirectangular"
          },
          coastlinewidth: 2,
          lataxis: {
            // range: [lat_min, lat_max],
            showgrid: true,
            tickmode: "linear",
            dtick: 10
          },
          lonaxis: {
            // range: [lon_min, lon_max],
            showgrid: true,
            tickmode: "linear",
            dtick: 20
          }
        }
      };
      this.map = {
        drawer: true,
        data: data,
        layout: layout,
        options: undefined
      };
    },
    waveform_show: function(index) {
      var x = undefined;
      var y = undefined;
      var result_data = undefined;
      this.waveform.present_index = index;

      this.$http
        .get(
          this.$config.baseurl +
            "/" +
            this.$store.state.catalog.id +
            "/" +
            this.station_table[index].station_name
        )
        .then(result => {
          result_data = JSON.parse(result.data);
          /* update wave log*/
          this.waveform.past_wave = result_data;
          this.waveform_plot(result_data, false);
          // this.map_show(index);
        })
        .catch(err => {
          console.log(err);
        });
    },
    waveform_plot: function(result_data, pre_label) {
      var r = result_data.r;
      var z = result_data.z;
      var t = result_data.t;
      var toplotwave = {
        r: r,
        t: t,
        z: z
      };
      var stats = result_data.stats;

      var x = Array.from(
        new Array(stats.npts),
        (val, index) => index * stats.delta
      );
      if (pre_label) {
        x = Array.from(
          new Array(stats.npts),
          (val, index) => index * stats.delta - 200
        );
      }

      var data_plot = {
        x: x,
        y: toplotwave[this.waveform.setting.channal],
        mode: "lines",
        type: "scatter",
        showlegend: false
      };
      var layout = {
        title:
          this.$store.state.catalog.id +
          " " +
          this.station_table[this.waveform.present_index].station_name
      };
      /* plot time label*/
      var label_time_plot_x = [];
      var label_time_plot_y = [];
      var label_time_plot_text = [];
      switch (this.waveform.setting.start_time) {
        case "reference_time":
          for (var phase of this.waveform.setting.label_arrival_time) {
            if (this.waveform.traveltime_result[phase] != undefined) {
              label_time_plot_x.push(
                this.waveform.traveltime_result[phase] + stats.o
              );
              label_time_plot_text.push(phase);
              label_time_plot_y.push(0);
            }
          }
          break;
        case "shock_time":
          for (let phase of this.waveform.setting.label_arrival_time) {
            if (this.waveform.traveltime_result[phase] != undefined) {
              label_time_plot_x.push(this.waveform.traveltime_result[phase]);
              label_time_plot_text.push(phase);
              label_time_plot_y.push(0);
            }
          }
          break;
        case "p_arrival_time":
          for (let phase of this.waveform.setting.label_arrival_time) {
            if (this.waveform.traveltime_result[phase] != undefined) {
              if (this.waveform.traveltime_result["p"] === undefined) {
                label_time_plot_x.push(
                  this.waveform.traveltime_result[phase] -
                    this.waveform.traveltime_result["P"]
                );
                label_time_plot_text.push(phase);
                label_time_plot_y.push(0);
              }
            } else {
              label_time_plot_x.push(
                this.waveform.traveltime_result[phase] -
                  this.waveform.traveltime_result["p"]
              );
              label_time_plot_text.push(phase);
              label_time_plot_y.push(0);
            }
          }
          break;
        case "s_arrival_time":
          for (let phase of this.waveform.setting.label_arrival_time) {
            if (this.waveform.traveltime_result[phase] != undefined) {
              if (this.waveform.traveltime_result["s"] === undefined) {
                label_time_plot_x.push(
                  this.waveform.traveltime_result[phase] -
                    this.waveform.traveltime_result["S"]
                );
                label_time_plot_text.push(phase);
                label_time_plot_y.push(0);
              }
            } else {
              label_time_plot_x.push(
                this.waveform.traveltime_result[phase] -
                  this.waveform.traveltime_result["s"]
              );
              label_time_plot_text.push(phase);
              label_time_plot_y.push(0);
            }
          }
          break;
        default:
      }

      var label_time_plot = {
        x: label_time_plot_x,
        y: label_time_plot_y,
        text: label_time_plot_text,
        mode: "markers+text",
        textposition: "top",
        type: "scatter",
        showlegend: false
      };

      var data = [data_plot, label_time_plot];

      this.waveform.button_show = true;
      this.map = {
        drawer: true,
        data: data,
        layout: layout,
        options: undefined
      };
    },
    submit_waveform_setting: function() {
      /* iris traveltime*/
      var traveltime_result = {};
      this.$http
        .get(this.$config.iris_traveltime, {
          params: {
            distdeg: this.station_table[this.waveform.present_index]
              .station_gcarc,
            evdepth: this.$store.state.catalog.depth,
            format: "json",
            model: this.waveform.setting.model
          }
        })
        .then(result => {
          var temp_label_arrival_time = JSON.parse(
            JSON.stringify(this.waveform.setting.label_arrival_time)
          );
          temp_label_arrival_time.push("p", "P", "s", "S");
          for (let item of temp_label_arrival_time) {
            let traveltime_obj = result.data.arrivals.find(
              o => o.phase === item
            );
            traveltime_result[item] = traveltime_obj
              ? traveltime_obj.time
              : undefined;
          }
          this.waveform.traveltime_result = traveltime_result;
          /* get filtered data*/
          if (this.waveform.setting.changed) {
            this.waveform.setting.changed = false;
            var get_filtered_data_start_time = "reference_time";
            switch (this.waveform.setting.start_time) {
              case "reference_time":
                get_filtered_data_start_time = "reference_time";
                break;
              case "shock_time":
                get_filtered_data_start_time = "shock_time";
                break;
              case "p_arrival_time":
                get_filtered_data_start_time = traveltime_result["p"]
                  ? traveltime_result["p"]
                  : traveltime_result["P"];
                break;
              case "s_arrival_time":
                get_filtered_data_start_time = traveltime_result["s"]
                  ? traveltime_result["s"]
                  : traveltime_result["S"];
                break;
              default:
                get_filtered_data_start_time = -1;
            }
            this.$http
              .post(
                this.$config.baseurl +
                  "/" +
                  this.$store.state.catalog.id +
                  "/" +
                  this.station_table[this.waveform.present_index].station_name,
                JSON.stringify({
                  start_time: get_filtered_data_start_time
                    ? get_filtered_data_start_time
                    : "reference_time",
                  filter: this.waveform.setting.filter
                })
              )
              .then(result => {
                /* update wave log*/
                var result_data = JSON.parse(result.data);
                this.waveform.past_wave = result_data;

                /* update waveform */
                if (
                  this.waveform.setting.start_time === "reference_time" ||
                  this.waveform.setting.start_time === "shock_time"
                ) {
                  this.waveform_plot(JSON.parse(result.data), false);
                  return;
                }
                if (
                  this.waveform.setting.start_time === "p_arrival_time" ||
                  this.waveform.setting.start_time === "s_arrival_time"
                ) {
                  this.waveform_plot(JSON.parse(result.data), true);
                  return;
                }
              })
              .catch(err => {
                console.log(err);
                return;
              });
          }
          /* if not changed, then make new label or change display channal*/
          if (
            this.waveform.setting.start_time === "reference_time" ||
            this.waveform.setting.start_time === "shock_time"
          ) {
            this.waveform_plot(this.waveform.past_wave, false);
            return;
          }
          if (
            this.waveform.setting.start_time === "p_arrival_time" ||
            this.waveform.setting.start_time === "s_arrival_time"
          ) {
            this.waveform_plot(this.waveform.past_wave, true);
            return;
          }
        })
        .catch(err => {
          console.log(err);
          for (let item of this.waveform.setting.label_arrival_time) {
            traveltime_result[item] = undefined;
          }
        });
    },
    setting_change: function() {
      this.waveform.setting.changed = true;
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
.map-canvas-div {
  margin-left: auto;
  margin-right: auto;
  width: 1500px;
  height: 800px;
}
</style>
