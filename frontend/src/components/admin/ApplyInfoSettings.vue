<template>
  <div>
    <el-table :data="tableData">
      <el-table-column prop="scholarship_name" label="奖学金名称" width="180"></el-table-column>
      <el-table-column prop="set_time" label="设置时间" width="180"></el-table-column>
      <el-table-column prop="can_apply" label="申请开关" width="200">
        <template slot-scope="scope">
          <el-switch
            v-model="scope.row.can_apply"
            @change="handleChangeAvailability($event, scope.$index, scope.row)"
          ></el-switch>
        </template>
      </el-table-column>
      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-button @click="handleEdit(scope.$index, scope.row)" type="text" size="small">编辑</el-button>
          <el-button @click="handleDelete(scope.$index, scope.row)" type="text" size="small">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-row style="margin-top: 30px;" type="flex" justify="start">
      <el-col :span="3">
        <el-button type="primary" @click="handleAdd">新增</el-button>
      </el-col>
    </el-row>
    <el-dialog :title="dialogTitle" :visible.sync="dialogVisible" width="50%">
      <el-form
        label-position="right"
        label-width="13vw"
        size="small"
        :model="scholarshipInfo"
        status-icon
      >
        <el-form-item label="奖学金名称" prop="name">
          <el-input
            v-model="scholarshipInfo.scholarship_name"
            placeholder="请输入名称"
            v-bind:style="{ width: elemWidth + 'vw' }"
          ></el-input>
        </el-form-item>
        <el-form-item label="评分规则" prop="score_rule">
          <el-select
            v-model="scholarshipInfo.score_rule"
            placeholder="请选择"
            v-bind:style="{ width: elemWidth + 'vw' }"
          >
            <el-option
              v-for="item in scoreRuleList"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="handleSubmit">确 定</el-button>
      </span>
    </el-dialog>
    <el-dialog title="提示" :visible.sync="confirmDialogVisible" width="50%">
      <span>删除操作不可恢复，请确认</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="cancelDelete">取 消</el-button>
        <el-button type="danger" @click="confirmDelete">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
