<template>
  <div>
    <el-form :inline="true" ref="filter_form" :model="filter.conditions" label-width="50px">
      <el-form-item
        label="筛选"
        :rules="[{ required: true, message: '字段不能为空', trigger: ['change','blur'] }]"
        prop="scholarship_name"
      >
        <el-select v-model="filter.conditions.scholarship_name" placeholder="请选择奖学金">
          <div v-for="item in filter.scholarship_names" :key="item.value">            
            <el-option
            :label="item.label"
            :value="item.value"
            ></el-option>
          </div>
          
        </el-select>
      </el-form-item>
      <el-form-item
        :rules="[{ required: true, message: '字段不能为空', trigger: ['change','blur'] }]"
        prop="student_type"
      >
        <el-select
          v-model="filter.conditions.student_type"
          placeholder
          style="width: 5vw; min-width: 80px;"
        >
          <el-option
            v-for="item in filter.student_types"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          ></el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-select
          clearable
          v-model="filter.conditions.department"
          placeholder
          style="width: 8vw; min-width: 100px;"
          prop="department"
        >
          <el-option
            v-for="item in filter.departments"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          ></el-option>
        </el-select>
      </el-form-item>
      <el-form-item
        label="排序"
        :rules="[{ required: true, message: '字段不能为空', trigger: ['change','blur'] }]"
        prop="ordering"
      >
        <el-select
          v-model="filter.conditions.ordering"
          placeholder
          style="width: 7vw; min-width: 130px;"
        >
        <div v-for="item in filter.ordering_list" :key="item.value">
          <el-option      
            v-if="item.show"
            :label="item.label"
            :value="item.value"
          ></el-option>
        </div>
          
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitFilter(1);currPage=1;">确定</el-button>
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
          :current-page.sync="currPage"
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

    var main_ptr = null;

