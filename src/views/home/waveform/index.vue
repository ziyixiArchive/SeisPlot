<template>
  <div class="wave-main">
    <Row class="button-row">
      <Col span="22">&nbsp</Col>
      <Col span="2">
        <Button
          type="info"
          shape="circle"
          @click="drawer_value=true"
          size="small"
        >Waveform Configuration
          <Icon type="ios-settings"/>
        </Button>
        <Drawer
          title="Waveform Configuration"
          placement="left"
          :closable="false"
          v-model="drawer_value"
          width="500"
        >
          <Button type="info" shape="circle" @click="plot" size="small">Plot
            <Icon type="ios-settings"/>
          </Button>
        </Drawer>
      </Col>
    </Row>
    <Row>
      <Col span="24">
        <Card class="wave-canvas-div">
          <vue-plotly :data="data" :layout="layout" :options="options" class="vue-plotly"/>
        </Card>
      </Col>
    </Row>
  </div>
</template>

<script>
import VuePlotly from "@statnett/vue-plotly";

var x=new Array(10000);
var y=new Array(10000);
for(var i=0;i<10000;i++){
    x[i]=i;
    y[i]=i;
}

export default {
  components: {
    VuePlotly
  },
  data: function() {
    return {
      data: [{ x: x, y: y }],
      layout: {},
      options: {},
      drawer_value: false
    };
  }
};
</script>
<style>
.wave-main {
  margin-top: 30px;
}
.wave-canvas-div {
  margin-left: auto;
  margin-right: auto;
  width: 1500px;
  height: 800px;
}
.vue-plotly {
    margin: auto;
    height: 750px;
}
</style>
