(() =>
{

const AJAX_HOST = 'http://127.0.0.1/api'; // '/api';
const AJAX_HISTORY_HOST = 'http://127.0.0.1/static/predict/predict'; // '/static/predict/predict';


mdui.$.ajaxSetup({
    global: true
});

mdui.$(document).ajaxStart(() =>
{
    mdui.$.doms.AJAXProgress.removeClass('mdui-hidden');
    mdui.$.lockScreen();
    mdui.$.showOverlay();
});

mdui.$(document).ajaxComplete(() =>
{
    mdui.$.doms.AJAXProgress.addClass('mdui-hidden');
    mdui.$.unlockScreen();
    mdui.$.hideOverlay();
});



mdui.$.extend({
    get(url) {
        return new Promise((res, rej) =>
        {
            mdui.$.ajax({
                method: 'GET',
                url: AJAX_HOST + url,
                dataType: 'json',
                xhrFields: {
                    withCredentials: true
                },
                success(data) {
                    res(data);
                },
                error(e) {
                    errorHandler(e);
                    rej(e);
                }
            })
        });
    }
});

mdui.$.extend({
    api: {
        getAnnounce()
        {
            mdui.$.get('/announce')
                .then(data =>
                {
                    mdui.$.doms.announceContent.html(data.msg);
                });
        },
        search(keyword)
        {
            const keywordType = mdui.$.doms.searchKeywordType.serializeArray().filter(e => e.name === 'search-keyword-type')[0].value;

            if (keyword == '')
            {
                mdui.alert('请输入关键词！', '前方高能');
                return;
            }

            if (keywordType === 'school') mdui.$.api.searchSchool(keyword);
            else if (keywordType === 'subject') mdui.$.api.searchSubject(keyword);
        },
        searchSchool(keyword)
        {
            mdui.$.get('/search/' + encodeURIComponent(keyword))
                .then(data =>
                {
                    if (data.length <= 0)
                    {
                        mdui.alert('没有更多啦', '前方高能');
                        return;
                    }

                    mdui.$.doms.searchResultContainer.html(
                        '<div class="mdui-text-color-theme-disabled mdui-text-center mdui-m-t-1 mdui-m-b-1 mdui-hidden-lg-up">提示：可左右滑动查看更多信息</div>' +
                        mdui.$.createTable(
                            parseData(data),
                            [
                                'ID',
                                '名称',
                                '办学体制',
                                '办学类型',
                                '985 / 211',
                                '双一流类型',
                                '录取最低分',
                                '软科排名',
                                '操作'
                            ]
                        ).outerHTML
                    );
                });
            
            function parseData(data)
            {
                return data.map((_e, id) =>
                    {
                        const e = _e.detail;
                        const result = {
                            'ID': id + 1,
                            '名称': e.name,
                            '办学体制': e.school_nature_name,
                            '办学类型': e.school_type_name + ' ' + e.type_name,
                            '985 / 211': (e.is985 ? '是' : '否') + ' / ' + (e.is211 ? '是' : '否'),
                            '双一流类型': e.dual_class_name,
                            '录取最低分': (e.minscore > 0 ? parseInt(e.minscore) : null),
                            '软科排名': (e.ruanke_rank > 0 ? parseInt(e.ruanke_rank) : null),
                            '操作': mdui.$.createActions([
                                { inner: '查看详情', action: 'mdui.$.api.getSchoolDetail(' + e.school_id + ')' },
                                { inner: '查看招生学科', action: 'mdui.$.api.getProject(' + e.school_id + ')' },
                                { inner: '查看各科分数线', action: 'mdui.$.api.getScore(' + e.school_id + ')' },
                                { inner: '查看历史分数线', action: 'mdui.$.api.getHistoryScore(' + e.school_id + ')' }
                            ])
                        };

                        return result;
                    }
                );
            }
        },
        searchSubject(_keyword, page = 1, noEncode = false)
        {
            let keyword = (noEncode ? _keyword : encodeURIComponent(_keyword))

            mdui.$.get('/searchprojectbypage/' + keyword + '/' + page + '/20')
                .then(data =>
                {
                    if (data.length <= 0)
                    {
                        mdui.alert('没有更多啦', '前方高能');
                        return;
                    }

                    mdui.$.doms.searchResultContainer.html(
                        '<div class="mdui-text-color-theme-disabled mdui-text-center mdui-m-t-1 mdui-m-b-1 mdui-hidden-lg-up">提示：可左右滑动查看更多信息</div>' +
                        mdui.$.createTable(
                            parseData(data),
                            [
                                'ID',
                                '名称',
                                '学校名称',
                                '科目类型',
                                '招生类别',
                                '录取批次',
                                '招生人数',
                                '学费（元/年）',
                                '学年制（年）',
                                '操作'
                            ]
                        ).outerHTML +
                        '<div class="mdui-m-t-2">' +
                        '<button class="mdui-btn mdui-btn-float mdui-ripple mdui-color-theme-accent" onclick="mdui.$.api.searchSubject(\'' + keyword + '\', ' + (page - 1) + ', true)"><i class="mdui-icon material-icons">&#xe314;</i>上一页</button>' +
                        '<button class="mdui-btn mdui-btn-float mdui-ripple mdui-color-theme-accent mdui-float-right" onclick="mdui.$.api.searchSubject(\'' + keyword + '\', ' + (page + 1) + ', true)">下一页<i class="mdui-icon material-icons">&#xe315;</i></button>' +
                        '</div>'
                    );

                    window.scrollTo(0, 0);
                });
            
            function parseData(data)
            {
                return data.map((e, id) =>
                    {
                        const result = {
                            'ID': id + 1,
                            '名称': e.projectname,
                            '学校名称': e.school_name,
                            '科目类型': e.level1_name + ' ' + e.level2_name + ' ' + e.level3_name,
                            '招生类别': e.zslx_name,
                            '录取批次': e.local_batch_name,
                            '招生人数': e.num,
                            '学费（元/年）': e.tuition,
                            '学年制（年）': e.length,
                            '操作': mdui.$.createActions([
                                { inner: '查看学校详情', action: 'mdui.$.api.getSchoolDetail(' + e.school_id + ')' },
                                { inner: '查看学校所有招生学科', action: 'mdui.$.api.getProject(' + e.school_id + ')' }
                            ])
                        };

                        return result;
                    }
                );
            }
        },
        getSchoolDetail(id)
        {
            mdui.$.get('/getSchoolDetail/' + id)
                .then(data =>
                {
                    const preParsedData = {
                        '名称': data.name,
                        '地理位置': data.province_name + ' ' + data.city_name + ' ' + data.town_name,
                        '隶属于': data.belong,
                        '办学体制': data.school_nature_name,
                        '本科类型': data.school_type_name,
                        '院校类型': data.type_name,
                        '图书馆藏书量': data.num_library,
                        '是否为985': (data.is985 ? '是' : '否'),
                        '是否为211': (data.is211 ? '是' : '否'),
                        '双一流类型': data.dual_class_name,
                        '录取最低分': (data.minscore > 0 ? parseInt(data.minscore) : null),
                        '软科排名': (data.ruanke_rank > 0 ? parseInt(data.ruanke_rank) : null),
                        '云上高博会服务平台': data.heec_url,
                        '简介': data.content + '...'
                    };
                    
                    mdui.alert(
                        parseData(
                            preParsedData,
                            [
                                '名称',
                                '地理位置',
                                '隶属于',
                                '办学体制',
                                '本科类型',
                                '院校类型',
                                '图书馆藏书量',
                                '是否为985',
                                '是否为211',
                                '双一流类型',
                                '录取最低分',
                                '软科排名',
                                '云上高博会服务平台',
                                '简介'
                            ]
                        )
                        , '学校详情 - ' + data.name
                    );
                });
            
            function parseData(data, heads)
            {
                const ContainerDOM = document.createElement('div');

                for (const head of heads)
                {
                    let contentDOM = document.createElement('div');
                    contentDOM.setAttribute('data-title', head);

                    if (!data[head] || data[head] == '') {
                        contentDOM.innerHTML = '<span>暂无数据</span>';
                    } else {
                        contentDOM.innerHTML = '<span>' + data[head] + '</span>';
                    }

                    contentDOM.className = 'item';
                    ContainerDOM.appendChild(contentDOM);
                }

                ContainerDOM.className = 'data-list';
                return ContainerDOM.outerHTML;
            }
        },
        getProject(id)
        {
            mdui.$.get('/getProject/' + id)
                .then(data =>
                {
                    mdui.alert(
                        mdui.$.createTable(
                            parseData(data.data),
                            [
                                'ID',
                                '招生类别',
                                '科目类型',
                                '科目大类',
                                '科目小类',
                                '录取批次',
                                '学费（元/年）',
                                '学年制（年）',
                                '计划招生人数'
                            ],
                            false
                        ).outerHTML,
                        '招生学科'
                    );
                });
            
            function parseData(datas)
            {
                const result = [];

                for (const id in datas)
                {
                    const data = datas[id];
                    const currResult = {
                        'ID': (parseInt(id) + 1),
                        '招生类别': data.zslx_name,
                        '科目类型': data.level1_name,
                        '科目大类': data.level2_name,
                        '科目小类': data.level3_name,
                        '录取批次': data.local_batch_name,
                        '学费（元/年）': data.tuition,
                        '学年制（年）': data.length,
                        '计划招生人数': data.num
                    };
                    result.push(currResult);
                }

                return result.sort((a, b) => a.ID - b.ID);
            }
        },
        getScore(id)
        {
            mdui.$.get('/getScore/' + id)
                .then(data =>
                {
                    mdui.alert(
                        mdui.$.createTable(
                            parseData(data),
                            [
                                'ID',
                                '科目名称',
                                '科目类型',
                                '科目大类',
                                '科目小类',
                                '录取批次',
                                '历史最高分',
                                '历史最低分',
                                '平均分'
                            ],
                            false
                        ).outerHTML,
                        '各科分数线'
                    );
                });
            
            function parseData(datas)
            {
                const result = [];

                for (const id in datas)
                {
                    if (!isNaN(datas[id].projectnum)) continue;

                    const data = datas[id];
                    const currResult = {
                        'ID': parseInt(id),
                        '科目名称': data.spname,
                        '科目类型': data.level1_name,
                        '科目大类': data.level2_name,
                        '科目小类': data.level3_name,
                        '录取批次': data.local_batch_name,
                        '历史最高分': data.max,
                        '历史最低分': data.min,
                        '平均分': data.average
                    };

                    result.push(currResult);
                }

                return result.sort((a, b) => a.ID - b.ID);
            }
        },
        getHistoryScore(id)
        {
            mdui.prompt('输入年份（2023年即为预测分数线）', '输入目标年份', (e) =>
            {
                const SelectedYear = Math.round(parseInt(e));
                let apiPath = '';

                if (isNaN(SelectedYear) || (SelectedYear < 2018 || SelectedYear > 2023))
                {
                    mdui.alert('您输入的年份有误', '前方高能');
                    return;
                }

                if (SelectedYear >= 2023) apiPath = '/results/' + id + '_all.json';
                else apiPath = '/history/' + SelectedYear + '/' + id + 'score.json';

                mdui.$.ajax({
                    method: 'GET',
                    url: AJAX_HISTORY_HOST + apiPath,
                    dataType: 'json',
                    xhrFields: {
                        withCredentials: true
                    },
                    success(data) {
                        mdui.alert(
                            mdui.$.createTable(
                                parseData(data),
                                [
                                    '科目名称',
                                    '最低分',
                                    '最高分',
                                    '平均分'
                                ],
                                false
                            ).outerHTML,
                            SelectedYear + '年分数线' + (SelectedYear >= 2023 ? '预测' : '查询')
                        );
                    },
                    error(e) {
                        errorHandler(e);
                    }
                });
            });

            function parseData(datas)
            {
                const result = [];

                if (datas instanceof Array)
                {
                    for (const data of datas)
                    {
                        result.push({
                            '科目名称': data.name,
                            '最低分': data['2023'].min,
                            '最高分': data['2023'].max,
                            '平均分': data['2023'].average
                        });
                    }
                }
                else
                {
                    for (const name in datas.data)
                    {
                        const _datas = datas.data[name].item;

                        for (const data of _datas)
                        {
                            result.push({
                                '科目名称': data.spname,
                                '最低分': data.min,
                                '最高分': data.max,
                                '平均分': data.average
                            });
                        }
                    }
                }

                return result;
            }
        }
    }
});



function errorHandler(e)
{
    try {
        if (!e.responseText || e.responseText == '') throw 'Switch to catch';
        const json = JSON.parse(e.responseText);
        mdui.alert('电波好像对不上了，请稍候再试吧！(' + json.code + ': ' + json.msg + ')', '出错啦！');
    } catch (_e) {
        if (typeof e.status === 'number') {
            mdui.alert('电波好像对不上了，请稍候再试吧！(' + e.status + (typeof e.statusText === 'string' && e.statusText != '' ? ': ' + e.statusText : '') + ')', '出错啦！');
        } else {
            mdui.alert('电波好像对不上了，请稍候再试吧！', '出错啦！');
        }
    }
}

})();