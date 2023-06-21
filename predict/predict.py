import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error
import json


def readfile(id):
    data_all = []
    isline1 = False
    isline2 = False
    with open('history/2022/' + str(id) + '_score.json', 'r') as f1:
        data = json.load(f1)['data']
    key_name = next(iter(data))  # 得到傻逼随机键名
    data = data[key_name]
    numFound = data['numFound']
    item = data['item']
    for line in item:
        special_id = line['special_id']
        max = line['max']
        min = line['min']
        average = line['average']
        # 本身可以写个循环优化一下的但是我真的懒了
        try:
            with open('history/2021/' + str(id) + '_score.json', 'r') as f1:
                data1 = json.load(f1)['data']
                key_name = next(iter(data1))  # 得到傻逼随机键名
                data1 = data1[key_name]
                item1 = data1['item']
                for line1 in item1:
                    if line1['special_id'] == special_id:
                        max1 = line1['max']
                        min1 = line1['min']
                        average1 = line1['average']
                        isline1 = True
                if isline1 is not True:
                    max1 = max
                    min1 = min
                    average1 = average
        except:
            max1 = max
            min1 = min
            average1 = average

        # 如果当年没有数据就拿去年的代替掉 不严谨但是能用
        try:
            with open('history/2020/' + str(id) + '_score.json', 'r') as f1:
                data2 = json.load(f1)['data']
            key_name2 = next(iter(data2))  # 得到傻逼随机键名
            data2 = data2[key_name2]
            item2 = data2['item']
            for line2 in item2:
                if line2['special_id'] == special_id:
                    max2 = line2['max']
                    min2 = line2['min']
                    average2 = line2['average']
                    isline2 = True
            if isline2 is not True:
                max2 = max
                min2 = min
                average2 = average
        except:
            max2 = max
            min2 = min
            average2 = average

        # 如果当年没有数据就拿去年的代替掉 不严谨但是能用
        singledata = {
            'name': line['spname'],
            '2022': {
                'max': max,
                'min': min,
                'average': average
            },
            '2021': {
                'max': max1,
                'min': min1,
                'average': average1
            },
            '2020': {
                'max': max2,
                'min': min2,
                'average': average2
            },
        }
        data_all.append(singledata)
    return data_all


def predict(data1, data2, data3):
    X = np.array([[2022], [2021], [2020]])  # 年份
    Y = np.array([data1, data2, data3])  # 录取分数

    best_degree = 1  # 最佳多项式次数
    best_mse = float('inf')  # 初始化最佳均方误差为无穷大

    for degree in range(1, 6):  # 尝试多项式次数从1到5
        # 创建多项式特征
        poly_features = PolynomialFeatures(degree=degree)
        X_poly = poly_features.fit_transform(X)

        # 创建多项式回归模型
        model = LinearRegression()

        # 训练模型
        model.fit(X_poly, Y)

        # 预测数据
        Y_pred = model.predict(X_poly)

        # 计算均方误差
        mse = mean_squared_error(Y, Y_pred)

        # 比较并更新最佳拟合方案
        if mse < best_mse:
            best_mse = mse
            best_degree = degree

    # 选择最佳拟合方案
    poly_features = PolynomialFeatures(degree=best_degree)
    X_poly = poly_features.fit_transform(X)
    model = LinearRegression()
    model.fit(X_poly, Y)

    # 预测2023年的录取分数
    year_2023 = np.array([[2023]])  # 今年的年份
    year_2023_poly = poly_features.transform(year_2023)
    predicted_score = model.predict(year_2023_poly)

    # 获取拟合函数的系数和截距
    coefficients = model.coef_
    intercept = model.intercept_

    # 构建拟合函数的表达式
    expression = f"{intercept:.2f}"
    for i, coef in enumerate(coefficients[1:], start=1):
        expression += f" + {coef:.2f} * X^{i}"

    # 输出结果
    # print("最佳拟合方案的多项式次数:", best_degree)
    # print("最佳拟合方案的均方误差:", best_mse)
    # print("预测的2023年录取分数:", predicted_score[0])
    # print("拟合函数的表达式:", expression)
    return predicted_score[0]


def predictall(id):
    data = readfile(id)
    for line in data:
        line['2022']['max'] = float(line['2022']['max'])
        line['2022']['min'] = float(line['2022']['min'])
        if line['2022']['average'] == '-':
            line['2022']['average'] = round((line['2022']['max']+line['2022']['min'])/2,2)
        else:
            line['2022']['average'] = float(line['2022']['average'])
        line['2021']['max'] = float(line['2021']['max'])
        line['2021']['min'] = float(line['2021']['min'])
        if line['2021']['average'] == '-':
            line['2021']['average'] = round((line['2021']['max']+line['2021']['min'])/2,2)
        else:
            line['2021']['average'] = float(line['2021']['average'])
        line['2020']['max'] = float(line['2020']['max'])
        line['2020']['min'] = float(line['2020']['min'])
        if line['2020']['average'] == '-':
            line['2020']['average'] = round((line['2020']['max']+line['2020']['min'])/2,2)
        else:
            line['2020']['average'] = float(line['2020']['average'])
        max_predict = predict(float(line['2022']['max']), float(line['2021']['max']), float(line['2020']['max']))
        min_predict = predict(float(line['2022']['min']), float(line['2021']['min']), float(line['2020']['min']))
        average_predict = predict(float(line['2022']['average']), float(line['2021']['average']),
                                  float(line['2020']['average']))
        line['2023'] = {'max': round(max_predict, 2),
                        'min': round(min_predict, 2),
                        'average': round(average_predict, 2)
                        }
    return data


i = 30
while i <4000:
    try:
        datawrite = json.dumps(predictall(i))
        resultfile = open('results/' + str(i) + '_all.json', 'a+')
        resultfile.write(datawrite)
        resultfile.close()
        i = i + 1
    except ValueError:
        print(i)
        i = i +1
    except Exception as e:
        i = i +1
