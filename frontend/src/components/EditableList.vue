<template>
  <div>
    <el-row type="flex" justify="center" style="margin: 10px;">
      <el-col :span="24">
        <b style="line-height: 30px; font-size: 20px;">{{ model.title }}</b>
        <el-button
          icon="el-icon-question"
          circle
          v-if="model.note != null && model.note != ''"
          style="font-size: 20px;"
          @click="displayHelpMsg(model.note)"
        ></el-button>
      </el-col>
    </el-row>
    <el-form :model="model" ref="form">
      <el-table
        border
        :data="model.tableData"
        style="width: 100%;"
        :cell-style="{'vertical-align':'middle'}"
      >
        <el-table-column
          v-for="(col,index) in model.tableColumn"
          v-bind:key="index"
          :label="col.label"
          :width="col.colWidth"
        >
          <template slot="header" slot-scope="scope">
            <span>{{ col.label }}</span>
            <el-button
              icon="el-icon-question"
              circle
              v-if="col.note != null && col.note != ''"
              @click="displayHelpMsg(col.note)"
            ></el-button>
          </template>
          <template slot-scope="scope">
            <el-form-item
              :prop="'tableData.' + scope.$index + col.name"
              style="margin-bottom: 0"
              :rules="[{ required: true, message: '字段不能为空', trigger: 'blur' }]"
            >
              <el-input
                v-if="col.type === 'input'"
                v-model="model.tableData[scope.$index][col.name]"
                :disabled="isReadOnly"
              ></el-input>
              <el-date-picker
                v-if="col.type === 'date-picker'"
                v-model="model.tableData[scope.$index][col.name]"
                :disabled="isReadOnly"
              ></el-date-picker>
              <el-select
                v-if="col.type === 'selection'"
                v-model="model.tableData[scope.$index][col.name]"
                :disabled="isReadOnly"
              >
                <el-option
                  v-for="item in col.data"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                ></el-option>
              </el-select>
              <el-input-number
                v-if="col.type === 'input-number'"
                v-model="model.tableData[scope.$index][col.name]"
                :min="col.min"
                :max="col.max"
                :disabled="isReadOnly"
              ></el-input-number>
              <span v-if="col.type === 'seq'">{{ scope.$index + 1 }}</span>
              <span v-if="col.type === 'text'">{{ model.tableData[scope.$index][col.name] }}</span>
            </el-form-item>
          </template>
        </el-table-column>
        <el-table-column v-if="!isReadOnly">
          <template slot-scope="scope">
            <el-button
              type="danger"
              @click="handleDel(scope.$index)"
              v-bind:style="{'line-height': '10px'}"
            >删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-row
        v-if="!isReadOnly"
        type="flex"
        justify="start"
        style="margin-top: 20px; margin-bottom: 20px;"
      >
        <el-col :span="3">
          <el-button type="primary" @click="handleAdd">添加</el-button>
        </el-col>
      </el-row>
    </el-form>
  </div>
</template>

<script>
/* eslint-disable */
export default {
  name: "EditableList",
  props: {
    model: {
      type: Object,
      default: {}
    },
    isReadOnly: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {};
  },
  methods: {
    handleAdd() {
      let val = Object.assign({}, this.model.templateData); // deep
      val.seq = this.model.tableData.length;
      this.model.tableData.push(val);
    },
    handleDel(idx) {
      this.model.tableData.splice(idx, 1);
    },
    validate() {
      let that = this;
      return new Promise(function(resolve, reject) {
        that.$refs["form"].validate(valid =>
          valid ? resolve() : reject());
      });
    },
    getContent() {
      for (let i in this.model.tableData) {
        if (this.model.tableData[i]["seq"] != null) {
          this.model.tableData[i]["seq"] = i;
        }
      }
      return this.model.tableData;
    },
    displayHelpMsg(content) {
      this.$alert(content, "详情", {
        dangerouslyUseHTMLString: true,
        confirmButtonText: "确定",
        callback: action => {}
      });
    }
  }
};
</script>
