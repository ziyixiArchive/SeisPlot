<template>
  <div>
    <Layout class="login">
      <Header class="login-header">
        <img src="../../static/seismic.jpg" class="icon-main">
      </Header>
      <Content class="login-content">
        <Card class="login-card">
          <p slot="title">Project Setting</p>
          <Form ref="setting_form" :model="setting_form" label-position="right" :label-width="100">
            <FormItem label="name">
              <Input v-model="setting_form.name" :placeholder="setting_form.name"></Input>
            </FormItem>
            <FormItem label="author">
              <Input v-model="setting_form.author" :placeholder="setting_form.author"></Input>
            </FormItem>
            <FormItem label="description">
              <Input v-model="setting_form.description" :placeholder="setting_form.description"></Input>
            </FormItem>
            <FormItem label="directory">
              <Input v-model="setting_form.directory" :placeholder="setting_form.directory"></Input>
            </FormItem>
            <FormItem label="Date">
              <DatePicker
                :value="setting_form.date"
                type="date"
                format="ddd MMM dd yyyy"
                :placeholder="setting_form.date"
                style="width: 400px;"
                @on-change="handle_date_change"
              ></DatePicker>
            </FormItem>

            <FormItem label>
              <Checkbox v-model="setting_form.save">
                Save Configuration
                <span v-if="setting_form.save">in ~/.seisPlotrc</span>
              </Checkbox>
            </FormItem>
            <FormItem>
              <Button type="primary" to="home" @click="submit">Create</Button>
              <Button style="margin-left: 20px">Clear</Button>
            </FormItem>
          </Form>
        </Card>
      </Content>
      <Footer class="login-footer">&copy; 2018 Ziyi Xi</Footer>
    </Layout>
  </div>
</template>

<script>
const today = new Date().toDateString();

export default {
  data() {
    return {
      setting_form: {
        name: "",
        author: "",
        description: "",
        save: true,
        date: today,
        directory: ""
      }
    };
  },
  computed: {},
  mounted() {
    this.preload();
  },
  methods: {
    submit: function() {
      console.log(JSON.stringify(this.setting_form));
      this.$http
        .post(this.$config.baseurl + "login", JSON.stringify(this.setting_form))
        .then(result => {
          console.log(result);
        })
        .catch(err => {
          console.log(err);
        });
    },
    handle_date_change: function(date) {
      this.setting_form.date = date;
    },
    preload: function() {
      this.$http
        .get(this.$config.baseurl + "login_get_default")
        .then(result => {
          console.log(result);
          if (Object.keys(result.data).length === 0) {
            return;
          }
          this.setting_form.name = result.data.name;
          this.setting_form.author = result.data.author;
          this.setting_form.description = result.data.description;
          this.setting_form.date = result.data.date;
          this.setting_form.directory = result.data.directory;
          this.setting_form.save = result.data.save === "True";
        })
        .catch(err => {
          console.log(err);
        });
    }
  }
};
</script>

<style>
.login {
  background-color: white;
}
.login-header {
  background-color: white;
  height: 267px;
}
.login-content {
  background-color: white;
}
.login-footer {
  background-color: white;
  text-align: center;
  margin-top: 200px;
}
.icon-main {
  height: 104px;
  width: 267px;
  display: block;
  margin-left: auto;
  margin-right: auto;
}
.login-card {
  width: 900px;
  margin-top: -100px;
  margin-left: auto;
  margin-right: auto;
}
</style>
