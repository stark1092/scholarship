<template>
    <div class="apply-main-container">
        <el-row align="middle" justify="start" type="flex">
            <el-col align="start">
                <h1>奖学金名称</h1>
            </el-col>
        </el-row>
        <el-row align="middle" justify="start" style="margin-top: 20px;" type="flex">
            <el-col align="start">
                <el-select
                    :disabled="scholarship_id_preset != ''"
                    @change="onSelectScholarship"
                    placeholder="请选择奖学金"
                    style="width: 30vw;"
                    v-model="scholarship_id"
                >
                    <el-option
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                        v-for="item in available_scholarships"
                    ></el-option>
                </el-select>
            </el-col>
        </el-row>
        <el-divider></el-divider>
        <el-row align="middle" justify="start" type="flex">
            <el-col align="start">
                <h1>申请状态: {{ scholarship_id === "" ? "请选择奖学金" : (isApplied ? '已申请' : '未申请') }}</h1>
            </el-col>
        </el-row>
        <el-row
            align="middle"
            justify="start"
            style="margin-top: 10px;"
            type="flex"
            v-if="isApplied && !stu_num && !is_teacher && !readOnly"
        >
            <el-col align="start">
                <el-button @click="withdrawApplyInfo" type="danger">撤回申请</el-button>
            </el-col>
        </el-row>
        <el-divider></el-divider>
        <div v-if="!readOnly">
            <el-row align="middle" justify="start" type="flex">
                <el-col align="start">
                    <h1>导入以前的申请</h1>
                </el-col>
            </el-row>
            <el-row align="middle" justify="start" style="margin-top: 20px;" type="flex">
                <el-col align="start">
                    <el-select
                        @change="onSelectFormerScholarship"
                        placeholder="请选择以前申请的奖学金"
                        style="width: 30vw;"
                        v-model="scholarship_former_id"
                    >
                        <el-option
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                            v-for="item in all_scholarships"
                        ></el-option>
                    </el-select>
                </el-col>
            </el-row>
            <el-divider></el-divider>
        </div>
        <el-row :gutter="0" align="middle" justify="start" type="flex">
            <el-col align="start">
                <h1>基本信息</h1>
            </el-col>
        </el-row>
        <el-divider></el-divider>
        <el-row justify="start" type="flex">
            <el-col align="start">
                <PerInfo :stu_num="stu_num" disabled ref="perinfo"></PerInfo>
            </el-col>
        </el-row>
        <el-row justify="start" style="margin-top: 30px" type="flex">
            <el-col align="start">
                <h1>
                    学术成果
                    <el-tooltip
                        :content="academic_note"
                        class="item"
                        effect="dark"
                        placement="top"
                        v-if="academic_note"
                    >
                        <i class="el-icon-question"></i>
                    </el-tooltip>
                </h1>
            </el-col>
        </el-row>
        <el-divider></el-divider>
        <el-row :key="item.name" justify="center" type="flex" v-for="item in academic_criteria_computed">
            <el-col>
                <EditableList :isReadOnly="readOnly || is_teacher" :model="item.content" :ref="item.name"></EditableList>
            </el-col>
        </el-row>
        <el-row justify="start" style="margin-top: 30px" type="flex">
            <el-col align="start">
                <h1>
                    社工经历
                    <el-tooltip :content="work_note" class="item" effect="dark" placement="top" v-if="work_note">
                        <i class="el-icon-question"></i>
                    </el-tooltip>
                </h1>
            </el-col>
        </el-row>
        <el-divider></el-divider>
        <el-row :key="item.name" justify="center" type="flex" v-for="item in work_criteria">
            <el-col>
                <EditableList :isReadOnly="readOnly || is_teacher" :model="item.content" :ref="item.name"></EditableList>
            </el-col>
        </el-row>
        <el-row justify="start" style="margin-top: 30px" type="flex">
            <el-col align="start">
                <h1>
                    其他加分项
                    <el-tooltip :content="other_note" class="item" effect="dark" placement="top" v-if="other_note">
                        <i class="el-icon-question"></i>
                    </el-tooltip>
                </h1>
            </el-col>
        </el-row>
        <el-divider></el-divider>
        <el-row justify="start" style="margin-bottom: 10px;" type="flex">
            <el-col :span="18" align="start">
                <el-input
                    :disabled="readOnly || is_teacher"
                    autosize
                    placeholder="请输入内容"
                    type="textarea"
                    v-model="other_academic_awards"
                ></el-input>
            </el-col>
        </el-row>
        <!--Remove tag-->
        <el-row justify="start" style="margin-bottom: 30px;" type="flex" v-if="!is_teacher && scholarship_id != ''">
            <el-col :span="12" align="start">
                <el-checkbox-group :disabled="readOnly || is_teacher" v-model="useSpecialAct">
                    <el-checkbox name="confirmed">使用专项活动加分</el-checkbox>
                </el-checkbox-group>
            </el-col>
        </el-row>
        <!--End remove tag-->
        <el-row justify="center" type="flex" v-if="!readOnly && !is_teacher && scholarship_id != ''">
            <el-col :span="3">
                <el-button @click="onSubmit" type="success">提交</el-button>
            </el-col>
            <el-col :span="3">
                <el-button @click="onSave(false)" type="info">暂存</el-button>
            </el-col>
        </el-row>
        <div v-if="is_teacher && isApplied">
            <el-row justify="start" style="align-items: center;" type="flex">
                <el-col :span="5">
                    <h1>教师评分(1-10分，精确到一位小数)</h1>
                </el-col>
                <el-col :span="2">
                    <el-input-number
                        :max="10"
                        :min="0"
                        :precision="1"
                        :step="1"
                        controls-position="right"
                        v-model="teacher_score"
                    ></el-input-number>
                </el-col>
            </el-row>
            <el-row justify="start" style="margin-top: 20px;" type="flex">
                <el-col :span="2">
                    <el-button @click="onSubmitTeacherScore" type="primary">提交评分</el-button>
                </el-col>
            </el-row>
        </div>
    </div>
