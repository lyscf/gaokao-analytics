import json
from flask_cors import CORS
from flask import jsonify, Flask

app = Flask(__name__)

i = 30
totalList = []
while i < 4000:
    try:
        file = open('info/' + str(i) + '_info.json', 'r')
        data = json.load(file)['data']
        name = data['name']
        school_id = data['school_id']
        totalList.append({'name': name, 'school_id': school_id})
        i = i + 1
        file.close()
    except Exception as e:
        i = i + 1


# 将对应关系写进内存里面


def get_school_detail_in_memory(id):
    with open('info/' + str(id) + '_info.json', 'r') as f:
        data = json.load(f)['data']
    school_id = data['school_id']  # 后台给他的id，剩下的同理
    name = data['name']  # 北京工业大学
    belong = data['belong']  # 北京市
    if data['f985'] == '1':
        is985 = True
    else:
        is985 = False
    if data['f211'] == '1':
        is211 = True
    else:
        is211 = False
    try:
        # 接下来的内容要他妈的试一下因为不一定都有
        ruanke_rank = data['ruanke_rank']  # 63
    except:
        print('error')
    type_name = data['type_name']  # 理工类
    school_type_name = data['school_type_name']  # 普通本科
    try:
        minscore = data['province_score_min']['62']['min']  # 62是甘肃理科的编号 其余的没测试
    except:
        minscore = 0
    gbh_url = data['gbh_url']  # https://heec.cahe.edu.cn/school/9 高等教育领域数字化综合服务平台的数据 可以看科研成果
    num_library = data['num_library']  # 114514万
    dual_class_name = data['dual_class_name']  # 双一流
    province_name = data['province_name']  # 北京
    city_name = data['town_name']  # 北京市
    town_name = data['town_name']  # 海淀区
    school_nature_name = data['school_nature_name']  # 公办
    content = data['content']
    f.close()
    data = {
        'school_id': school_id,
        'name': name,
        'belong': belong,
        'is985': is985,
        'is211': is211,
        'ruanke_rank': ruanke_rank,
        'type_name': type_name,
        'school_type_name': school_type_name,
        'minscore': minscore,
        'heec_url': gbh_url,
        'num_library': num_library,
        'dual_class_name': dual_class_name,
        'province_name': province_name,
        'town_name': town_name,
        'city_name': city_name,
        'school_nature_name': school_nature_name,
        'content': content
    }
    return data


@app.route('/api/getProject/<id>')
def get_project(id):
    try:
        print('project/' + str(id) + '_project.json')
        with open('project/' + str(id) + '_project.json', 'r') as f:
            data = json.load(f)['data']
    except:
        return jsonify({'code': 404, 'msg': 'No project for this area!'}), 404
    key_name = next(iter(data))  # 得到傻逼随机键名
    data = data[key_name]
    dataset = []
    for line in data['item']:
        dataset.append({
            'num': line['num'],
            'length': line['num'],
            'tuition': line['tuition'],
            'level1_name': line['level1_name'],  # 本科
            'level2_name': line['level2_name'],  # 文学
            'level3_name': line['level3_name'],  # 中国语言文学类
            'zslx_name': line['zslx_name'],  # 普通类
            'local_batch_name': line['local_batch_name']
        })
    dataall = {
        'numFound': data['numFound'],
        'data': dataset
    }
    return jsonify(dataall)


@app.route('/api/getScore/<id>')
def get_score(id):
    try:
        with open('score/' + str(id) + '_score.json', 'r') as f:
            data = json.load(f)['data']
    except:
        return jsonify({'code': 404, 'msg': 'No score for this area!'}), 404
    key_name = next(iter(data))  # 得到傻逼随机键名
    data = data[key_name]  # 再次解析得到data
    item = data['item']
    dataset = {}
    dataset[0] = {'projectnum': data['numFound']}
    i = 1
    for line in item:
        dataset[int(i)] = {
            'max': line['max'],  # 442
            'min': line['min'],  # 434
            'average': line['average'],  # 437.85
            'level1_name': line['level1_name'],  # 本科
            'level2_name': line['level2_name'],  # 文学
            'level3_name': line['level3_name'],  # 中国语言文学类
            'local_batch_name': line['local_batch_name'],  # 本科二批K段
            'spname': line['spname']  # 中国语言文学
        }
        i = i + 1
    i = 1
    return jsonify(dataset)


