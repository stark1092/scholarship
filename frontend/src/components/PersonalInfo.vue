<template>
  <el-form label-position="right" label-width="13vw" size="small">
    <el-form-item label="姓名">
      <el-input
        v-model="perinfo.name"
        placeholder="请输入内容"
        v-bind:style="{ width: elemWidth + 'vw' }"
        disabled
      ></el-input>
    </el-form-item>
    <el-form-item label="班级">
      <el-input
        v-model="perinfo.class_name"
        placeholder="请输入内容"
        v-bind:style="{ width: elemWidth + 'vw' }"
        :disabled="disabled"
      ></el-input>
    </el-form-item>
    <el-form-item label="性别">
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
    <el-form-item label="系所">
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
    <el-form-item label="类别">
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
    <el-form-item label="年级">
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
    <el-form-item label="学籍状态">
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
    <el-form-item label="政治面貌">
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
    <el-form-item label="民族">
      <el-input
        v-model="perinfo.ethnic_group"
        placeholder="请输入内容"
        v-bind:style="{ width: elemWidth + 'vw' }"
        :disabled="disabled"
      ></el-input>
    </el-form-item>
    <el-form-item label="导师">
      <el-input
        v-model="perinfo.instructor"
        placeholder="请输入内容"
        v-bind:style="{ width: elemWidth + 'vw' }"
        :disabled="disabled"
      ></el-input>
    </el-form-item>
    <el-form-item label="邮箱">
      <el-input
        v-model="perinfo.email"
        placeholder="请输入内容"
        v-bind:style="{ width: elemWidth + 'vw' }"
        :disabled="disabled"
      ></el-input>
    </el-form-item>
    <el-form-item label="手机">
      <el-input
        v-model="perinfo.mobile"
        placeholder="请输入内容"
        v-bind:style="{ width: elemWidth + 'vw' }"
        :disabled="disabled"
      ></el-input>
    </el-form-item>
    <el-form-item label="地址">
      <el-input
        v-model="perinfo.address"
        placeholder="请输入内容"
        v-bind:style="{ width: elemWidth + 'vw' }"
        :disabled="disabled"
      ></el-input>
    </el-form-item>
    <el-form-item label="邮编">
      <el-input
        v-model="perinfo.post_code"
        placeholder="请输入内容"
        v-bind:style="{ width: elemWidth + 'vw' }"
        :disabled="disabled"
      ></el-input>
    </el-form-item>
    <el-form-item label="是否已开题">
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
  created() {
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
          if (res.status === -1) {
            this.$router.push("/");
          }
          alert(res.message);
        }
      })
      .catch(function(response) {
        console.log("Error");
      });
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
