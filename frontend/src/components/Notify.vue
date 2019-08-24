<template>
  <div>
    <el-table :data="tableData" style="width: 100%">
      <el-table-column prop="title" label="通知标题" width="180"></el-table-column>
      <el-table-column prop="date" label="时间" width="180"></el-table-column>
      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-button size="mini" @click="handleDetails(scope.$index, scope.row)">查看详情</el-button>
          <el-button
            v-if="isAdmin"
            size="mini"
            type="warning"
            @click="handleDel(scope.$index, scope.row)"
          >删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog title="消息内容" :visible.sync="dialogVisible" width="80%">
      <div class="innerHtml">
        <span v-html="msgContent"></span>
      </div>
      <span slot="footer" class="dialog-footer">
        <!--el-button @click="dialogVisible = false">取 消</el-button-->
        <el-button type="primary" @click="dialogVisible = false">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<style>
.ql-align-center {
  text-align: center;
}
.ql-align-justify {
  text-align: justify;
}
.ql-align-right {
  text-align: right;
}

.innerHtml {
  margin-left: 10%;
  margin-right: 10%;
  text-align: left;
}
</style>

<script>
/* eslint-disable */
export default {
  data() {
    return {
      tableData: [],
      dialogVisible: false,
      msgContent: "",
      isAdmin: window.sessionStorage.user_type === "2"
    };
  },
  created() {
    this.getNotify();
  },
  methods: {
    getNotify() {
      this.$http
        .post("getNotify", {
          token: window.sessionStorage.token,
          username: window.sessionStorage.username
        })
        .then(response => {
          let res = JSON.parse(response.bodyText);
          if (res.status === 0) {
            res.data.forEach(element => {
              element.date = new Date(element.date).toLocaleString();
            });
            this.tableData = res.data;
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
    },
    handleDetails(idx, row) {
      if (
        idx >= 0 &&
        this.tableData != null &&
        this.tableData[idx] != null &&
        this.tableData[idx].link != null
      ) {
        this.msgContent = this.tableData[idx].link;
        this.dialogVisible = true;
      }
    },
    handleDel(idx, row) {
      let that = this;
      this.$http
        .post("delNotify", {
          token: window.sessionStorage.token,
          username: window.sessionStorage.username,
          data: { id: row.id, title: row.title }
        })
        .then(response => {
          let res = JSON.parse(response.bodyText);
          if (res.status === 0) {
            that.tableData.splice(idx, 1);
            swal({ title: "删除成功", icon: "success", button: "确定" });
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
};
</script>