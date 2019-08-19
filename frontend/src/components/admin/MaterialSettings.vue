<template>
  <div>
    <el-table :data="tableData">
      <el-table-column prop="alias" label="规则名称" width="180"></el-table-column>
      <el-table-column prop="set_date" label="设置时间" width="180"></el-table-column>
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
    <el-dialog :title="dialogTitle" :visible.sync="dialogVisible" width="40%">
      <el-form
        label-position="left"
        label-width="10vw"
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
            v-model="materialRule.json"
          ></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="handleSubmit">确 定</el-button>
      </span>
    </el-dialog>
    <el-dialog title="提示" :visible.sync="confirmDialogVisible" width="30%">
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
      elemWidth: 20,
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
    this.tableData.push(
      {
        alias: "name",
        set_date: "date"
      },
      {
        alias: "name2",
        set_date: "date2"
      }
    );
  },
  methods: {
    handleAdd() {
      this.materialRule = {
        alias: "",
        json: ""
      };
      this.dialogTitle = "添加规则";
      this.dialogVisible = true;
    },
    handleSubmit() {
      this.editing = {};
    },
    handleDelete(idx, row) {
      let that = this;
      this.deleteCallback = () => {
        that.tableData.splice(idx, 1);
      };
      this.confirmDialogVisible = true;
    },
    handleEdit(idx, row) {
      this.editing = row;
      this.dialogTitle = "编辑规则" + row.alias;
      this.dialogVisible = true;
    },
    cancelDelete() {
      this.deleteCallback = null;
      this.confirmDialogVisible = false;
    },
    confirmDelete() {
      if(this.deleteCallback)
        this.deleteCallback();
      this.confirmDialogVisible = false;
    }
  }
};
</script>