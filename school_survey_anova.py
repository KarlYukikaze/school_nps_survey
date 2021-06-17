from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
import pandas as pd

data = pd.read_csv(r'D:/2021/2021clean.csv', encoding='gbk')
data = data.loc[data['年份'] == 2021]



for i in range(1,19):
    formula = 'q{} ~ grade'.format(i)
    print('\n')
    print(formula)
    print('-'*10)
    print('\n')
    model = ols(formula, data=data).fit()
    anova_table = anova_lm(model, typ = 1)
    print(anova_table)