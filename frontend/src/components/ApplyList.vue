<template>
  <div>
    <el-form :inline="true" ref="filter_form" :model="filter" label-width="50px">
      <el-form-item label="筛选">
        <el-select v-model="filter.conditions.scholarship_name" placeholder="请选择奖学金">
          <el-option
            v-for="item in filter.scholarship_names"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          ></el-option>
        </el-select>
        <el-select v-model="filter.conditions.student_type" placeholder style="width: 5vw; min-width: 80px;">
          <el-option
            v-for="item in filter.student_types"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          ></el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-select v-model="filter.conditions.department" placeholder style="width: 8vw; min-width: 100px;">
          <el-option
            v-for="item in filter.departments"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          ></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="排序">
        <el-select v-model="filter.conditions.ordering" placeholder style="width: 7vw; min-width: 130px;">
          <el-option
            v-for="item in filter.ordering_list"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          ></el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitFilter">确定</el-button>
      </el-form-item>
      <el-form-item>
        <el-button type="success" @click="exportList" v-if="isAdmin">导出为EXCEL</el-button>
      </el-form-item>
    </el-form>
    <el-row type="flex" justify="center">
      <el-col :span="24">
        <List :model="model" :linkCb="linkCb"></List>
      </el-col>
    </el-row>
    <el-row type="flex" justify="center" style="margin-top: 1vh">
      <el-col :span="24">
        <el-pagination
          :hide-on-single-page="true"
          background
          layout="prev, pager, next"
          :page-count="numPages"
          @current-change="handlePageChange"
        ></el-pagination>
      </el-col>
    </el-row>
  </div>
</template>

<script>
/* eslint-disable */
import List from "./UneditableList";
import {
  getRoughStudentTypeList,
  getDepartmentList
} from "../api/basicSettings";

const numElemPerPage = 15;

export default {
  data() {
    return {
      isAdmin: false, // TODO - set this according to user type
      numPages: 0,
      model: {
        tableColumn: [
          {
            type: "seq",
            label: "#",
            name: "seq",
            colWidth: "50%"
          },
          {
            type: "text",
            label: "学号",
            name: "student_num"
          },
          {
            type: "text",
            label: "姓名",
            name: "name"
          },
          {
            type: "text",
            label: "A类论文",
            name: "a_paper"
          },
          {
            type: "text",
            label: "B类论文",
            name: "b_paper"
          },
          {
            type: "text",
            label: "C类论文",
            name: "c_paper"
          },
          {
            type: "text",
            label: "O类论文",
            name: "o_paper"
          },
          {
            type: "text",
            label: "专利",
            name: "patent"
          },
          {
            type: "text",
            label: "学术得分",
            name: "academic_score"
          },
          {
            type: "text",
            label: "社工得分",
            name: "work_score"
          },
          {
            type: "text",
            label: "教师评分",
            name: "teacher_score"
          },
          {
            type: "text",
            label: "总分",
            name: "tot_score"
          },
          {
            type: "text",
            label: "被举报数",
            name: "num_report",
            note:
              "发现不实信息请向thucs_scholarship@163.com举报，我们将严格保密举报者的信息"
          },
          {
            type: "link",
            label: "查看详情",
            name: "link"
          }
        ],
        tableData: []
      },
      buffer: [],
      linkCb: function(link) {
        let route = this.$router.resolve({
          path: "/home/view_apply",
          query: { stu_num: link }
        });
        window.open(route.href, "_blank");
      },
      filter: {
        conditions: {
          scholarship_name: "",
          student_type: "",
          department: "",
          ordering: ""
        },
        scholarship_names: [{
          value: "s1",
          label: "Scholarship 1"
        },{
          value: "s2",
          label: "Scholarship 2"
        }],
        student_types: getRoughStudentTypeList(),
        departments: getDepartmentList(),
        ordering_list: [
          {
            value: "tot_score",
            label: "总分"
          },
          {
            value: "academic_score",
            label: "学术得分"
          },
          {
            value: "work_score",
            label: "社工得分"
          }
        ],
      }
    };
  },
  components: { List },
  created() {
    /*
    this.$http.post('getAllApplicants', {'token': window.sessionStorage.token, 'username': window.sessionStorage.username})
    .then(response => {
      let json = JSON.parse(response.bodyText);
      if(json.status == 0) {
        this.buffer = json.applicant;
        this.numPages = Math.ceil(this.buffer.length / numElemPerPage);
        this.handlePageChange(1);
      }
    }).catch(function(response){
      console.log('Error')
    })
    */
  },
  methods: {
    handlePageChange(val) {
      this.model.tableData = this.buffer.slice(
        (val - 1) * numElemPerPage,
        val * numElemPerPage
      );
    },
    fakeAddData() {
      for (let i = 0; i < 33; ++i) {
        this.fakeAddDataHelper();
      }
    },
    fakeAddDataHelper() {
      let idx = this.buffer.length;
      this.buffer.push({
        seq: idx,
        student_num: "2017011555",
        name: "王小明",
        a_paper: "1",
        b_paper: "1",
        c_paper: "1",
        o_paper: "0",
        patent: "1",
        academic_score: "2",
        work_score: "3",
        teacher_score: "0",
        tot_score: "5",
        num_report: "0",
        link: {
          link: "2017011555",
          label: "点击查看"
        }
      });
    },
    submitFilter() {
      this.$http.post('filterAndSort', {'token': window.sessionStorage.token, 'username': window.sessionStorage.username, 
      'data': this.filter.conditions}).then(response => {
        let json = JSON.parse(response.bodyText);
        console.log(json)
        if(json.status == 0) {
          this.buffer = json.applicant;
          this.numPages = Math.ceil(this.buffer.length / numElemPerPage);
          this.handlePageChange(1);
        }
      }).catch(function(response){
        console.log('Error')
      })
    },
    exportList() {
      // submit filter to backend, and request generating excel file
    }
  }
};
</script>

