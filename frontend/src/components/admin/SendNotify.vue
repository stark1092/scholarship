<template>
  <div>
    <el-row type="flex" justify="start" align="middle">
      <el-col align="start" :span="2">
        <h1>通知标题</h1>
      </el-col>
      <el-col align="start" justify="start" :span="6">
        <el-input v-model="title" placeholder="请输入通知标题" style="width: 20vw;"></el-input>
      </el-col>
    </el-row>
    <el-divider></el-divider>
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
      <el-col :span="2" align="start" justify="start">
        <el-button type="warning" @click="onClear()">清除</el-button>
      </el-col>
      <el-col :span="8" align="start" justify="start">
        <el-upload
          ref="upload"
          action
          :multiple="false"
          accept=".docx,.DOCX"
          :on-change="handleChange"
          :file-list="fileList"
          :limit="1"
          :http-request="myUpload"
          :auto-upload="false"
        >
          <el-button slot="trigger" type="primary">选取Word文档导入</el-button>
          <el-button style="margin-left: 10px;" type="success" @click="onSubmitDocument">上传到服务器</el-button>
          <div slot="tip" class="el-upload__tip">只能上传docx文件, 不支持doc</div>
        </el-upload>
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
    myUpload(content) {
      if (this.title.trim() === "") {
        swal({
          title: "错误",
          text: "通知标题不能为空",
          icon: "error",
          button: "确定"
        });
        return;
      }
      let that = this;
      let form = new FormData();
      form.append("file", content.file);
      form.append("title", this.title);
      form.append("token", window.sessionStorage.token);
      form.append("username", window.sessionStorage.username);
      this.$http
        .post("sendNotifyUpload", form, {
          headers: { "Content-Type": "multipart/form-data" },
          progress(e) {
            if (e.lengthComputable) {
              let percent = (e.loaded / e.total) * 100;
              content.onProgress({ percent: percent });
            }
          }
        })
        .then(response => {
          let res = JSON.parse(response.bodyText);
          if (res.status === 0) {
            content.onSuccess();
            that.$refs.upload.clearFiles();
            swal({
              title: "文件上传成功",
              icon: "success",
              button: "确定"
            });
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
        .catch(function(res) {
          console.log(res);
        });
    },
    handleChange(file, fileList) {
      let name = file.name.split(".");
      name = name[name.length - 1];
      const ext = name === "docx" || name === "DOCX";
      const size = file.size < 10 * 1024 * 1024;
      if (!ext) {
        swal({ title: "错误", text: "文件必须为DOCX，不支持DOC", icon: "error" });
        this.$refs.upload.uploadFiles = [];
      } else if (!size) {
        swal({ title: "错误", text: "文件大小不能超过10M", icon: "error" });
        this.$refs.upload.uploadFiles = [];
      } else {
        this.$refs.upload.uploadFiles = [file];
      }
    },
    onSubmitDocument() {
      this.$refs.upload.submit();
    },
    onSubmit() {
      if (this.title.trim() === "" || this.content.trim() === "") {
        swal({
          title: "错误",
          text: "通知标题或内容不能为空",
          icon: "error",
          button: "确定"
        });
      } else {
        this.$http
          .post("sendNotify", {
            token: window.sessionStorage.token,
            username: window.sessionStorage.username,
            data: { title: this.title, link: this.content }
          })
          .then(response => {
            let res = JSON.parse(response.bodyText);
            if (res.status === 0) {
              swal({
                title: "消息发送成功",
                icon: "success",
                button: "确定"
              });
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
            console.log(response);
          });
      }
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
      title: "",
      fileList: [],
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