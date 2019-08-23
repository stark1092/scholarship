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

const getApplyMainSettings = function () {
    return {
        academic_criteria: [
            {
                name: "conf_paper",
                content: {
                    title: "会议论文",
                    note:
                        "(1)申请人为第一作者（第一发明人）或者导师为第一作者（第一发明人）时申请人为第二作者（第二发明人）。注明：导师为学籍上导师，或者为导师指定给该申请人的副导师，导师必须在作者名单内。<br>\
            (2)奖学金申请表中的论文（专利）必须是在校期间所发表的论文或已经授权的专利，该时间段要求以“论文所在期刊的出版日期”或“论文所投会议的召开日期”或“专利授权日期”为准。<br>\
            (3)论文的第一单位署名不是清华大学的，不得填入奖学金的申请表。<br>\
            (4)只有录用函但还未正式出版或未正式召开会议的论文不得被填入申请表，但为了让即将毕业的研究生有机会展示自己的工作成果，即将毕业的研究生在本人做出这是自己最后一次参加奖学金评定的申明后，可以将只收到录用函的论文填入申请表。但要在奖学金申请材料表中明确标出“最后一年申请”（含义：若本次评得秋奖奖项，今后不得再参选任何含奖金的奖项）。<br>\
            (5)发表在同一刊物上的同一篇论文不得连续两次重复评奖，即不能按照录用时期和正式刊发的两个时间重复参评。",
                    templateData: {
                        seq: 0,
                        author: "",
                        isFirstAuthor: "0",
                        ccfRank: "A",
                        journal: "",
                        paper: "",
                        date: "",
                        numPages: "",
                        category: "full",
                        isLastYear: "0"
                    },
                    tableData: [],
                    tableColumn: [
                        {
                            type: "seq",
                            label: "#",
                            name: "seq",
                            colWidth: "50%"
                        },
                        {
                            type: "input",
                            label: "作者",
                            name: "author"
                        },
                        {
                            type: "selection",
                            data: [
                                {
                                    label: "否",
                                    value: "0"
                                },
                                {
                                    label: "是",
                                    value: "1"
                                }
                            ],
                            label: "是否一作",
                            name: "isFirstAuthor",
                            colWidth: "130%",
                            note: "本人一作，或导师一作本人二作"
                        },
                        {
                            type: "selection",
                            data: [
                                {
                                    label: "A",
                                    value: "A"
                                },
                                {
                                    label: "B",
                                    value: "B"
                                },
                                {
                                    label: "C",
                                    value: "C"
                                },
                                {
                                    label: "O",
                                    value: "O"
                                },
                                {
                                    label: "其他",
                                    value: "other"
                                }
                            ],
                            label: "CCF排名",
                            name: "ccfRank",
                            colWidth: "100%"
                        },
                        {
                            type: "input",
                            label: "会议全称",
                            name: "conf",
                            colWidth: "200%"
                        },
                        {
                            type: "input",
                            label: "论文全称",
                            name: "paper",
                            colWidth: "200%"
                        },
                        {
                            type: "date-picker",
                            label: "开会时间",
                            name: "date",
                            colWidth: "250%"
                        },
                        {
                            type: "input",
                            label: "页数",
                            name: "numPages",
                            colWidth: "80%"
                        },
                        {
                            type: "selection",
                            data: [
                                {
                                    label: "Full paper",
                                    value: "full"
                                },
                                {
                                    label: "Short paper",
                                    value: "short"
                                },
                                {
                                    label: "Poster",
                                    value: "poster"
                                },
                                {
                                    label: "Workshop",
                                    value: "workshop"
                                },
                                {
                                    label: "Demo",
                                    value: "demo"
                                }
                            ],
                            label: "论文类型",
                            name: "category"
                        },
                        {
                            type: "selection",
                            data: [
                                {
                                    label: "否",
                                    value: "0"
                                },
                                {
                                    label: "是",
                                    value: "1"
                                }
                            ],
                            label: "最后一年申请",
                            name: "isLastYear"
                        }
                    ]
                }
            },
            {
                name: "journal_paper",
                content: {
                    title: "期刊论文",
                    note:
                        "(1)申请人为第一作者（第一发明人）或者导师为第一作者（第一发明人）时申请人为第二作者（第二发明人）。注明：导师为学籍上导师，或者为导师指定给该申请人的副导师，导师必须在作者名单内。<br>\
            (2)奖学金申请表中的论文（专利）必须是在校期间所发表的论文或已经授权的专利，该时间段要求以“论文所在期刊的出版日期”或“论文所投会议的召开日期”或“专利授权日期”为准。<br>\
            (3)论文的第一单位署名不是清华大学的，不得填入奖学金的申请表。<br>\
            (4)只有录用函但还未正式出版或未正式召开会议的论文不得被填入申请表，但为了让即将毕业的研究生有机会展示自己的工作成果，即将毕业的研究生在本人做出这是自己最后一次参加奖学金评定的申明后，可以将只收到录用函的论文填入申请表。但要在奖学金申请材料表中明确标出“最后一年申请”（含义：若本次评得秋奖奖项，今后不得再参选任何含奖金的奖项）。<br>\
            (5)发表在同一刊物上的同一篇论文不得连续两次重复评奖，即不能按照录用时期和正式刊发的两个时间重复参评。",
                    templateData: {
                        seq: 0,
                        author: "",
                        isFirstAuthor: "0",
                        ccfRank: "A",
                        journal: "",
                        paper: "",
                        date: "",
                        pagePos: "",
                        numPages: "",
                        category: "full",
                        isLastYear: "0"
                    },
                    tableData: [],
                    tableColumn: [
                        {
                            type: "seq",
                            label: "#",
                            name: "seq",
                            colWidth: "50%"
                        },
                        {
                            type: "input",
                            label: "作者",
                            name: "author"
                        },
                        {
                            type: "selection",
                            data: [
                                {
                                    label: "否",
                                    value: "0"
                                },
                                {
                                    label: "是",
                                    value: "1"
                                }
                            ],
                            label: "是否一作",
                            name: "isFirstAuthor",
                            colWidth: "130%",
                            note: "本人一作，或导师一作本人二作"
                        },
                        {
                            type: "selection",
                            data: [
                                {
                                    label: "A",
                                    value: "A"
                                },
                                {
                                    label: "B",
                                    value: "B"
                                },
                                {
                                    label: "C",
                                    value: "C"
                                },
                                {
                                    label: "O",
                                    value: "O"
                                },
                                {
                                    label: "其他",
                                    value: "other"
                                }
                            ],
                            label: "CCF排名",
                            name: "ccfRank",
                            colWidth: "100%"
                        },
                        {
                            type: "input",
                            label: "期刊全称",
                            name: "journal",
                            colWidth: "200%"
                        },
                        {
                            type: "input",
                            label: "论文全称",
                            name: "paper",
                            colWidth: "200%"
                        },
                        {
                            type: "date-picker",
                            label: "出版日期",
                            name: "date",
                            colWidth: "250%"
                        },
                        {
                            type: "input",
                            label: "页码",
                            name: "pagePos",
                            colWidth: "80%"
                        },
                        {
                            type: "input",
                            label: "页数",
                            name: "numPages",
                            colWidth: "80%"
                        },
                        {
                            type: "selection",
                            data: [
                                {
                                    label: "Full paper",
                                    value: "full"
                                },
                                {
                                    label: "Short paper",
                                    value: "short"
                                },
                                {
                                    label: "Poster",
                                    value: "poster"
                                },
                                {
                                    label: "Workshop",
                                    value: "workshop"
                                },
                                {
                                    label: "Demo",
                                    value: "demo"
                                }
                            ],
                            label: "论文类型",
                            name: "category"
                        },
                        {
                            type: "selection",
                            data: [
                                {
                                    label: "否",
                                    value: "0"
                                },
                                {
                                    label: "是",
                                    value: "1"
                                }
                            ],
                            label: "最后一年申请",
                            name: "isLastYear"
                        }
                    ]
                }
            },
            {
                name: "patent",
                content: {
                    title: "专利",
                    note:
                        "(1)申请人为第一作者（第一发明人）或者导师为第一作者（第一发明人）时申请人为第二作者（第二发明人）。注明：导师为学籍上导师，或者为导师指定给该申请人的副导师，导师必须在作者名单内。<br>\
            (2)奖学金申请表中的论文（专利）必须是在校期间所发表的论文或已经授权的专利，该时间段要求以“论文所在期刊的出版日期”或“论文所投会议的召开日期”或“专利授权日期”为准。<br>\
            (3)论文的第一单位署名不是清华大学的，不得填入奖学金的申请表。<br>\
            (4)只有录用函但还未正式出版或未正式召开会议的论文不得被填入申请表，但为了让即将毕业的研究生有机会展示自己的工作成果，即将毕业的研究生在本人做出这是自己最后一次参加奖学金评定的申明后，可以将只收到录用函的论文填入申请表。但要在奖学金申请材料表中明确标出“最后一年申请”（含义：若本次评得秋奖奖项，今后不得再参选任何含奖金的奖项）。<br>\
            (5)发表在同一刊物上的同一篇论文不得连续两次重复评奖，即不能按照录用时期和正式刊发的两个时间重复参评。",
                    templateData: {
                        seq: 0,
                        author: "",
                        isFirstAuthor: "0",
                        name: "",
                        number: "",
                        date: "",
                        isLastYear: "0"
                    },
                    tableData: [],
                    tableColumn: [
                        {
                            type: "seq",
                            label: "#",
                            name: "seq",
                            colWidth: "50%"
                        },
                        {
                            type: "input",
                            label: "作者",
                            name: "author"
                        },
                        {
                            type: "selection",
                            data: [
                                {
                                    label: "否",
                                    value: "0"
                                },
                                {
                                    label: "是",
                                    value: "1"
                                }
                            ],
                            label: "是否一作",
                            name: "isFirstAuthor",
                            colWidth: "130%",
                            note: "本人一作，或导师一作本人二作"
                        },
                        {
                            type: "input",
                            label: "专利名称",
                            name: "name",
                            colWidth: "300%"
                        },
                        {
                            type: "input",
                            label: "公开（公告）号",
                            name: "number",
                            colWidth: "300%"
                        },
                        {
                            type: "date-picker",
                            label: "公开（公告）日期",
                            name: "date",
                            colWidth: "250%"
                        },
                        {
                            type: "selection",
                            data: [
                                {
                                    label: "否",
                                    value: "0"
                                },
                                {
                                    label: "是",
                                    value: "1"
                                }
                            ],
                            label: "最后一年申请",
                            name: "isLastYear"
                        }
                    ]
                }
            },
            {
                name: "project",
                content: {
                    title: "项目",
                    templateData: {
                        seq: 0,
                        author: "",
                        name: "",
                        date: "",
                        type: "national",
                        isLastYear: "0"
                    },
                    tableData: [],
                    tableColumn: [
                        {
                            type: "seq",
                            label: "#",
                            name: "seq",
                            colWidth: "50%"
                        },
                        {
                            type: "input",
                            label: "作者",
                            name: "author"
                        },
                        {
                            type: "input",
                            label: "项目名称",
                            name: "name",
                            colWidth: "300%"
                        },
                        {
                            type: "date-picker",
                            label: "获奖时间",
                            name: "date",
                            colWidth: "250%"
                        },
                        {
                            type: "selection",
                            data: [
                                {
                                    label: "国家级奖励",
                                    value: "national"
                                },
                                {
                                    label: "省级部一等奖项目",
                                    value: "provincial_1"
                                },
                                {
                                    label: "省级部二等奖项目",
                                    value: "provincial_2"
                                }
                            ],
                            label: "获奖类型",
                            name: "type",
                            colWidth: "300%"
                        },
                        {
                            type: "selection",
                            data: [
                                {
                                    label: "否",
                                    value: "0"
                                },
                                {
                                    label: "是",
                                    value: "1"
                                }
                            ],
                            label: "最后一年申请",
                            name: "isLastYear"
                        }
                    ]
                }
            },
            {
                name: "intl_standard",
                content: {
                    title: "国际标准",
                    templateData: {
                        seq: 0,
                        author: "",
                        name: "",
                        date: "",
                        isLastYear: "0"
                    },
                    tableData: [],
                    tableColumn: [
                        {
                            type: "seq",
                            label: "#",
                            name: "seq",
                            colWidth: "50%"
                        },
                        {
                            type: "input",
                            label: "作者",
                            name: "author",
                            colWidth: "400%"
                        },
                        {
                            type: "input",
                            label: "标准名称",
                            name: "name",
                            colWidth: "400%"
                        },
                        {
                            type: "date-picker",
                            label: "标准发布时间",
                            name: "date",
                            colWidth: "250%"
                        },
                        {
                            type: "selection",
                            data: [
                                {
                                    label: "否",
                                    value: "0"
                                },
                                {
                                    label: "是",
                                    value: "1"
                                }
                            ],
                            label: "最后一年申请",
                            name: "isLastYear",
                            colWidth: "300%"
                        }
                    ]
                }
            },
            {
                name: "conf_award",
                content: {
                    title: "会议奖励",
                    templateData: {
                        seq: 0,
                        author: "",
                        confName: "",
                        awardName: "",
                        ccfCategory: "",
                        date: "",
                        isLastYear: "0"
                    },
                    tableData: [],
                    tableColumn: [
                        {
                            type: "seq",
                            label: "#",
                            name: "seq",
                            colWidth: "50%"
                        },
                        {
                            type: "input",
                            label: "作者",
                            name: "author",
                            colWidth: "200%"
                        },
                        {
                            type: "input",
                            label: "会议名称",
                            name: "confName",
                            colWidth: "200%"
                        },
                        {
                            type: "input",
                            label: "奖励名称",
                            name: "awardName",
                            colWidth: "200%"
                        },
                        {
                            type: "input",
                            label: "CCF分类",
                            name: "ccfCategory",
                            colWidth: "200%"
                        },
                        {
                            type: "date-picker",
                            label: "获取日期",
                            name: "date",
                            colWidth: "300%"
                        },
                        {
                            type: "selection",
                            data: [
                                {
                                    label: "否",
                                    value: "0"
                                },
                                {
                                    label: "是",
                                    value: "1"
                                }
                            ],
                            label: "最后一年申请",
                            name: "isLastYear"
                        }
                    ]
                }
            }
        ],
        academic_note: "",
        work_criteria: [
            {
                name: "post",
                content: {
                    title: "担任岗位",
                    templateData: {
                        seq: 0,
                        name: "",
                        class: "A",
                        startDate: "",
                        endDate: "",
                        monthFirst: 0,
                        monthSecond: 0
                    },
                    tableData: [],
                    tableColumn: [
                        {
                            type: "seq",
                            label: "#",
                            name: "seq",
                            colWidth: "50%"
                        },
                        {
                            type: "input",
                            label: "岗位名称",
                            name: "name"
                        },
                        {
                            type: "selection",
                            note:
                                "A.学生思想政治辅导员，研究生德育工作助理；系研团委总支书记、系研会主席、信息中心主任；校级研团研会部长及以上职务。<br>\
                    B.系研团委副书记、系研会副主席、信息中心副主任；校级研团研会副部长。<br>\
                    C.各班班长、党支书、团支书；系研团委部长、系研会部长、信息中心部长。<br>\
                    D.班级党支委成员（组织委员、宣传委员）、班委成员、团支委成员、系研会学生骨干（由系研究生会确认）、系研团总支学生骨干（由系研团总支确认）、信息中心学生骨干（由信息中心确认）、系体育俱乐部主席、系体育代表队教练、校各学生社团协会会长。",
                            data: [
                                {
                                    label: "A",
                                    value: "A"
                                },
                                {
                                    label: "B",
                                    value: "B"
                                },
                                {
                                    label: "C",
                                    value: "C"
                                },
                                {
                                    label: "D",
                                    value: "D"
                                }
                            ],
                            label: "岗位等级",
                            name: "class"
                        },
                        {
                            type: "date-picker",
                            label: "开始时间",
                            name: "startDate",
                            colWidth: "250%"
                        },
                        {
                            type: "date-picker",
                            label: "结束时间",
                            name: "endDate",
                            colWidth: "250%"
                        },
                        {
                            type: "input-number",
                            label: "第一学期月数(填写整数)",
                            name: "monthFirst",
                            min: 0,
                            colWidth: "200%"
                        },
                        {
                            type: "input-number",
                            label: "第二学期月数(填写整数)",
                            name: "monthSecond",
                            min: 0,
                            colWidth: "200%"
                        }
                    ]
                }
            },
            {
                name: "accu_pro",
                content: {
                    title: "累积项目",
                    templateData: {
                        seq: 0,
                        class: "A",
                        content: "",
                        date: ""
                    },
                    tableData: [],
                    tableColumn: [
                        {
                            type: "seq",
                            label: "#",
                            name: "seq",
                            colWidth: "50%"
                        },
                        {
                            type: "selection",
                            note:
                                "A.一二九辅导员，校级优秀德育助理（5分）<br>\
                      B.校级优秀研究生共产党员，校级优秀共青团员，校级优秀党支部、研究生党支部支书，校级优秀班集体班长；（4分）<br>\
                      C.清华大学优秀学生（研究生）干部（4分）<br>\
                      D.校级各学生组织评选的优秀学生干部（3分）<br>\
                      E.校级党建研究基金、特色组织生活基金和集体建设基金优秀项目的党支部支书(2分)<br>\
                      F.博士生必修环节暑期实践一、二、三等奖；（3分、2分、1分）<br>\
                      G.系级各学生组织评选的优秀学生干部；（1分）<br>\
                      H.参加一二九大合唱；（1分）<br>\
                      I.非博士生必修环节社会实践支队长；（2分）<br>\
                      J.非博士生必修环节社会实践队员；（1分）<br>\
                      K.非博士生必修环节社会实践校级金/银/铜奖支队成员（1.5分、1分、0.5分）<br>\
                      L.通过身体素质测试，或申请免测通过的；（1分）",
                            data: [
                                {
                                    label: "A",
                                    value: "A"
                                },
                                {
                                    label: "B",
                                    value: "B"
                                },
                                {
                                    label: "C",
                                    value: "C"
                                },
                                {
                                    label: "D",
                                    value: "D"
                                },
                                {
                                    label: "E",
                                    value: "E"
                                },
                                {
                                    label: "F1",
                                    value: "F1"
                                },
                                {
                                    label: "F2",
                                    value: "F2"
                                },
                                {
                                    label: "F3",
                                    value: "F3"
                                },
                                {
                                    label: "G",
                                    value: "G"
                                },
                                {
                                    label: "H",
                                    value: "H"
                                },
                                {
                                    label: "I",
                                    value: "I"
                                },
                                {
                                    label: "J",
                                    value: "J"
                                },
                                {
                                    label: "K1",
                                    value: "K1"
                                },
                                {
                                    label: "K2",
                                    value: "K2"
                                },
                                {
                                    label: "K3",
                                    value: "K3"
                                },
                                {
                                    label: "L",
                                    value: "L"
                                }
                            ],
                            label: "加分项",
                            name: "class"
                        },
                        {
                            type: "input",
                            label: "加分内容",
                            name: "content",
                            colWidth: "800%"
                        },
                        {
                            type: "date-picker",
                            label: "时间",
                            name: "date",
                            colWidth: "250%"
                        }
                    ]
                }
            }
        ],
        work_note: "在校期间担任的社工岗位",
        other_note: ""
    }
}

export {
    getDepartmentList, getGenderList, getSpecificStudentTypeList, getRoughStudentTypeList,
    getStudentStatusList, getPoliticalStatusList, getGradeList, getApplyMainSettings
};