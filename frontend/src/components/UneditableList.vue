<template>
  <el-form :model="model">
    <el-table :data="model.tableData" :stripe="stripe" style="width: 100%" class="resetPadding">
      <div v-for="(col,index) in model.tableColumn" v-bind:key="index">
        <el-table-column
        v-if="col.show"
        :label="col.label"
        :width="col.colWidth"
      >
      
        <template slot="header">
          <span>{{ col.label }}</span>
          <el-button
            icon="el-icon-question"
            circle
            v-if="col.note != null && col.note != ''"
            @click="displayHelpMsg(col.note)"
          ></el-button>
        </template>
        <template slot-scope="scope">
          <el-form-item :prop="'tableData.' + scope.$index + col.name" style="margin-bottom: 0">
            <span v-if="col.type === 'seq'">{{ model.tableData[scope.$index][col.name] + 1 }}</span>
            <span v-if="col.type === 'text'">{{ model.tableData[scope.$index][col.name] }}</span>
            <el-link
              v-if="col.type === 'link'"
              :underline="false"
              type="primary"
              @click="handleJmp(model.tableData[scope.$index][col.name].link)"
            >{{ model.tableData[scope.$index][col.name].label }}</el-link>
          </el-form-item>
        </template>
      </el-table-column>
      </div>
    </el-table>
  </el-form>
</template>

<script>
/* eslint-disable */
export default {
  name: "UneditableList",
  props: {
    stripe: {
      type: Boolean,
      default: true
    },
    model: {
      type: Object,
      default: {}
    },
    linkCb: {
      type: Function,
      default: (link)=>{}
    }
  },
  data() {
    return {};
  },
  methods: {
    displayHelpMsg(content) {
      this.$alert(content, "详情", {
        dangerouslyUseHTMLString: true,
        confirmButtonText: "确定",
        callback: action => {}
      });
    },
    handleJmp(link) {
      this.linkCb(link)
      //console.log(link);
    }
  }
};
</script>

<style>
.resetPadding td{
  padding: 0!important;
}
</style>

