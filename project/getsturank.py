import requests
import wget

i = 20
while i < 4001:
    try:
        url ='https://static-data.gaokao.cn/www/2.0/schoolspecialplan/' + str(i) + '/2022/62.json'
        print(url)
        wget.download(url=url,out=str(i)+'_project.json')
        print('[+]' + str(i) + 'success!')
    except Exception as e:
        print('[x]' + str(i) + 'Failed!')
        print(e)
    i = i + 1