</template>

<style scoped>
h1 {
    font-size: 1.17em;
    margin-block-start: 1em;
    margin-block-end: 1em;
}

.apply-main-container {
    padding-left: 20px;
}
</style>

<script>
/* eslint-disable */
import PerInfo from './PersonalInfo';
import EditableList from './EditableList';
import { getApplyMainSettings } from '../api/basicSettings';

function* reverseKeys(arr) {
  var key = arr.length - 1;

  while (key >= 0) {
    yield key;
    key -= 1;
  }
}

export default {
    computed: {
        academic_criteria_computed: function() {
            if (window.sessionStorage.user_type === '1') {
                this.academic_criteria.forEach(criterion => {
                    for(let idx of reverseKeys(criterion.content.tableColumn)) {
                      let item = criterion.content.tableColumn[idx];
                      if (
                            item.label === '开会时间' ||
                            item.label === '出版日期'
                        )
                            criterion.content.tableColumn.splice(idx, 1);
                        else if (item.label === '公开（公告）号')
                            item.label = '授权号';
                        else if (item.label === '公开（公告）日期')
                            item.label = '授权日期';
                    }
                });
            }
            return this.academic_criteria;
        }
    },
    data() {
        return {
            useSpecialAct: false,
            formValidationRes: [],
            readOnly: false,
            apply_id: 0,
            academic_criteria: [],
            academic_note: '',
            work_criteria: [],
            work_note: '',
            other_academic_awards: '',
            other_note: '',
            is_teacher: window.sessionStorage.user_type === '1',
            teacher_score: 0.0,
            scholarship_id: '',
            scholarship_former_id: '',
            isApplied: false,
            stu_num: this.$route.query.stu_num,
            scholarship_id_preset: '',
            available_scholarships: [],
            all_scholarships: []
        };
    },
    components: { PerInfo, EditableList },
    created() {
        this.setReadOnly();
        let that = this;
        if (this.$route.query.scholarship) {
            this.scholarship_id_preset = parseInt(
                this.$route.query.scholarship
            );
            this.onSelectScholarship(this.$route.query.scholarship);
            this.scholarship_id = this.scholarship_id_preset;
        }
        this.$http
            .post(
                this.readOnly
                    ? 'getAllScholarshipList'
                    : 'getAvailableScholarshipList',
                {
                    username: window.sessionStorage.username,
                    token: window.sessionStorage.token
                }
            )
            .then(response => {
                let res = JSON.parse(response.bodyText);
                if (res.status === 0) {
                    res = JSON.parse(res.data);
                    res.forEach(e => {
                        that.available_scholarships.push({
                            value: e.pk,
                            label: e.fields.scholarship_name
                        });
                    });
                } else {
                    swal({
                        title: '出错了',
                        text: res.message,
                        icon: 'error',
                        button: '确定'
                    }).then(val => {
                        if (res.status === -1) {
                            that.$router.push('/');
                        }
                    });
                }
            })
            .catch(response => {
                console.log(response);
            });
    },
    methods: {
        setFormData(form) {
            Object.keys(form.academic).forEach(key => {
                this.$refs[key][0].setContent(form.academic[key]);
            });
            Object.keys(form.work).forEach(key => {
                this.$refs[key][0].setContent(form.work[key]);
            });
            // remove tag
            if (
                form.other_academic.includes('PBokGE2nY2Qp8ukMBqqEFIFd5O3jc96V')
            ) {
                this.useSpecialAct = true;
                form.other_academic = form.other_academic.replace(
                    'PBokGE2nY2Qp8ukMBqqEFIFd5O3jc96V',
                    ''
                );
            } else this.useSpecialAct = false;
            // end remove tag
            this.other_academic_awards = form.other_academic;
        },
        withdrawApplyInfo() {
            this.$http
                .post('withdrawApplyInfo', {
                    username: window.sessionStorage.username,
                    token: window.sessionStorage.token,
                    data: { scholarship_id: this.scholarship_id }
                })
                .then(response => {
                    let res = JSON.parse(response.bodyText);
                    if (res.status === 0) {
                        swal({
                            title: '撤销申请成功',
                            text: res.message,
                            icon: 'success',
                            button: '确定'
                        }).then(val => {
                            this.$router.go(0);
                        });
                    } else {
                        swal({
                            title: '出错了',
                            text: res.message,
                            icon: 'error',
                            button: '确定'
                        }).then(val => {
                            if (res.status === -1) {
                                that.$router.push('/');
                            }
                        });
                    }
                })
                .catch(res => {
                    console.log(response);
                });
        },
        onSelectScholarship(val) {
            let that = this;
            this.$http
                .post('getScholarshipMaterial', {
                    username: window.sessionStorage.username,
                    token: window.sessionStorage.token,
                    data: String(val)
                })
                .then(response => {
                    let res = JSON.parse(response.bodyText);
                    if (res.status === 0) {
                        res = JSON.parse(res.data);
                        that.academic_criteria = res.academic_criteria;
                        that.academic_note = res.academic_note;
                        that.work_criteria = res.work_criteria;
                        that.work_note = res.work_note;
                        that.other_note = res.other_note;
                        that.other_academic_awards = '';
                        that.teacher_score = 0.0;
                        that.isApplied = false;
                        let post_data = { scholarship_id: val };
                        if (that.readOnly && that.stu_num != '') {
                            post_data['stu_num'] = that.stu_num;
                        }
                        that.$http
                            .post('obtainApplyInfo', {
                                username: window.sessionStorage.username,
                                token: window.sessionStorage.token,
                                data: post_data
                            })
                            .then(response => {
                                let res = JSON.parse(response.bodyText);
                                if (res.status === 0) {
                                    if (res.data && res.data.json != '') {
                                        that.isApplied =
                                            res.data.is_user_confirm;
                                        that.apply_id = res.data.id;
                                        res = JSON.parse(res.data.json);
                                        that.setFormData(res);
                                        if (that.is_teacher) {
                                            that.getTeacherScore();
                                        }
                                    } else that.isApplied = false;
                                } else {
                                    swal({
                                        title: '出错了',
                                        text: res.message,
                                        icon: 'error',
                                        button: '确定'
                                    }).then(val => {
                                        if (res.status === -1) {
                                            that.$router.push('/');
                                        }
                                    });
                                }
                            })
                            .catch(response => {
                                console.log(response);
                            });
                    } else {
                        swal({
                            title: '出错了',
                            text: res.message,
                            icon: 'error',
                            button: '确定'
                        }).then(val => {
                            if (res.status === -1) {
                                that.$router.push('/');
                            }
                        });
                    }
                })
                .catch(response => {
                    console.log(response);
                });
            if (!this.readOnly) {
                this.$http
                    .post('getAllScholarshipList',
                        {
                            username: window.sessionStorage.username,
                            token: window.sessionStorage.token
                        }
                    )
                    .then(response => {
                        let res = JSON.parse(response.bodyText);
                        if (res.status === 0) {
                            res = JSON.parse(res.data);
                            res.forEach(e => {
                                if (e.pk != this.scholarship_id) {
                                    that.all_scholarships.push({
                                        value: e.pk,
                                        label: e.fields.scholarship_name
                                    });
                                }
                            });
                        } else {
                            swal({
                                title: '出错了',
                                text: res.message,
                                icon: 'error',
                                button: '确定'
                            }).then(val => {
                                if (res.status === -1) {
                                    that.$router.push('/');
                                }
                            });
                        }
                    })
                    .catch(response => {
                        console.log(response);
                    });
            }
        },
        onSelectFormerScholarship(val) {
            let that = this;
            this.$http
                .post('getScholarshipMaterial', {
                    username: window.sessionStorage.username,
                    token: window.sessionStorage.token,
                    data: String(val)
                })
                .then(response => {
                    let res = JSON.parse(response.bodyText);
                    if (res.status === 0) {
                        res = JSON.parse(res.data);
                        let post_data = { scholarship_id: val };
                        if (that.readOnly && that.stu_num != '') {
                            post_data['stu_num'] = that.stu_num;
                        }
                        that.$http
                            .post('obtainApplyInfo', {
                                username: window.sessionStorage.username,
                                token: window.sessionStorage.token,
                                data: post_data
                            })
                            .then(response => {
                                let res = JSON.parse(response.bodyText);
                                if (res.status === 0) {
                                    if (res.data && res.data.json != '') {
                                        res = JSON.parse(res.data.json);
                                        that.setFormData(res);
                                    }
                                    this.formValidationRes = [];
                                } else {
                                    swal({
                                        title: '出错了',
                                        text: res.message,
                                        icon: 'error',
                                        button: '确定'
                                    }).then(val => {
                                        if (res.status === -1) {
                                            that.$router.push('/');
                                        }
                                    });
                                }
                            })
                            .catch(response => {
                                console.log(response);
                            });
                    } else {
                        swal({
                            title: '出错了',
                            text: res.message,
                            icon: 'error',
                            button: '确定'
                        }).then(val => {
                            if (res.status === -1) {
                                that.$router.push('/');
                            }
                        });
                    }
                })
                .catch(response => {
                    console.log(response);
                });
        },
        setReadOnly() {
            console.log(this.$route.path);
            let re_view_apply = /^\/.*?view_apply$/;
            let re_apply = /^\/.*?apply/;
            if (re_view_apply.test(this.$route.path)) {
                this.readOnly = true;
                // trigger update
            } else if (re_apply.test(this.$route.path)) {
                this.readOnly = false;
            }
        },
        getTeacherScore() {
            this.$http
                .post('getApplyInfoScore', {
                    username: window.sessionStorage.username,
                    token: window.sessionStorage.token,
                    data: { apply_id: this.apply_id }
                })
                .then(response => {
                    let res = JSON.parse(response.bodyText);
                    if (res.status === 0) {
                        this.teacher_score = parseFloat(String(res.data));
                    } else {
                        swal({
                            title: '出错了',
                            text: res.message,
                            icon: 'error',
                            button: '确定'
                        }).then(val => {
                            if (res.status === -1) {
                                that.$router.push('/');
                            }
                        });
                    }
                })
                .catch(res => {
                    console.log(res);
                });
        },
        onSubmitTeacherScore() {
            let that = this;
            this.$http
                .post('setApplyInfoScore', {
                    username: window.sessionStorage.username,
                    token: window.sessionStorage.token,
                    data: { apply_id: this.apply_id, score: this.teacher_score }
                })
                .then(response => {
                    let res = JSON.parse(response.bodyText);
                    if (res.status === 0) {
                        swal({
                            title: '打分成功',
                            icon: 'success',
                            button: '确定'
                        }).then(val => window.open('', '_self').close());
                    } else {
                        swal({
                            title: '出错了',
                            text: res.message,
                            icon: 'error',
                            button: '确定'
                        }).then(val => {
                            if (res.status === -1) {
                                that.$router.push('/');
                            }
                        });
                    }
                })
                .catch(res => {
                    console.log(res);
                });
        },
        onSave(user_confirm = false) {
            let that = this;
            let form_res = {
                academic: {},
                work: {},
                other_academic: null
            };
            that.academic_criteria.forEach(item => {
                form_res.academic[item.name] = that.$refs[
                    item.name
                ][0].getContent();
            });
            that.work_criteria.forEach(item => {
                form_res.work[item.name] = that.$refs[
                    item.name
                ][0].getContent();
            });
            form_res['other_academic'] = that.other_academic_awards;
            // remove tag
            if (that.useSpecialAct) {
                form_res['other_academic'] +=
                    '\nPBokGE2nY2Qp8ukMBqqEFIFd5O3jc96V';
            }
            // end remove tag
            that.$http
                .post('sendApplyInfo', {
                    username: window.sessionStorage.username,
                    token: window.sessionStorage.token,
                    data: {
                        scholarship_id: that.scholarship_id,
                        form: JSON.stringify(form_res),
                        confirm: user_confirm
                    }
                })
                .then(response => {
                    let res = JSON.parse(response.bodyText);
                    if (res.status === 0) {
                        swal({
                            title: user_confirm ? '申请成功' : '暂存成功',
                            icon: 'success',
                            button: '确定'
                        }).then(val => {
                            that.$router.go(0);
                        });
                    } else {
                        swal({
                            title: '出错了',
                            text: res.message,
                            icon: 'error',
                            button: '确定'
                        }).then(val => {
                            if (res.status === -1) {
                                that.$router.push('/');
                            }
                        });
                    }
                })
                .catch(response => {
                    console.log(response);
                });
        },
        onSubmit() {
            if (!this.$refs.perinfo.checkEmpty()) {
                swal({
                    title: '错误',
                    text: '补全所有个人信息后方能正式申请',
                    icon: 'error',
                    button: '确定'
                });
                return;
            }
            let that = this;
            this.formValidationRes = [];
            this.academic_criteria.forEach(item =>
                that.formValidationRes.push(that.$refs[item.name][0].validate())
            );
            this.work_criteria.forEach(item =>
                that.formValidationRes.push(that.$refs[item.name][0].validate())
            );
            Promise.all(that.formValidationRes)
                .then(function() {
                    that.onSave(true);
                })
                .catch(function() {
                    swal({
                        title: '错误',
                        icon: 'error',
                        text: '请检查所有表单项是否完整填写',
                        button: '确定'
                    });
                });
        }
    },
    watch: {
        $route: function() {
            this.setReadOnly();
        }
    }
};
</script>