export default {
  data() {
    let isStudent = window.sessionStorage.user_type === "0"
    return {
      isAdmin: window.sessionStorage.user_type === "2",
      numPages: 0,
      currPage: 1,
      model: {
        tableColumn: [
          {
            type: "seq",
            label: "#",
            name: "seq",
            colWidth: "50%",
            show: true
          },
          {
            type: "text",
            label: "学号",
            name: "student_num",
            show: true
          },
          {
            type: "text",
            label: "姓名",
            name: "name",
            show: true
          },
          {
            type: "text",
            label: "所",
            name: "department",
            show: !this.isStudent
          },
          {
            type: "text",
            label: "导师",
            name: "instructor",
            show: !this.isStudent
          },
          {
            type: "text",
            label: "A类论文",
            name: "a_paper",
            show: true
          },
          {
            type: "text",
            label: "B类论文",
            name: "b_paper",
            show: true
          },
          {
            type: "text",
            label: "C类论文",
            name: "c_paper",
            show: true
          },
          {
            type: "text",
            label: "O类论文",
            name: "o_paper",
            show: true
          },
          {
            type: "text",
            label: "专利",
            name: "patent",
            show: true
          },
          {
            type: "text",
            label: "学术得分",
            name: "academic_score",
            show: true
          },
          {
            type: "text",
            label: "社工得分",
            name: "work_score",
            show: true
          },
          {
            type: "text",
            label: "教师评分",
            name: "teacher_score",
            show: !this.isStudent
          },
          {
            type: "text",
            label: "总分",
            name: "tot_score",
            show: true
          },
          {
            type: "text",
            label: "被举报数",
            name: "num_report",
            note:
              "发现不实信息请向thucs_scholarship@163.com举报，我们将严格保密举报者的信息",
            show: this.isStudent
          },
          {
            type: "link",
            label: "查看详情",
            name: "link",
            show: true
          }
        ],
        tableData: []
      },
      linkCb: function(link) {
        let route = this.$router.resolve({
          path: "/view_apply",
          query: {
            stu_num: link,
            scholarship: main_ptr.filter.conditions.scholarship_name
          }
        });
        window.open(route.href, "_blank");
      },
      filter: {
        conditions: {
          scholarship_name: "",
          student_type: this.isStudent ? "":"doctor",
          department: "",
          ordering: this.isStudent ? "":"tot_score"
        },
        scholarship_names: [],
        student_types: getRoughStudentTypeList(),
        departments: getDepartmentList(),
        ordering_list: [
          {
            value: "tot_score",
            label: this.isStudent ? "总分" : "基础得分",
            show: true
          },
          {
            value: "teacher_score_tot",
            label: "教师评分",
            show: !this.isStudent
          },
          {
            value: "academic_score",
            label: "学术得分",
            show: true
          },
          {
            value: "work_score",
            label: "社工得分",
            show: true
          }
        ]
      }
    };
  },
  components: { List },
  created() {
    main_ptr = this;
    this.loadScholarshipList();
  },
  methods: {
    loadScholarshipList(cb = null) {
      let that = this;
      this.$http
        .post("getAllScholarshipList", {
          username: window.sessionStorage.username,
          token: window.sessionStorage.token
        })
        .then(response => {
          let res = JSON.parse(response.bodyText);
          if (res.status === 0) {
            let data = JSON.parse(res.data);
            data.forEach(e => {
              that.filter.scholarship_names.push({
                label: e.fields.scholarship_name,
                value: e.pk
              });
            });
            if (cb) cb();
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
        .catch(err => console.log(err));
    },
    handlePageChange(val) {
      this.submitFilter(val);
    },
    fakeAddDataHelper() {
      let template = {
        seq: 0,
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
      };
    },
    submitFilter(page = 1) {
      let that = this;
      console.log("SUBMIT")
      this.$refs["filter_form"].validate(valid => {
        if (valid) {
          let data = {};
          let filter_url = this.isStudent ? "filterAndSort" : "filterAndSortPrivileged"
          Object.assign(data, this.filter.conditions);
          data.page = page;
          this.$http
            .post(filter_url, {
              token: window.sessionStorage.token,
              username: window.sessionStorage.username,
              data: data
            })
            .then(response => {
              let res = JSON.parse(response.bodyText);
              if (res.status === 0) {
                that.numPages = res.data.page_cnt;
                console.log(res.data);
                that.model.tableData = res.data.curr_entries;
                that.model.tableData.forEach(e => {
                  e.link = { link: e.student_num, label: "点击查看" };
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
                .catch(function (response) {
                    console.log(response);
                });
              } else {
                  swal({
                      title: "错误",
                      text: "请选择完整筛选条件",
                      icon: "error",
                      button: "确定"
                  });
              }
              });
            },
            exportList() {
                // submit filter to backend, and request generating excel file
                let that = this;
                this.$refs["filter_form"].validate(valid => {
                    if (valid) {
                        let data = {};
                        Object.assign(data, this.filter.conditions);
                        this.$http
                            .post(
                                "exportExcel",
                                {
                                    token: window.sessionStorage.token,
                                    username: window.sessionStorage.username,
                                    data: data
                                },
                                {responseType: "blob"}
                            )
                            .then(response => {
                                if (response.body.status !== undefined) {
                                    if (response.body.status !== 0) {
                                        swal({
                                            title: "出错了",
                                            text: response.body.message,
                                            icon: "error",
                                            button: "确定"
                                        }).then(val => {
                                            if (response.body.status === -1) {
                                                that.$router.push("/");
                                            }
                                        });
                                        return;
                                    }
                                }
                                const link = document.createElement("a");
                                let blob = new Blob([response.data], {
                                    type: "application/vnd.ms-excel"
                                });
                                link.style.display = "none";
                                link.href = URL.createObjectURL(blob);
                                link.setAttribute("download", "申请列表.xls");
                                document.body.appendChild(link);
                                link.click();
                                document.body.removeChild(link);
                            })
                            .catch(function (response) {
                                console.log(response);
                            });
                    } else {
                        swal({
                            title: "错误",
                            text: "请选择完整筛选条件",
                            icon: "error",
                            button: "确定"
                        });
                    }
                });
            }
        }
    };
</script>

