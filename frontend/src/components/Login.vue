<template>
  <div class="container">
    <el-row type="flex" justify="center" style="padding-top: 20vh;">
      <el-col :span="10">
        <el-card class="box-card card">
          <el-form :model="login" status-icon :rules="rule" ref="login">
            <el-form-item prop="username" label="用户名">
              <el-input prefix-icon="el-icon-user" v-model="login.username" auto-complete="off" />
            </el-form-item>
            <el-form-item prop="password" label="密码" @keyup.enter.native="onSubmit('login')">
              <el-input
                prefix-icon="el-icon-key"
                v-model="login.password"
                type="password"
                auto-complete="off"
                show-password
              />
            </el-form-item>
            <el-form-item>
              <el-button class="btn" type="primary" @click="onSubmit('login')">登陆</el-button>
              <el-button class="btn" type="danger" @click="clearFrm()">清除</el-button>
              <el-button class="btn" type="success" @click="loginOAuth">使用酒井ID登录</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<style lang="scss" scoped>
.container {
  height: 100vh;
  width: 100vw;
  background: url('~@/assets/bg.jpg');
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center center;
  .card {
    background-color: rgba($color: #fff, $alpha: 0.5) !important;
  }
}
</style>

<script>
/* eslint-disable */
let md5 = require('js-md5');

export default {
  name: "login",
  data() {
    return {
      checked: false,
      token: "",
      login: {
        username: "",
        password: ""
      },
      rule: {
        username: [{ required: true, message: "用户名不能为空", trigger: "blur" }],
        password: [{ required: true, message: "密码不能为空", trigger: "blur" }]
      }
    };
  },
  methods: {
    onSubmit: function(login) {
      this.$refs[login].validate(valid => {
        if (valid) {
          this.$http.post('userlogin', {'username': this.login.username, 'password': md5(this.login.password)}).then(response => {
            let res = JSON.parse(response.bodyText)
            if(res.status === 0) {
            //if(true) {
              window.sessionStorage.token = res.token
              window.sessionStorage.username = res.username
              window.sessionStorage.name = res.name
              window.sessionStorage.user_type = res.user_type
              if(res.user_type == 2) {
                this.$router.push('/admin');
              } else {
                this.$router.push('/home');
              }
            } else {
              swal({title:"出错了",text:res.message,icon:"error",button:"确定"});
            }
          }).catch(function(response) {
            console.log('Error')
          })
        }
      });
    },
    clearFrm: function() {
        this.login.username = '';
        this.login.password = '';
    },
    loginOAuth: function() {
      this.$http.get('userlogin_stucs').then((response) => {
        let json = JSON.parse(response.bodyText)
        if(json.status === 0) {
          window.location = json.url
        } else {
          swal({title:"出错了",text:json.message,icon:"error",button:"确定"});
        }
      }).catch(function(response){
        console.log('Error')
      })
    }
  },
  created() {
    if(this.$route.query.message != null) {
      alert(this.$route.query.message)
    }
  }
};
</script>
