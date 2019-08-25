<template>
  <div class="apply-main-container">
    <el-row type="flex" justify="start" align="middle">
      <el-col align="start">
        <h1>奖学金名称</h1>
      </el-col>
    </el-row>
    <el-row type="flex" justify="start" align="middle" style="margin-top: 20px;">
      <el-col align="start">
        <el-select
          @change="onSelectScholarship"
          v-model="scholarship_id"
          placeholder="请选择奖学金"
          style="width: 30vw;"
        >
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
    <el-row type="flex" justify="start" align="middle">
      <el-col align="start">
        <h1>申请状态: {{ isApplied ? '已申请' : '未申请'}}</h1>
      </el-col>
    </el-row>
    <el-row v-if="isApplied" type="flex" justify="start" align="middle" style="margin-top: 10px;">
      <el-col align="start">
        <el-button type="danger" @click="withdrawApplyInfo">撤回申请</el-button>
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
        <PerInfo disabled ref="perinfo"></PerInfo>
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
    <el-row type="flex" justify="center" v-if="!readOnly && !is_teacher && scholarship_id != ''">
      <el-col :span="3">
        <el-button type="success" @click="onSubmit">提交</el-button>
      </el-col>
      <el-col :span="3">
        <el-button type="info" @click="onSave">暂存</el-button>
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
      formValidationRes: [],
      readOnly: false,
      academic_criteria: [],
      academic_note: "",
      work_criteria: [],
      work_note: "",
      other_academic_awards: "",
      other_note: "",
      is_teacher: window.sessionStorage.user_type === "1",
      teacher_score: 0.0,
      scholarship_id: "",
      isApplied: false,
      available_scholarships: []
    };
  },
  components: { PerInfo, EditableList },
  created() {
    this.setReadOnly();
    let that = this;
    this.$http
      .post("getAvailableScholarshipList", {
        username: window.sessionStorage.username,
        token: window.sessionStorage.token
      })
      .then(response => {
        let res = JSON.parse(response.bodyText);
        if (res.status === 0) {
          res = JSON.parse(res.data);
          res.forEach(e => {
            that.available_scholarships.push({
              value: e.pk,
              label: e.fields.scholarship_name
            });
          });
        } else {
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
      .catch(response => {
        console.log(response);
        console.log("Err");
      });
  },
  methods: {
    setFormData(form) {
      Object.keys(form.academic).forEach(key => {
        this.$refs[key][0].setContent(form.academic[key]);
      })
      Object.keys(form.work).forEach(key => {
        this.$refs[key][0].setContent(form.work[key]);
      })
      this.other_academic_awards = form.other_academic;
    },
    withdrawApplyInfo() {

    },
    onSelectScholarship(val) {
      let that = this;
      this.$http
        .post("getScholarshipMaterial", {
          username: window.sessionStorage.username,
          token: window.sessionStorage.token,
          data: String(val)
        })
        .then(response => {
          let res = JSON.parse(response.bodyText);
          if (res.status === 0) {
            res = JSON.parse(res.data);
            that.academic_criteria = res.academic_criteria;
            that.academic_note = res.academic_note;
            that.work_criteria = res.work_criteria;
            that.work_note = res.work_note;
            that.other_note = res.other_note;
            that.$http
              .post("obtainApplyInfo", {
                username: window.sessionStorage.username,
                token: window.sessionStorage.token,
                data: { scholarship_id: val }
              })
              .then(response => {
                let res = JSON.parse(response.bodyText);
                if (res.status === 0) {
                  if(res.data !== "") {
                    that.isApplied = true;
                    res = JSON.parse(res.data)
                    that.setFormData(res)
                  } else
                    that.isApplied = false;
                } else {
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
              .catch(response => {
                console.log("Err");
              });
          } else {
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
        .catch(response => {
          console.log(response);
          console.log("Err");
        });
    },
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
    onSave() {
      // no need to validate form because it is temporarily saved
      let that = this;
      let form_res = {
        academic: {},
        work: {},
        other_academic: null
      };
      that.academic_criteria.forEach(item => {
        form_res.academic[item.name] = that.$refs[item.name][0].getContent();
      });
      that.work_criteria.forEach(item => {
        form_res.work[item.name] = that.$refs[item.name][0].getContent();
      });
      form_res["other_academic"] = that.other_academic_awards;
      // TODO - send this data to server side
      // TODO - remember to include scholarship_name and id
      // because the system supports multiple types of applications simultaneously
      console.log(JSON.stringify(form_res));
    },
    onSubmit() {
      if (!this.$refs.perinfo.checkEmpty()) {
        swal({
          title: "错误",
          text: "补全所有个人信息后方能正式申请",
          icon: "error",
          button: "确定"
        });
        return;
      }
      let that = this;
      this.formValidationRes = [];
      this.academic_criteria.forEach(item =>
        that.formValidationRes.push(that.$refs[item.name][0].validate())
      );
      this.work_criteria.forEach(item =>
        that.formValidationRes.push(that.$refs[item.name][0].validate())
      );
      Promise.all(that.formValidationRes)
        .then(function() {
          let form_res = {
            academic: {},
            work: {},
            other_academic: null
          };
          that.academic_criteria.forEach(item => {
            form_res.academic[item.name] = that.$refs[
              item.name
            ][0].getContent();
          });
          that.work_criteria.forEach(item => {
            form_res.work[item.name] = that.$refs[item.name][0].getContent();
          });
          form_res["other_academic"] = that.other_academic_awards;
          that.$http
            .post("sendApplyInfo", {
              username: window.sessionStorage.username,
              token: window.sessionStorage.token,
              data: {
                scholarship_id: that.scholarship_id,
                form: JSON.stringify(form_res)
              }
            })
            .then(response => {
              let res = JSON.parse(response.bodyText);
              if (res.status === 0) {
                swal({
                  title: "申请成功",
                  icon: "success",
                  button: "确定"
                }).then(val => {
                  that.$router.go(0);
                });
              } else {
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
            .catch(response => {
              console.log(response);
              console.log("Err");
            });
        })
        .catch(function() {
          swal({
            title: "错误",
            icon: "error",
            text: "请检查所有表单项是否完整填写",
            button: "确定"
          });
        });
    }
  },
  watch: {
    $route: function() {
      this.setReadOnly();
    }
  }
};
</script>
