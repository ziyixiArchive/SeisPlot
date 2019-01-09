<template>
  <div>
    <Layout class="home">
      <Header class="home-header">
        <Row>
          <Col span="2">
            <img src="../../static/seismic.jpg" class="icon-home">
          </Col>
          <Col span="1">&nbsp</Col>
          <Col span="20">
            <Menu mode="horizontal" theme="light" active-name="1">
              <MenuItem name="1" to="/home/catalog">
                <Icon type="ios-book"/>Catalog
              </MenuItem>
              <MenuItem name="2" to="/home/map">
                <Icon type="ios-basketball"/>Map
              </MenuItem>
              <MenuItem name="3" to="/home/waveform">
                <Icon type="ios-pulse"/>Waveform
              </MenuItem>
            </Menu>
          </Col>
          <Col span="1">
            <Dropdown>
              <a href="javascript:void(0)" style="color:black">setting
                <Icon type="ios-settings"/>
              </a>
              <DropdownMenu slot="list">
                <DropdownItem on-clickoutside="test">Project Setting</DropdownItem>
                <DropdownItem>Quit</DropdownItem>
              </DropdownMenu>
            </Dropdown>
          </Col>
        </Row>
      </Header>
      <Content class="home-content">
        <router-view></router-view>
      </Content>
    </Layout>
  </div>
</template>


<script>
export default {
  data() {
    return {};
  },
  methods: {
    test: function() {
      console.log("test");
    }
  }
};
</script>


<style>
.home {
  background-color: white;
}
.home-header {
  background-color: white;
}
.home-content {
  background-color: white;
}
.icon-home {
  height: 100%;
  width: 100%;
}
</style>
