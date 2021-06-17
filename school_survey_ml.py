import numpy as np
import pandas as pd
from sklearn import tree
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
data = pd.read_csv(r'D:/2021/2021clean.csv', encoding='gbk')

features = ['q1', 'q2', 'q3', 'q4','q5','q6','q7','q8','q9','q10']
X = data[features]
y = data['q19']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=1)

clf = tree.DecisionTreeClassifier(max_depth=3)
clf = clf.fit(X_train, y_train)
y_predict = pd.Series(clf.predict(X_test))
y_predict = y_predict.to_list()

d = {'test':y_test, 'predict':y_predict}
test = pd.DataFrame(d)


model = ols('test ~ predict', data=test).fit()
anova_table = anova_lm(model, typ = 1)

import scipy.stats as st
print(st.levene(y_test,y_predict))

'''绘制混淆矩阵'''

from sklearn.metrics import confusion_matrix

plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文字体
plt.rcParams["axes.unicode_minus"] = False

cm = confusion_matrix(y_test, y_predict)

correct_num = 0
for i in range(cm.shape[0]):
    correct_num += cm[i,i]

correct_rate = (correct_num) / cm.sum()
print(correct_rate)

plt.matshow(cm)
plt.colorbar()

for x in range(len(cm)):
    for y in range(len(cm)):
        plt.annotate(cm[x,y], xy=(x,y), horizontalalignment='center', verticalalignment='center')
plt.ylabel('真实值')
plt.xlabel('预测值')
plt.title('混淆矩阵')



from sklearn.metrics import roc_curve

'''绘制roc曲线'''
y_score = clf.predict_proba(X_test)[:,1]
fpr1, tpr1, thresholds1 = roc_curve(y_test, y_score, pos_label=1)
plt.plot(fpr1, tpr1)
plt.xlabel('假正例率')
plt.ylabel('真正例率')
plt.xlim(0,1.05)
plt.ylim(0,1.05)
plt.title('分类树-ROC曲线')
