import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error

# 输入数据
X = np.array([[2022], [2021], [2020]])  # 年份
Y = np.array([442, 440, 458])  # 录取分数

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
year_2023 = np.array([[2020]])  # 今年的年份
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
print("最佳拟合方案的多项式次数:", best_degree)
print("最佳拟合方案的均方误差:", best_mse)
print("预测的2023年录取分数:", predicted_score[0])
print("拟合函数的表达式:", expression)