@app.route('/api/getSchoolDetail/<id>')
def get_SchoolDetail(id):
    try:
        with open('info/' + str(id) + '_info.json', 'r') as f:
            data = json.load(f)['data']
    except:
        return jsonify({'code': 404, 'msg': 'No such school!'}), 404
    school_id = data['school_id']  # 后台给他的id，剩下的同理
    name = data['name']  # 北京工业大学
    belong = data['belong']  # 北京市
    if data['f985'] == '1':
        is985 = True
    else:
        is985 = False
    if data['f211'] == '1':
        is211 = True
    else:
        is211 = False
    try:
        # 接下来的内容要他妈的试一下因为不一定都有
        ruanke_rank = data['ruanke_rank']  # 63
    except:
        print('error')
    type_name = data['type_name']  # 理工类
    school_type_name = data['school_type_name']  # 普通本科
    try:
        minscore = data['province_score_min']['62']['min']  # 62是甘肃理科的编号 其余的没测试
    except:
        minscore = 'null'
    gbh_url = data['gbh_url']  # https://heec.cahe.edu.cn/school/9 高等教育领域数字化综合服务平台的数据 可以看科研成果
    num_library = data['num_library']  # 114514万
    dual_class_name = data['dual_class_name']  # 双一流
    province_name = data['province_name']  # 北京
    city_name = data['town_name']  # 北京市
    town_name = data['town_name']  # 海淀区
    school_nature_name = data['school_nature_name']  # 公办
    content = data['content']
    f.close()
    data = {
        'school_id': school_id,
        'name': name,
        'belong': belong,
        'is985': is985,
        'is211': is211,
        'ruanke_rank': ruanke_rank,
        'type_name': type_name,
        'school_type_name': school_type_name,
        'minscore': minscore,
        'heec_url': gbh_url,
        'num_library': num_library,
        'dual_class_name': dual_class_name,
        'province_name': province_name,
        'town_name': town_name,
        'city_name': city_name,
        'school_nature_name': school_nature_name,
        'content': content
    }
    return jsonify(data)


@app.route('/api/search/<query>')
def search(query):
    search_result = []
    for list in totalList:
        if query in list['name']:
            list['detail'] = get_school_detail_in_memory(list['school_id'])
            search_result.append(list)
        else:
            continue
    return jsonify(search_result)


@app.route('/api/searchproject/<query>/<page>')
def search_project(query, page):
    search_result = []
    for i in totalList:
        try:
            with open('project/' + str(i['school_id']) + '_project.json', 'r') as f:
                data = json.load(f)['data']
                key_name = next(iter(data))  # 得到傻逼随机键名
                data = data[key_name]  # 再次解析得到data
                for line in data['item']:
                    if query in str(line['spname']):
                        search_result.append({
                            'school_id': i['school_id'],
                            'school_name': i['name'],
                            'projectname': line['spname'],
                            'num': line['num'],
                            'length': line['num'],
                            'tuition': line['tuition'],
                            'level1_name': line['level1_name'],  # 本科
                            'level2_name': line['level2_name'],  # 文学
                            'level3_name': line['level3_name'],  # 中国语言文学类
                            'zslx_name': line['zslx_name'],  # 普通类
                            'local_batch_name': line['local_batch_name']
                        })
        except:
            continue

    return jsonify(search_result)


@app.route('/api/searchprojectbypage/<query>/<page>/<page_size>')
def search_projectbypage(query, page, page_size):
    search_result = []
    start_index = (int(page) - 1) * int(page_size)
    end_index = start_index + int(page_size)
    for i in totalList:
        try:
            with open('project/' + str(i['school_id']) + '_project.json', 'r') as f:
                data = json.load(f)['data']
                key_name = next(iter(data))
                data = data[key_name]
                for line in data['item']:
                    if query in str(line['spname']):
                        search_result.append({
                            'school_id': i['school_id'],
                            'school_name': i['name'],
                            'projectname': line['spname'],
                            'num': line['num'],
                            'length': line['num'],
                            'tuition': line['tuition'],
                            'level1_name': line['level1_name'],
                            'level2_name': line['level2_name'],
                            'level3_name': line['level3_name'],
                            'zslx_name': line['zslx_name'],
                            'local_batch_name': line['local_batch_name']
                        })
        except:
            continue

    paginated_result = search_result[start_index:end_index]
    return jsonify(paginated_result)


@app.route('/api/announce')
def set_announce():
    return jsonify({'msg': '这是一个一个一个公告啊啊啊啊啊(错乱'})


CORS(app, supports_credentials=True)
app.run(host='0.0.0.0', port=1145)
