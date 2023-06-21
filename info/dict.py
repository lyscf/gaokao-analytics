import json


# 读取JSON文件
def readfile(num):
    with open(str(num) + '_info.json', 'r') as f:
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
    minscore = data['province_score_min']['62']['min']  # 62是甘肃理科的编号 其余的没测试
    gbh_url = data['gbh_url']  # https://heec.cahe.edu.cn/school/9 高等教育领域数字化综合服务平台的数据 可以看科研成果
    f.close()
    data= {
        'school_id':school_id,
        'name':name,
        'belong':belong,
        'is985':is985,
        'is211':is211,
        'ruanke_rank':ruanke_rank,
        'type_name':type_name,
        'school_type_name':school_type_name,
        'minscore':minscore,
        'gbh_url':gbh_url
    }
    '''
    print('====================================')
    print(school_id)
    print(name)
    print(belong)
    print(is985)
    print(is211)
    print(ruanke_rank)
    print(type_name)
    print(school_type_name)
    print(minscore)
    print(gbh_url)
    print('====================================')
    '''
    # print(data)
    return data
dataset = {}
i = 30
while i < 4000:
    try:
        dataset[i] = readfile(i)
        i = i + 1
    except Exception as e:
        i = i + 1
print(json.dumps(dataset))