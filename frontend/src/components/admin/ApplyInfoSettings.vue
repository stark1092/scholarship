<template>
  <div>
    <el-table :data="tableData">
      <el-table-column prop="scholarship_name" label="奖学金名称" width="180"></el-table-column>
      <el-table-column prop="set_date" label="设置时间" width="180"></el-table-column>
      <el-table-column prop="can_apply" label="申请开关" width="200">
        <template slot-scope="scope">
          <el-switch v-model="scope.row.can_apply"></el-switch>
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
            v-model="scholarshipInfo.name"
            placeholder="请输入名称"
            v-bind:style="{ width: elemWidth + 'vw' }"
          ></el-input>
        </el-form-item>
        <el-form-item label="评分规则" prop="score_rule">
          <el-select v-model="scholarshipInfo.score_rule" placeholder="请选择"
          v-bind:style="{ width: elemWidth + 'vw' }">
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
      editing: {}, // the scholarship currently being edited
      scholarshipInfo: {
        scholarship_name: "",
        score_rule: ""
      },
      scoreRuleList: [{
        label: "默认规则",
        value: "default"
      },{
        label: "规则2",
        value: "2"
      }],
      confirmDialogVisible: false,
      deleteCallback: null
    };
  },
  created() {
    this.tableData.push(
      {
        scholarship_name: "name",
        set_date: "date",
        can_apply: false
      },
      {
        scholarship_name: "name2",
        set_date: "date2",
        can_apply: true
      }
    );
  },
  methods: {
    handleAdd() {
      this.dialogTitle = "添加奖学金";
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
      this.dialogTitle = "编辑" + row.scholarship_name + "设置";
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