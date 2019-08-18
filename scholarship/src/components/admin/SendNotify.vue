<template>
  <div>
    <el-row type="flex" justify="center">
      <el-col :span="24">
        <quill-editor
          ref="myTextEditor"
          v-model="content"
          :options="editorOption"
          @blur="onEditorBlur($event)"
          @focus="onEditorFocus($event)"
          @ready="onEditorReady($event)"
        ></quill-editor>
      </el-col>
    </el-row>
    <el-row type="flex" justify="start" style="margin-top: 30px;">
      <el-col :span="2">
        <el-button type="primary" @click="onSubmit()">发送</el-button>
      </el-col>
      <el-col :span="2">
        <el-button type="warning" @click="onClear()">清除</el-button>
      </el-col>
      <el-col :span="4">
        <el-button type="success" @click="onSubmitDocument()">从Word文档导入</el-button>
      </el-col>
    </el-row>
  </div>
</template>

<script>
/* eslint-disable */
export default {
  computed: {
    editor() {
      return this.$refs.myTextEditor.quill;
    }
  },
  methods: {
    onSubmitDocument() {
      console.log("You called onSubmitDocument");
    },
    onSubmit() {
      console.log(this.content);
    },
    onClear() {
      this.content = "";
    },
    onEditorBlur(editor) {
      //console.log("editor blur!", editor);
    },
    onEditorFocus(editor) {
      //console.log("editor focus!", editor);
    },
    onEditorReady(editor) {
      //console.log("editor ready!", editor);
    }
  },
  data() {
    return {
      content: "",
      editorOption: {
        theme: "snow",
        boundary: document.body,
        modules: {
          toolbar: [
            ["bold", "italic", "underline", "strike"],
            ["blockquote", "code-block"],
            [{ header: 1 }, { header: 2 }],
            [{ list: "ordered" }, { list: "bullet" }],
            [{ script: "sub" }, { script: "super" }],
            [{ indent: "-1" }, { indent: "+1" }],
            [{ direction: "rtl" }],
            [{ size: ["small", false, "large", "huge"] }],
            [{ header: [1, 2, 3, 4, 5, 6, false] }],
            [{ color: [] }, { background: [] }],
            [{ font: [] }],
            [{ align: [] }],
            ["clean"],
            //["link", "image", "video"]
            ["link"]
          ]
        },
        placeholder: "Insert text here ...",
        readOnly: false
      }
    };
  },
  created() {}
};
</script>