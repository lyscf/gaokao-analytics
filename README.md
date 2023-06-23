# gaokao-analytics

利用python爬虫爬取高考录取分数线，招生计划以及学校计划，并尝试进行分数线预测

## 关于项目

由于作者为今年甘肃理科高考生，故采集数据的程序全部是甘肃理科，其他地区请通过在gaokao.cn自行抓包找到你的地区ID

例如 https://static-data.gaokao.cn/www/2.0/schoolspecialplan/34/2022/62.json 这个URL中的62就是甘肃理科的地区ID，其余地区请自行测试）

本项目仅提供了一个作为交流学习的测试程序，请不要用于非法采集/测试/盈利，产生的后果本人同样不担任何责任

本项目遵循GPL3.0协议开源，任何使用该项目的项目必须遵循同样协议并开源并不得商用

项目采用python和flask进行编写，并提供了api进行快速筛选，API接口文档没有写，但是应该是能看懂的罢（心虚）


## How-to-use

首先，请运行history(历史录取数据),info(学校信息介绍),rank(学校具体排名),project(学校招生计划),文件夹中的getxxxxx.py以获取数据

之后，你需要将history目录复制到predict目录下开始进行数据预测

运行predict.py开始预测，假设数据完整并与年份存在相关关系(这个预测我真不知道咋做所以就求助了万能的chatgpt)

最后，你可以启动api.py，默认监听1145端口

## 配置前端


感谢[MisaLiu](https://github.com/MisaLiu)写的前端! 

前端为静态HTML+JS+CSS，你需要做的就是修改/js/ajax.js中的两个域名为后端的域名即可

同时,你需要把后端的/predict目录复制到/static目录下以便请求预测数据

