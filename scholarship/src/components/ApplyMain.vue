<template>
  <div class="apply-main-container">
    <el-row type="flex" justify="start" align="middle" :gutter="0">
      <el-col :span="2">
        <span>基本信息</span>
      </el-col>
    </el-row>
    <el-divider></el-divider>
    <el-row type="flex" justify="start">
      <el-col :span="5" :push="1">
        <PerInfo disabled></PerInfo>
      </el-col>
    </el-row>
    <el-row type="flex" justify="start" style="margin-top: 30px">
      <el-col :span="2">
        <span>
          学术成果
          <el-tooltip
            class="item"
            effect="dark"
            :content="academic_note"
            placement="top"
            v-if="academic_note"
          >
            <i class="el-icon-question"></i>
          </el-tooltip>
        </span>
      </el-col>
    </el-row>
    <el-divider></el-divider>
    <el-row type="flex" justify="center" v-for="item in academic_criteria" :key="item.name">
      <el-col :span="24">
        <EditableList :model="item.content" :ref="item.name" :isReadOnly="readOnly"></EditableList>
      </el-col>
    </el-row>
    <el-row type="flex" justify="start" style="margin-top: 30px">
      <el-col :span="2">
        <span>
          社工经历
          <el-tooltip
            class="item"
            effect="dark"
            :content="work_note"
            placement="top"
            v-if="work_note"
          >
            <i class="el-icon-question"></i>
          </el-tooltip>
        </span>
      </el-col>
    </el-row>
    <el-divider></el-divider>
    <el-row type="flex" justify="center" v-for="item in work_criteria" :key="item.name">
      <el-col :span="24">
        <EditableList :model="item.content" :ref="item.name" :isReadOnly="readOnly"></EditableList>
      </el-col>
    </el-row>
    <el-row type="flex" justify="start" style="margin-top: 30px">
      <el-col :span="2">
        <span>
          其他学术奖项
          <el-tooltip
            class="item"
            effect="dark"
            :content="other_note"
            placement="top"
            v-if="other_note"
          >
            <i class="el-icon-question"></i>
          </el-tooltip>
        </span>
      </el-col>
    </el-row>
    <el-divider></el-divider>
    <el-row type="flex" justify="start" style="margin-bottom: 30px;">
      <el-col :span="12">
        <el-input type="textarea" autosize placeholder="请输入内容" v-model="other_academic_awards" :disabled="readOnly"></el-input>
      </el-col>
    </el-row>
    <el-row type="flex" justify="center" v-if="!readOnly">
      <el-col :span="5">
        <el-button type="success" @click="onSubmit">提交</el-button>
      </el-col>
    </el-row>
  </div>
</template>

<script>
/* eslint-disable */
import PerInfo from "./PersonalInfo";
import EditableList from "./EditableList";
import { getApplyMainSettings } from "../api/basicSettings"

export default {
  data() {
    return {
      readOnly: false,
      academic_criteria: [],
      academic_note: "",
      work_criteria: [],
      work_note: "",
      other_academic_awards: "",
      other_note: ""
    };
  },
  components: { PerInfo, EditableList },
  created() {
    if (this.$route.path === "/home/view_apply") {
        this.readOnly = true
      } else if (this.$route.path === "/home/apply") {
        this.readOnly = false
    }
    let settings = getApplyMainSettings()
    this.academic_criteria = settings.academic_criteria
    this.academic_note = settings.academic_note
    this.work_criteria = settings.work_criteria
    this.work_note = settings.work_note
    this.other_note = settings.other_note
  },
  methods: {
    onSubmit() {
      let form_res = {
        academic: {},
        work: {},
        other_academic: null
      };
      let that = this;
      this.academic_criteria.forEach(item => {
        form_res.academic[item.name] = that.$refs[item.name][0].getContent();
      });
      this.work_criteria.forEach(item => {
        form_res.work[item.name] = that.$refs[item.name][0].getContent();
      });
      form_res["other_academic"] = this.other_academic_awards;
      console.log(JSON.stringify(form_res));
    }
  },
  watch: {
    $route: function() {
      if (this.$route.path === "/home/view_apply") {
        this.readOnly = true
        // trigger update
      } else if (this.$route.path === "/home/apply") {
        this.readOnly = false
      }
    }
  }
};
</script>
