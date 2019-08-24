<template>
  <el-form
    label-position="right"
    label-width="13vw"
    size="small"
    :model="perinfo"
    ref="form"
    v-observe-visibility="visibilityChanged"
  >
    <el-form-item label="姓名" prop="name">
      <el-input
        v-model="perinfo.name"
        placeholder="请输入内容"
        v-bind:style="{ width: elemWidth + 'vw' }"
        disabled
      ></el-input>
    </el-form-item>
    <el-form-item
      label="班级"
      prop="class_name"
      :rules="[{ required: true, message: '字段不能为空', trigger: ['change','blur'] }]"
    >
      <el-input
        v-model="perinfo.class_name"
        placeholder="请输入内容"
        v-bind:style="{ width: elemWidth + 'vw' }"
        :disabled="disabled"
      ></el-input>
    </el-form-item>
    <el-form-item
      label="性别"
      prop="gender"
      :rules="[{ required: true, message: '字段不能为空', trigger: ['change','blur'] }]"
    >
      <el-select
        v-model="perinfo.gender"
        placeholder="请选择"
        v-bind:style="{ width: elemWidth + 'vw' }"
        :disabled="disabled"
      >
        <el-option
          v-for="item in gender_list"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        ></el-option>
      </el-select>
    </el-form-item>
    <el-form-item
      label="系所"
      prop="department"
      :rules="[{ required: true, message: '字段不能为空', trigger: ['change','blur'] }]"
    >
      <el-select
        v-model="perinfo.department"
        placeholder="请选择"
        v-bind:style="{ width: elemWidth + 'vw' }"
        :disabled="disabled"
      >
        <el-option
          v-for="item in department_list"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        ></el-option>
      </el-select>
    </el-form-item>
    <el-form-item
      label="类别"
      prop="student_type"
      :rules="[{ required: true, message: '字段不能为空', trigger: ['change','blur'] }]"
    >
      <el-select
        v-model="perinfo.student_type"
        placeholder="请选择"
        v-bind:style="{ width: elemWidth + 'vw' }"
        :disabled="disabled"
      >
        <el-option
          v-for="item in type_list"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        ></el-option>
      </el-select>
    </el-form-item>
    <el-form-item
      label="年级"
      prop="grade"
      :rules="[{ required: true, message: '字段不能为空', trigger: ['change','blur'] }]"
    >
      <el-select
        v-model="perinfo.grade"
        placeholder="请选择"
        v-bind:style="{ width: elemWidth + 'vw' }"
        :disabled="disabled"
      >
        <el-option
          v-for="item in grade_list"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        ></el-option>
      </el-select>
    </el-form-item>
    <el-form-item
      label="学籍状态"
      prop="student_status"
      :rules="[{ required: true, message: '字段不能为空', trigger: ['change','blur'] }]"
    >
      <el-select
        v-model="perinfo.student_status"
        placeholder="请选择"
        v-bind:style="{ width: elemWidth + 'vw' }"
        :disabled="disabled"
      >
        <el-option
          v-for="item in status_list"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        ></el-option>
      </el-select>
    </el-form-item>
    <el-form-item
      label="政治面貌"
      prop="political_status"
      :rules="[{ required: true, message: '字段不能为空', trigger: ['change','blur'] }]"
    >
      <el-select
        v-model="perinfo.political_status"
        placeholder="请选择"
        v-bind:style="{ width: elemWidth + 'vw' }"
        :disabled="disabled"
      >
        <el-option
          v-for="item in political_status_list"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        ></el-option>
      </el-select>
    </el-form-item>
    <el-form-item
      label="民族"
      prop="ethnic_group"
      :rules="[{ required: true, message: '字段不能为空', trigger: ['change','blur'] }]"
    >
      <el-input
        v-model="perinfo.ethnic_group"
        placeholder="请输入内容"
        v-bind:style="{ width: elemWidth + 'vw' }"
        :disabled="disabled"
      ></el-input>
    </el-form-item>
    <el-form-item
      label="导师"
      prop="instructor"
      :rules="[{ required: true, message: '字段不能为空', trigger: ['change','blur'] }]"
    >
      <el-input
        v-model="perinfo.instructor"
        placeholder="请输入内容"
        v-bind:style="{ width: elemWidth + 'vw' }"
        :disabled="disabled"
      ></el-input>
    </el-form-item>
    <el-form-item
      label="邮箱"
      prop="email"
      :rules="[{ required: true, message: '字段不能为空', trigger: ['change','blur'] }]"
    >
      <el-input
        v-model="perinfo.email"
        placeholder="请输入内容"
        v-bind:style="{ width: elemWidth + 'vw' }"
        :disabled="disabled"
      ></el-input>
    </el-form-item>
    <el-form-item
      label="手机"
      prop="mobile"
      :rules="[{ required: true, message: '字段不能为空', trigger: ['change','blur'] }]"
    >
      <el-input
        v-model="perinfo.mobile"
        placeholder="请输入内容"
        v-bind:style="{ width: elemWidth + 'vw' }"
        :disabled="disabled"
      ></el-input>
    </el-form-item>
    <el-form-item
      label="地址"
      prop="address"
      :rules="[{ required: true, message: '字段不能为空', trigger: ['change','blur'] }]"
    >
      <el-input
        v-model="perinfo.address"
        placeholder="请输入内容"
        v-bind:style="{ width: elemWidth + 'vw' }"
        :disabled="disabled"
      ></el-input>
    </el-form-item>
    <el-form-item
      label="邮编"
      prop="post_code"
      :rules="[{ required: true, message: '字段不能为空', trigger: ['change','blur'] }]"
    >
      <el-input
        v-model="perinfo.post_code"
        placeholder="请输入内容"
        v-bind:style="{ width: elemWidth + 'vw' }"
        :disabled="disabled"
      ></el-input>
    </el-form-item>
    <el-form-item
      label="是否已开题"
      prop="is_project_started"
      :rules="[{ required: true, message: '字段不能为空', trigger: ['change','blur'] }]"
    >
      <el-select
        v-model="perinfo.is_project_started"
        placeholder="请选择"
        v-bind:style="{ width: elemWidth + 'vw' }"
        :disabled="disabled"
      >
        <el-option
          v-for="item in is_projected_started_list"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        ></el-option>
      </el-select>
    </el-form-item>
  </el-form>
