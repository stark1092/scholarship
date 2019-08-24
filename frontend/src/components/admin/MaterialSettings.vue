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
        label-width="15vw"
        size="small"
        :model="materialRule"
        status-icon
      >
        <el-form-item label="规则名称" prop="alias">
          <el-input
            v-model="materialRule.alias"
            placeholder="请输入名称"
            v-bind:style="{ width: elemWidth + 'vw' }"
          ></el-input>
        </el-form-item>
        <el-form-item label="提交材料规则设置Json" prop="json">
          <el-input
            type="textarea"
            :autosize="{ minRows: 5, maxRows: 20 }"
            placeholder="若不清楚选项，请勿更改"
            v-bind:style="{ width: elemWidth + 'vw' }"
            v-model="materialRule.json"
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
      confirmDialogVisible: false,
      dialogTitle: "",
      editing: {}, // the scholarship currently being edited
      materialRule: {
        alias: "",
        json: ""
      },
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
        .post("getMaterial", {
          token: window.sessionStorage.token,
          username: window.sessionStorage.username
        })
        .then(response => {
          let json = JSON.parse(response.bodyText);
          //console.log(json)
          if (json.status == 0) {
            let arr = JSON.parse(json.data);
            // console.log(arr);
            arr.forEach(element => {
              let data = element.fields;
              data["pk"] = element.pk;
              data["set_time"] = new Date(data["set_time"]).toLocaleString();
              that.tableData.push(data);
            });
          } else {
            let that = this;
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
          console.log("Error");
        });
    },
    handleAdd() {
      this.materialRule = {
        alias: "",
        json: ""
      };
      this.dialogTitle = "添加规则";
      this.dialogVisible = true;
      let that = this;
      this.addCallback = () => {
        this.$http
          .post("addMaterial", {
            token: window.sessionStorage.token,
            username: window.sessionStorage.username,
            data: this.materialRule
          })
          .then(response => {
            let json = JSON.parse(response.bodyText);
            console.log(json);
            if (json.status === 0) {
              this.dialogVisible = false;
              that.load();
            } else {
              let that = this;
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
            console.log("Error");
          });
      };
    },
    handleSubmit() {
      this.editing = {};
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
        console.log(that.tableData[idx]["pk"]);
        this.$http
          .post("delMaterial", {
            token: window.sessionStorage.token,
            username: window.sessionStorage.username,
            data: this.tableData[idx]["pk"]
          })
          .then(response => {
            let json = JSON.parse(response.bodyText);
            console.log(json);
            if (json.status === 0) {
              this.dialogVisible = false;
              that.tableData.splice(idx, 1);
            } else {
              let that = this;
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
            console.log("Error");
          });
      };
      this.confirmDialogVisible = true;
    },
    handleEdit(idx, row) {
      this.editing = row;
      this.dialogTitle = "编辑规则" + row.alias;
      this.dialogVisible = true;
      this.materialRule.alias = this.tableData[idx].alias;
      this.materialRule.json = this.tableData[idx].json;
      let that = this;
      this.editCallback = () => {
        let data = this.materialRule;
        data["pk"] = this.tableData[idx]["pk"];
        this.$http
          .post("editMaterial", {
            token: window.sessionStorage.token,
            username: window.sessionStorage.username,
            data: data
          })
          .then(response => {
            let json = JSON.parse(response.bodyText);
            console.log(json);
            if (json.status === 0) {
              this.dialogVisible = false;
              that.load();
            } else {
              let that = this;
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
            console.log("Error");
          });
      };
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