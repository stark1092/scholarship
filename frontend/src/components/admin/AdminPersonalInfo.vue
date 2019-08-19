<template>
  <el-form label-position="left" label-width="13vw" size="small" :model="perinfo" status-icon :rules="rule">
    <el-form-item label="原密码" prop="old_pwd">
      <el-input
        v-model="perinfo.old_pwd"
        placeholder="请输入原密码"
        v-bind:style="{ width: elemWidth + 'vw' }"
        :disabled="disabled"
        show-password
      ></el-input>
    </el-form-item>
    <el-form-item label="新密码" prop="new_pwd">
      <el-input
        v-model="perinfo.new_pwd"
        placeholder="请输入新密码"
        v-bind:style="{ width: elemWidth + 'vw' }"
        :disabled="disabled"
        show-password
      ></el-input>
    </el-form-item>
    <el-form-item label="新密码确认" prop="new_pwd_confirm">
      <el-input
        v-model="perinfo.new_pwd_confirm"
        placeholder="请再输入一次新密码"
        v-bind:style="{ width: elemWidth + 'vw' }"
        :disabled="disabled"
        show-password
      ></el-input>
    </el-form-item>
  </el-form>
</template>

<script>
/* eslint-disable */
export default {
  created() {},
  props: {
    disabled: {
      type: Boolean,
      default: false
    }
  },
  methods: {
      onSubmit() {
          return {
              old_pwd: this.perinfo.old_pwd,
              new_pwd: this.perinfo.new_pwd
          }
      },
      isValid() {
          return valid
      }
  },
  data() {
    var validatePass2 = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请再次输入密码"));
      } else if (value !== this.perinfo.new_pwd) {
        callback(new Error("两次输入密码不一致!"));
      } else {
        this.valid = this.old_pwd !== "" && this.new_pwd !== "";
        callback();
      }
    };
    var validatorCommon = (rule, val, cb) => {
        if(val === "") {
            this.valid = false;
            cb(new Error("密码不能为空"));
        } else {
            cb();
        }
    }
    return {
      perinfo: {
        old_pwd: "",
        new_pwd: "",
        new_pwd_confirm: ""
      },
      valid: false,
      elemWidth: 25,
      rule: {
        old_pwd: [
          { required: true, validator: validatorCommon, trigger: "blur" }
        ],
        new_pwd: [{ required: true, validator: validatorCommon, trigger: "blur" }],
        new_pwd_confirm: [
          { required: true, validator: validatePass2, trigger: "blur" }
        ]
      }
    };
  }
};
</script>