/* eslint-disable */
export default {
  data() {
    return {
      elemWidth: 30,
      tableData: [],
      dialogVisible: false,
      dialogTitle: "",
      scholarshipInfo: {
        scholarship_name: "",
        score_rule: ""
      },
      scoreRuleList: [],
      confirmDialogVisible: false,
      deleteCallback: null
    };
  },
  created() {
    this.load();
  },
  methods: {
    load() {
      this.tableData = [];
      let that = this;
      this.$http
        .post("getScholarshipInfoList", {
          token: window.sessionStorage.token,
          username: window.sessionStorage.username
        })
        .then(response => {
          let json = JSON.parse(response.bodyText);
          //console.log(json)
          if (json.status == 0) {
            let arr = JSON.parse(json.data);
            arr.forEach(element => {
              let data = element.fields;
              data["pk"] = element.pk;
              data["set_time"] = new Date(data["set_time"]).toLocaleString();
              that.tableData.push(data);
            });
          } else {
            swal({
              title: "出错了",
              text: json.message,
              icon: "error",
              button: "确定"
            }).then(val => {
              if (json.status === -1) {
                that.$router.push("/");
              }
            });
          }
        })
        .catch(function(response) {
          console.log(response);
        });
    },
    getScoreRuleSettings(cb) {
      let that = this;
      this.$http
        .post("getScoreRuleList", {
          token: window.sessionStorage.token,
          username: window.sessionStorage.username
        })
        .then(response => {
          let res = JSON.parse(response.bodyText);
          if (res.status == 0) {
            let data = JSON.parse(res.data);
            that.scoreRuleList = [];
            data.forEach(element => {
              that.scoreRuleList.push({
                value: element.pk,
                label:
                  element.fields.alias +
                  "  设置于" +
                  new Date(element.fields.set_time).toLocaleString()
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
        .catch(function(response) {
          console.log(response);
        });
    },
    handleChangeAvailability(evt, idx, row) {
      console.log(evt, idx, row);
      this.$http
        .post("switchScholarshipAvailability", {
          username: window.sessionStorage.username,
          token: window.sessionStorage.token,
          data: {
            pk: row.pk,
            can_apply: row.can_apply
          }
        })
        .then(response => {
          let res = JSON.parse(response.bodyText);
          if (res.status === 0) {
            swal({
              title: "设置成功",
              icon: "success",
              button: "确定"
            });
          } else {
            swal({
              title: "出错了",
              text: json.message,
              icon: "error",
              button: "确定"
            }).then(val => {
              if (json.status === -1) {
                that.$router.push("/");
              }
            });
          }
        })
        .catch(response => {
          console.log(response);
        });
    },
    handleAdd() {
      this.scholarshipInfo = {
        scholarship_name: "",
        score_rule: ""
      };
      this.dialogTitle = "添加奖学金";
      this.dialogVisible = true;
      let that = this;
      this.getScoreRuleSettings(() => {
        that.addCallback = () => {
          that.$http
            .post("addScholarshipInfo", {
              token: window.sessionStorage.token,
              username: window.sessionStorage.username,
              data: that.scholarshipInfo
            })
            .then(response => {
              let json = JSON.parse(response.bodyText);
              console.log(json);
              if (json.status === 0) {
                that.dialogVisible = false;
                swal({
                  title: "添加成功",
                  icon: "success",
                  button: "确定"
                }).then(val => {
                  that.load();
                });
              } else {
                swal({
                  title: "出错了",
                  text: json.message,
                  icon: "error",
                  button: "确定"
                }).then(val => {
                  if (json.status === -1) {
                    that.$router.push("/");
                  }
                });
              }
            })
            .catch(function(response) {
            });
        };
      });
    },
    handleSubmit() {
      if (this.addCallback) {
        this.addCallback();
        this.addCallback = null;
      }
      if (this.editCallback) {
        this.editCallback();
        this.editCallback = null;
      }
    },
    handleDelete(idx, row) {
      let that = this;
      this.deleteCallback = () => {
        that.$http
          .post("delScholarshipInfo", {
            token: window.sessionStorage.token,
            username: window.sessionStorage.username,
            data: row.pk
          })
          .then(response => {
            let json = JSON.parse(response.bodyText);
            if (json.status === 0) {
              that.dialogVisible = false;
              swal({
                title: "删除成功",
                icon: "success",
                button: "确定"
              }).then(val => {
                that.tableData.splice(idx, 1);
              });
            } else {
              swal({
                title: "出错了",
                text: json.message,
                icon: "error",
                button: "确定"
              }).then(val => {
                if (json.status === -1) {
                  that.$router.push("/");
                }
              });
            }
          })
          .catch(function(response) {
            console.log(response);
          });
      };
      this.confirmDialogVisible = true;
    },
    handleEdit(idx, row) {
      this.dialogTitle = "编辑" + row.scholarship_name + "设置";
      this.dialogVisible = true;
      this.scholarshipInfo.scholarship_name = row.scholarship_name;
      this.scholarshipInfo.score_rule = row.apply_score_rule_id;
      let that = this;
      this.getScoreRuleSettings(() => {
        that.editCallback = () => {
          let data = that.scholarshipInfo;
          data["pk"] = row.pk;
          that.$http
            .post("editScholarshipInfo", {
              token: window.sessionStorage.token,
              username: window.sessionStorage.username,
              data: data
            })
            .then(response => {
              let json = JSON.parse(response.bodyText);
              console.log(json);
              if (json.status === 0) {
                swal({
                  title: "修改成功",
                  icon: "success",
                  button: "确定"
                });
                that.dialogVisible = false;
                that.load();
              } else {
                swal({
                  title: "出错了",
                  text: json.message,
                  icon: "error",
                  button: "确定"
                }).then(val => {
                  if (json.status === -1) {
                    that.$router.push("/");
                  }
                });
              }
            })
            .catch(function(response) {
              console.log(response);
            });
        };
      });
    },
    cancelDelete() {
      this.deleteCallback = null;
      this.confirmDialogVisible = false;
    },
    confirmDelete() {
      if (this.deleteCallback) this.deleteCallback();
      this.confirmDialogVisible = false;
    }
  }
};
</script>