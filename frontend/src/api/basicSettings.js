/* eslint-disable */
/* stub method for basic settings */
export const footer = "Developer <a href='https://github.com/zx1239856' target='_blank'>zx1239856</a>, <a href='https://github.com/dkax' target='_blank'>dkax</a> \
&copy; 2019, All rights reserved."

const getGenderList = function () {
    return [{
        label: '男',
        value: 'male'
    }, {
        label: '女',
        value: 'female'
    }]
}

const getDepartmentList = function () {
    return [{
        value: "media",
        label: "媒体所"
    }, {
        value: "cad",
        label: "CAD所"
    }, {
        value: "hi_perf",
        label: "高性能所"
    }, {
        value: "ai",
        label: "人智所"
    }, {
        value: "software",
        label: "软件所"
    }, {
        value: "network",
        label: "网络所"
    }, {
        value: "gix",
        label: "GIX所"
    }, {
        value: "cs_ma",
        label: "计研"
    }]
}

const getSpecificStudentTypeList = function () {
    return [{
        value: "master",
        label: "硕士"
    }, {
        value: "doctor_straight",
        label: "直博"
    }, {
        value: "master_doctor",
        label: "硕博连读"
    }, {
        value: "doctor_normal",
        label: "普博"
    }]
}

const getRoughStudentTypeList = function () {
    return [{
        value: "master",
        label: "硕士"
    }, {
        value: "doctor",
        label: "博士"
    }]
}

const getStudentStatusList = function () {
    return [{
        value: "cst",
        label: "计算机系"
    }, {
        value: "shenzhen",
        label: "深圳研究院"
    }, {
        value: "other",
        label: "其他"
    }]
}

const getPoliticalStatusList = function () {
    return [{
        value: "party",
        label: "中共党员"
    }, {
        value: "pre_party",
        label: "预备党员"
    }, {
        value: "league",
        label: "共青团员"
    }, {
        value: "general",
        label: "群众"
    }, {
        value: "other",
        label: "其他"
    }]
}

const getGradeList = function () {
    let list = [];
    for (let i = 1; i <= 6; ++i) {
        list.push({ value: String(i), label: String(i) });
    }
    list.push({ value: "above", label: "以上" });
    return list;
}

export {
    getDepartmentList, getGenderList, getSpecificStudentTypeList, getRoughStudentTypeList,
    getStudentStatusList, getPoliticalStatusList, getGradeList, getApplyMainSettings
};