</template>

<script>
/* eslint-disable */
import {
  getDepartmentList,
  getGenderList,
  getSpecificStudentTypeList,
  getRoughStudentTypeList,
  getStudentStatusList,
  getPoliticalStatusList,
  getGradeList
} from "../api/basicSettings.js";
export default {
  methods: {
    visibilityChanged(isVisible, entry) {
      if (isVisible) {
        this.$http
          .post("getPersonalInfo", {
            token: window.sessionStorage.token,
            username: window.sessionStorage.username
          })
          .then(response => {
            let res = JSON.parse(response.bodyText);
            if (res.status === 0) {
              this.perinfo = res.data;
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
            console.log("Error");
          });
      }
    }
  },
  props: {
    disabled: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      perinfo: {
        name: "",
        class_name: "",
        gender: "",
        department: "",
        student_type: "",
        grade: "",
        student_status: "",
        political_status: "",
        ethnic_group: "",
        instructor: "",
        email: "",
        mobile: "",
        address: "",
        post_code: ""
      },
      gender_list: getGenderList(),
      department_list: getDepartmentList(),
      type_list: getSpecificStudentTypeList(),
      grade_list: getGradeList(),
      status_list: getStudentStatusList(),
      political_status_list: getPoliticalStatusList(),
      is_projected_started_list: [
        {
          value: true,
          label: "是"
        },
        {
          value: false,
          label: "否"
        }
      ],
      elemWidth: 20
    };
  }
};
</script>
