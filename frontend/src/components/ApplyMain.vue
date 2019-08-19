<template>
  <div class="apply-main-container">
    <el-row type="flex" justify="start" align="middle">
      <el-col align="start">
        <h1>申请的奖学金名称</h1>
      </el-col>
    </el-row>
    <el-row type="flex" justify="start" align="middle" style="margin-top: 20px;">
      <el-col align="start">
        <el-select v-model="scholarship_name" placeholder="请选择要申请的奖学金" style="width: 30vw;"
        :disabled="readOnly || is_teacher">
          <el-option
            v-for="item in available_scholarships"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          ></el-option>
        </el-select>
      </el-col>
    </el-row>
    <el-divider></el-divider>
    <el-row type="flex" justify="start" align="middle" :gutter="0">
      <el-col align="start">
        <h1>基本信息</h1>
      </el-col>
    </el-row>
    <el-divider></el-divider>
    <el-row type="flex" justify="start">
      <el-col align="start">
        <PerInfo disabled></PerInfo>
      </el-col>
    </el-row>
    <el-row type="flex" justify="start" style="margin-top: 30px">
      <el-col align="start">
        <h1>
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
        </h1>
      </el-col>
    </el-row>
    <el-divider></el-divider>
    <el-row type="flex" justify="center" v-for="item in academic_criteria" :key="item.name">
      <el-col>
        <EditableList :model="item.content" :ref="item.name" :isReadOnly="readOnly || is_teacher"></EditableList>
      </el-col>
    </el-row>
    <el-row type="flex" justify="start" style="margin-top: 30px">
      <el-col align="start">
        <h1>
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
        </h1>
      </el-col>
    </el-row>
    <el-divider></el-divider>
    <el-row type="flex" justify="center" v-for="item in work_criteria" :key="item.name">
      <el-col>
        <EditableList :model="item.content" :ref="item.name" :isReadOnly="readOnly || is_teacher"></EditableList>
      </el-col>
    </el-row>
    <el-row type="flex" justify="start" style="margin-top: 30px">
      <el-col align="start">
        <h1>
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
        </h1>
      </el-col>
    </el-row>
    <el-divider></el-divider>
    <el-row type="flex" justify="start" style="margin-bottom: 30px;">
      <el-col :span="18" align="start">
        <el-input
          type="textarea"
          autosize
          placeholder="请输入内容"
          v-model="other_academic_awards"
          :disabled="readOnly || is_teacher"
        ></el-input>
      </el-col>
    </el-row>
    <el-row type="flex" justify="center" v-if="!readOnly && !is_teacher">
      <el-col :span="5">
        <el-button type="success" @click="onSubmit">提交</el-button>
      </el-col>
    </el-row>
    <div v-if="is_teacher">
      <el-row type="flex" justify="start">
        <el-col :span="2">
          <h1>教师评分</h1>
        </el-col>
        <el-col :span="2">
          <el-input-number
            v-model="teacher_score"
            :precision="2"
            :step="1.0"
            :min="0"
            controls-position="right"
          ></el-input-number>
        </el-col>
      </el-row>
      <el-row type="flex" justify="start" style="margin-top: 20px;">
        <el-col :span="2">
          <el-button type="primary" @click="onSubmitTeacherScore">提交评分</el-button>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
/* eslint-disable */
import PerInfo from "./PersonalInfo";
import EditableList from "./EditableList";
import { getApplyMainSettings } from "../api/basicSettings";

export default {
  data() {
    return {
      readOnly: false,
      academic_criteria: [],
      academic_note: "",
      work_criteria: [],
      work_note: "",
      other_academic_awards: "",
      other_note: "",
      is_teacher: false,
      teacher_score: 0.0,
      scholarship_name: "",
      available_scholarships: [
        {
          value: "s1",
          label: "Scholarship 1"
        },
        {
          value: "s2",
          label: "Scholarship 2"
        }
      ]
    };
  },
  components: { PerInfo, EditableList },
  created() {
    this.setReadOnly();
    let settings = getApplyMainSettings();
    this.academic_criteria = settings.academic_criteria;
    this.academic_note = settings.academic_note;
    this.work_criteria = settings.work_criteria;
    this.work_note = settings.work_note;
    this.other_note = settings.other_note;
  },
  methods: {
    setReadOnly() {
      let re_view_apply = /^\/.*?view_apply$/;
      let re_apply = /^\/.*?apply/;
      if (re_view_apply.test(this.$route.path)) {
        this.readOnly = true;
        // trigger update
      } else if (re_apply.test(this.$route.path)) {
        this.readOnly = false;
      }
    },
    onSubmitTeacherScore() {
      console.log("Teacher_score is" + this.teacher_score);
    },
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
      // TODO - send this data to server side
      // TODO - remember to include scholarship_name and id
      // because the system supports multiple types of applications simultaneously
      console.log(JSON.stringify(form_res));
    }
  },
  watch: {
    $route: function() {
      this.setReadOnly();
    }
  }
};
</script>
