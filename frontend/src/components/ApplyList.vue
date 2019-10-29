<template>
    <div>
        <el-form :inline="true" :model="filter.conditions" label-width="50px" ref="filter_form">
            <el-form-item
                :rules="[{ required: true, message: '字段不能为空', trigger: ['change','blur'] }]"
                label="筛选"
                prop="scholarship_name"
            >
                <el-select placeholder="请选择奖学金" v-model="filter.conditions.scholarship_name">
                    <div :key="item.value" v-for="item in filter.scholarship_names">
                        <el-option :label="item.label" :value="item.value"></el-option>
                    </div>
                </el-select>
            </el-form-item>
            <el-form-item
                :rules="[{ required: true, message: '字段不能为空', trigger: ['change','blur'] }]"
                prop="student_type"
            >
                <el-select placeholder style="width: 5vw; min-width: 80px;" v-model="filter.conditions.student_type">
                    <el-option
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                        v-for="item in filter.student_types"
                    ></el-option>
                </el-select>
            </el-form-item>
            <el-form-item>
                <el-select
                    clearable
                    placeholder
                    prop="department"
                    style="width: 8vw; min-width: 100px;"
                    v-model="filter.conditions.department"
                >
                    <el-option
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                        v-for="item in filter.departments"
                    ></el-option>
                </el-select>
            </el-form-item>
            <el-form-item
                :rules="[{ required: true, message: '字段不能为空', trigger: ['change','blur'] }]"
                label="排序"
                prop="ordering"
            >
                <el-select placeholder style="width: 7vw; min-width: 130px;" v-model="filter.conditions.ordering">
                    <div :key="item.value" v-for="item in filter.ordering_list">
                        <el-option :label="item.label" :value="item.value" v-if="item.show"></el-option>
                    </div>
                </el-select>
            </el-form-item>
            <el-form-item>
                <el-button @click="submitFilter(1);currPage=1;" type="primary">确定</el-button>
            </el-form-item>
            <el-form-item>
                <el-button @click="exportList" type="success" v-if="isAdmin">导出为EXCEL</el-button>
            </el-form-item>
        </el-form>
        <el-row justify="center" type="flex">
            <el-col :span="24">
                <List :linkCb="linkCb" :model="model"></List>
            </el-col>
        </el-row>
        <el-row justify="center" style="margin-top: 1vh" type="flex">
            <el-col :span="24">
                <el-pagination
                    :current-page.sync="currPage"
                    :hide-on-single-page="true"
                    :page-count="numPages"
                    @current-change="handlePageChange"
                    background
                    layout="prev, pager, next"
                ></el-pagination>
            </el-col>
        </el-row>
    </div>
</template>

<script>
/* eslint-disable */
import List from './UneditableList';
import {
    getRoughStudentTypeList,
    getDepartmentList,
    getDepartmentListTeacher
} from '../api/basicSettings';

const numElemPerPage = 15;

var main_ptr = null;

