<template>
  <div class="map-main">
    <Row class="button-row">
      <Col span="22">&nbsp</Col>
      <Col span="2">
        <Button type="info" shape="circle" @click="drawer_value=true" size="small">Map Configuration
          <Icon type="ios-settings"/>
        </Button>
        <Drawer
          title="Map Configuration"
          placement="left"
          :closable="false"
          v-model="drawer_value"
          width="500"
        >
          <Button
            type="info"
            shape="circle"
            @click="plot"
            size="small"
          >Plot
            <Icon type="ios-settings"/>
          </Button>
        </Drawer>
      </Col>
    </Row>
    <Row>
      <Col span="24">
        <Card class="map-canvas-div">
          <canvas
            id="map"
            width="1500"
            height="800"
            class="map-canvas"
          >Your browser does not support HTML5 Canvas.</canvas>
        </Card>
      </Col>
    </Row>
  </div>
</template>

<script>
import map from "./map.js"

export default {
  data() {
    return {
      drawer_value: false
    };
  },
  methods: {
      plot: function() {
          map.plot()
      }
  }
};
</script>

<style>
.map-main {
  margin-top: 30px;
}
.map-canvas-div {
  margin-left: auto;
  margin-right: auto;
  width: 1500px;
  height: 800px;
}
</style>
