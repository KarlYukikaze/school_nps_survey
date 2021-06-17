
from tokenize import group
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt

data = pd.read_csv(r'D:/2021/2021clean.csv', encoding='gbk')

formula = 'NPS ~ '
for i in range(1,17):
    text = 'q{} +'.format(str(i))
    formula += text

formula += ' q17'
print(formula)


formula = 'NPS~q1'
mixed_lm = smf.mixedlm(formula=formula, data=data, groups=data['school']).fit()
print(mixed_lm.summary())

anotherformula = 'NPS ~ 课程设置 + 日常教学 + 家校沟通 + 校园生活 + 学生成长 + 校园环境 + school'
mixed_lm = smf.mixedlm(formula=formula, data=data, groups=data['school']).fit()
print(mixed_lm.summary())