export default {
    computed: {
        tableColumn: function() {
            if (window.sessionStorage.user_type === '1') {
                return [
                    {
                        type: 'seq',
                        label: '#',
                        name: 'seq',
                        colWidth: '50%'
                    },
                    {
                        type: 'text',
                        label: '学号',
                        name: 'student_num'
                    },
                    {
                        type: 'text',
                        label: '姓名',
                        name: 'name'
                    },
                    {
                        type: 'text',
                        label: '所',
                        name: 'department'
                    },
                    {
                        type: 'text',
                        label: '导师',
                        name: 'instructor'
                    },
                    {
                        type: 'text',
                        label: 'A类论文',
                        name: 'a_paper'
                    },
                    {
                        type: 'text',
                        label: 'B类论文',
                        name: 'b_paper'
                    },
                    {
                        type: 'text',
                        label: 'C类论文',
                        name: 'c_paper'
                    },
                    {
                        type: 'text',
                        label: 'O类论文',
                        name: 'o_paper'
                    },
                    {
                        type: 'text',
                        label: '专利',
                        name: 'patent'
                    },
                    {
                        type: 'text',
                        label: '学术得分',
                        name: 'academic_score'
                    },
                    {
                        type: 'text',
                        label: '社工得分',
                        name: 'work_score'
                    },
                    {
                        type: 'text',
                        label: '基础得分',
                        name: 'tot_score',
                        note: '基础得分=学术x0.7+(社工得分+专项得分)x0.3'
                    },
                    {
                        type: 'text',
                        label: '教师评分',
                        name: 'teacher_score'
                    },
                    {
                        type: 'link',
                        label: '查看详情',
                        name: 'link'
                    }
                ];
            } else if (window.sessionStorage.user_type === '2') {
                return [
                    {
                        type: 'seq',
                        label: '#',
                        name: 'seq',
                        colWidth: '50%'
                    },
                    {
                        type: 'text',
                        label: '学号',
                        name: 'student_num'
                    },
                    {
                        type: 'text',
                        label: '姓名',
                        name: 'name'
                    },
                    {
                        type: 'text',
                        label: 'A类论文',
                        name: 'a_paper'
                    },
                    {
                        type: 'text',
                        label: 'B类论文',
                        name: 'b_paper'
                    },
                    {
                        type: 'text',
                        label: 'C类论文',
                        name: 'c_paper'
                    },
                    {
                        type: 'text',
                        label: 'O类论文',
                        name: 'o_paper'
                    },
                    {
                        type: 'text',
                        label: '专利',
                        name: 'patent'
                    },
                    {
                        type: 'text',
                        label: '学术得分',
                        name: 'academic_score'
                    },
                    {
                        type: 'text',
                        label: '社工得分',
                        name: 'work_score'
                    },
                    {
                        type: 'text',
                        label: '教师评分',
                        name: 'teacher_score'
                    },
                    {
                        type: 'text',
                        label: '总分',
                        name: 'tot_score'
                    },
                    {
                        type: 'text',
                        label: '被举报数',
                        name: 'num_report',
                        note:
                            '发现不实信息请向thucs_scholarship@163.com举报，我们将严格保密举报者的信息'
                    },
                    {
                        type: 'link',
                        label: '查看详情',
                        name: 'link'
                    }
                ];
            } else
                return [
                    {
                        type: 'seq',
                        label: '#',
                        name: 'seq',
                        colWidth: '50%'
                    },
                    {
                        type: 'text',
                        label: '学号',
                        name: 'student_num'
                    },
                    {
                        type: 'text',
                        label: '姓名',
                        name: 'name'
                    },
                    {
                        type: 'text',
                        label: 'A类论文',
                        name: 'a_paper'
                    },
                    {
                        type: 'text',
                        label: 'B类论文',
                        name: 'b_paper'
                    },
                    {
                        type: 'text',
                        label: 'C类论文',
                        name: 'c_paper'
                    },
                    {
                        type: 'text',
                        label: 'O类论文',
                        name: 'o_paper'
                    },
                    {
                        type: 'text',
                        label: '专利',
                        name: 'patent'
                    },
                    {
                        type: 'text',
                        label: '学术得分',
                        name: 'academic_score'
                    },
                    {
                        type: 'text',
                        label: '社工得分',
                        name: 'work_score'
                    },
                    {
                        type: 'text',
                        label: '总分',
                        name: 'tot_score'
                    },
                    {
                        type: 'text',
                        label: '被举报数',
                        name: 'num_report',
                        note:
                            '发现不实信息请向thucs_scholarship@163.com举报，我们将严格保密举报者的信息'
                    },
                    {
                        type: 'link',
                        label: '查看详情',
                        name: 'link'
                    }
                ];
        }
    },
    data() {
        let isTeacher = window.sessionStorage.user_type === '1';
        return {
            isAdmin: window.sessionStorage.user_type === '2',
            isTeacher: window.sessionStorage.user_type === '1',
            numPages: 0,
            currPage: 1,
            model: {
                tableData: [],
                tableColumn: null
            },
            linkCb: function(link) {
                let route = this.$router.resolve({
                    path: '/view_apply',
                    query: {
                        stu_num: link,
                        scholarship: main_ptr.filter.conditions.scholarship_name
                    }
                });
                window.open(route.href, '_blank');
            },
            filter: {
                conditions: {
                    scholarship_name: '',
                    student_type: !isTeacher ? '' : 'doctor',
                    department: '',
                    ordering: !isTeacher ? '' : 'tot_score'
                },
                scholarship_names: [],
                student_types: getRoughStudentTypeList(),
                departments: isTeacher ? getDepartmentListTeacher() : getDepartmentList(),
                ordering_list: [
                    {
                        value: 'tot_score',
                        label: (!isTeacher) ? '总分' : '基础得分',
                        show: true
                    },
                    {
                        value: 'teacher_score',
                        label: '教师评分',
                        show: isTeacher
                    },
                    {
                        value: 'academic_score',
                        label: '学术得分',
                        show: true
                    },
                    {
                        value: 'work_score',
                        label: '社工得分',
                        show: true
                    }
                ]
            }
        };
    },
    components: { List },
    created() {
        main_ptr = this;
        this.loadScholarshipList();
        this.model.tableColumn = this.tableColumn;
    },
    methods: {
        loadScholarshipList(cb = null) {
            let that = this;
            this.$http
                .post('getAllScholarshipList', {
                    username: window.sessionStorage.username,
                    token: window.sessionStorage.token
                })
                .then(response => {
                    let res = JSON.parse(response.bodyText);
                    if (res.status === 0) {
                        let data = JSON.parse(res.data);
                        data.forEach(e => {
                            that.filter.scholarship_names.push({
                                label: e.fields.scholarship_name,
                                value: e.pk
                            });
                        });
                        if (cb) cb();
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
                .catch(err => console.log(err));
        },
        handlePageChange(val) {
            this.submitFilter(val);
        },
        fakeAddDataHelper() {
            let template = {
                seq: 0,
                student_num: '2017011555',
                name: '王小明',
                a_paper: '1',
                b_paper: '1',
                c_paper: '1',
                o_paper: '0',
                patent: '1',
                academic_score: '2',
                work_score: '3',
                teacher_score: '0',
                tot_score: '5',
                num_report: '0',
                link: {
                    link: '2017011555',
                    label: '点击查看'
                }
            };
        },
        submitFilter(page = 1) {
            let that = this;
            let api_name_map = {
                '0': 'filterAndSort',
                '1': 'filterAndSortTeacher',
                '2': 'filterAndSortAdmin'
            };
            this.$refs['filter_form'].validate(valid => {
                if (valid) {
                    let data = {};
                    let filter_url =
                        api_name_map[window.sessionStorage.user_type];
                    Object.assign(data, this.filter.conditions);
                    data.page = page;
                    this.$http
                        .post(filter_url, {
                            token: window.sessionStorage.token,
                            username: window.sessionStorage.username,
                            data: data
                        })
                        .then(response => {
                            let res = JSON.parse(response.bodyText);
                            if (res.status === 0) {
                                that.numPages = res.data.page_cnt;
                                console.log(res.data);
                                that.model.tableData = res.data.curr_entries;
                                that.model.tableData.forEach(e => {
                                    e.link = {
                                        link: e.student_num,
                                        label: '点击查看'
                                    };
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
                        .catch(function(response) {
                            console.log(response);
                        });
                } else {
                    swal({
                        title: '错误',
                        text: '请选择完整筛选条件',
                        icon: 'error',
                        button: '确定'
                    });
                }
            });
        },
        exportList() {
            // submit filter to backend, and request generating excel file
            let that = this;
            this.$refs['filter_form'].validate(valid => {
                if (valid) {
                    let data = {};
                    Object.assign(data, this.filter.conditions);
                    this.$http
                        .post(
                            'exportExcel',
                            {
                                token: window.sessionStorage.token,
                                username: window.sessionStorage.username,
                                data: data
                            },
                            { responseType: 'blob' }
                        )
                        .then(response => {
                            if (response.body.status !== undefined) {
                                if (response.body.status !== 0) {
                                    swal({
                                        title: '出错了',
                                        text: response.body.message,
                                        icon: 'error',
                                        button: '确定'
                                    }).then(val => {
                                        if (response.body.status === -1) {
                                            that.$router.push('/');
                                        }
                                    });
                                    return;
                                }
                            }
                            const link = document.createElement('a');
                            let blob = new Blob([response.data], {
                                type: 'application/vnd.ms-excel'
                            });
                            link.style.display = 'none';
                            link.href = URL.createObjectURL(blob);
                            link.setAttribute('download', '申请列表.xls');
                            document.body.appendChild(link);
                            link.click();
                            document.body.removeChild(link);
                        })
                        .catch(function(response) {
                            console.log(response);
                        });
                } else {
                    swal({
                        title: '错误',
                        text: '请选择完整筛选条件',
                        icon: 'error',
                        button: '确定'
                    });
                }
            });
        }
    }
};
</script>

