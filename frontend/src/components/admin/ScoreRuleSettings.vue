<template>
  <div>
    <el-table :data="tableData">
      <el-table-column prop="alias" label="规则名称" width="180"></el-table-column>
      <el-table-column prop="set_time" label="设置时间" width="180"></el-table-column>
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
        label-width="10vw"
        size="small"
        :model="scoreRule"
        status-icon
      >
        <el-form-item label="规则名称" prop="alias">
          <el-input
            v-model="scoreRule.alias"
            placeholder="请输入名称"
            v-bind:style="{ width: elemWidth + 'vw' }"
          ></el-input>
        </el-form-item>
        <el-form-item label="对应提交材料规则" prop="apply_material_id">
          <el-select
            v-model="scoreRule.apply_material_id"
            placeholder="请选择"
            v-bind:style="{ width: elemWidth + 'vw' }"
          >
            <el-option
              v-for="item in applyMaterialList"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="评分规则设置Json" prop="json">
          <el-input
            type="textarea"
            :autosize="{ minRows: 5, maxRows: 20 }"
            placeholder="若不清楚选项，请勿更改"
            v-bind:style="{ width: elemWidth + 'vw' }"
            v-model="scoreRule.json"
          ></el-input>
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
      scoreRule: {
        alias: "",
        apply_material_id: "",
        json: ""
      },
      applyMaterialList: [],
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
        .post("getScoreRuleList", {
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
    getMaterialSettings(cb) {
      let that = this;
      this.$http
        .post("getMaterialList", {
          token: window.sessionStorage.token,
          username: window.sessionStorage.username
        })
        .then(response => {
          let res = JSON.parse(response.bodyText);
          if (res.status == 0) {
            let data = JSON.parse(res.data);
            this.applyMaterialList = [];
            data.forEach(element => {
              this.applyMaterialList.push({
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
    handleAdd() {
      this.editCallback = null;
      this.scoreRule = {
        alias: "",
        apply_material_id: "",
        json: ""
      };
      this.dialogTitle = "添加规则";
      this.dialogVisible = true;
      let that = this;
      this.getMaterialSettings(() => {
        that.addCallback = () => {
          that.$http
            .post("addScoreRule", {
              token: window.sessionStorage.token,
              username: window.sessionStorage.username,
              data: that.scoreRule
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
              console.log(response);
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
          .post("delScoreRule", {
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
      this.addCallback = null;
      this.dialogTitle = "编辑规则" + row.alias;
      this.dialogVisible = true;
      this.scoreRule.alias = row.alias;
      this.scoreRule.apply_material_id = row.apply_material_id;
      let that = this;
      this.getMaterialSettings(() => {
        that.$http
          .post("getScoreRule", {
            username: window.sessionStorage.username,
            token: window.sessionStorage.token,
            data: row.pk
          })
          .then(response => {
            let res = JSON.parse(response.bodyText);
            if (res.status === 0) {
              that.scoreRule.json = res.data;
              that.editCallback = () => {
                let data = that.scoreRule;
                data["pk"] = that.tableData[idx]["pk"];
                that.$http
                  .post("editScoreRule", {
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