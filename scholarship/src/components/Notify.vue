<template>
  <div>
    <el-table :data="tableData" style="width: 100%">
    <el-table-column prop="title" label="通知标题" width="180"></el-table-column>
    <el-table-column prop="date" label="时间" width="180"></el-table-column>
    <el-table-column label="操作">
      <template slot-scope="scope">
        <el-button
          size="mini"
          @click="handleDetails(scope.$index, scope.row)">查看详情</el-button>
      </template>
    </el-table-column>
  </el-table>
  <el-dialog
  title="消息内容"
  :visible.sync="dialogVisible"
  width="30%">
  <span>{{ msgContent }}</span>
  <span slot="footer" class="dialog-footer">
    <!--el-button @click="dialogVisible = false">取 消</el-button-->
    <el-button type="primary" @click="dialogVisible = false">确 定</el-button>
  </span>
</el-dialog>
  </div>
</template>

<script>
/* eslint-disable */
export default {
  data() {
    return {
      tableData: [],
      dialogVisible: false,
      msgContent: '',
    };
  },
  created() {
    this.getNotify()
  },
  methods: {
    getNotify() {
      /*this.$http.get('get_notify').then((response) => {
          let json = JSON.parse(response.bodyText);
          if(json.status == 0) {
            this.tableData = json.notify
          }
        }).catch(function(response){
          console.log('Error')
        })*/
    },
    handleDetails(idx, row) {
      if(idx >= 0 && this.tableData != null && this.tableData[idx] != null && this.tableData[idx].link != null) {
        this.msgContent = this.tableData[idx].link;
        this.dialogVisible = true;
      }
    }
  }
};
</script>