import wget

i = 20
while i < 4001:
    try:
        url ='https://static-data.gaokao.cn/www/2.0/schoolspecialscore/' + str(i) + '/2019/62.json'
        print(url)
        wget.download(url=url,out=str(i)+'_score.json')
        print('[+]' + str(i) + 'success!')
    except Exception as e:
        print('[x]' + str(i) + 'Failed!')
        print(e)
    i = i + 1
