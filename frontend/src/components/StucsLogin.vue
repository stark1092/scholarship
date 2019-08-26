<template>
  <div></div>
</template>

<script>
/* eslint-disable */
export default {
  created() {
    this.$http
      .post("userlogin_stucs_cb", this.$route.query)
      .then(response => {
        let res = JSON.parse(response.bodyText);
        if (res.status === 0) {
          window.sessionStorage.token = res.token;
          window.sessionStorage.username = res.username;
          window.sessionStorage.name = res.name;
          window.sessionStorage.user_type = res.user_type;
          this.$router.push({ path: "/home" });
        } else {
          let that = this;
          swal({
            title: "出错了",
            text: res.message,
            icon: "error",
            button: "确定"
          }).then(val => {
            if (res.status === -1) {
              that.$router.push("/");
            }
          });
        }
      })
      .catch(function(response) {
        console.log(response);
      });
  }
};
</script>

