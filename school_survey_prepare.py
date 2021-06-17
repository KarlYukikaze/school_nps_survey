import pandas as pd
import time
import re

user_info = ['id','start','end','time','counrty','province','city',
        'relationship','school','grade','class']

'''导入腾讯问卷原始的数据格式，详见模板，进行处理，删除无用的字段，重命名字段名称'''
class Data_Prepare:
    def __init__(self,file) -> None:
        self.path = file
        self.data = pd.read_csv(file)
        self.user_info = user_info

    '''先把无用的字段删除，此处的字段名称可参照实际问卷修改'''
    def col_drop(self) -> pd.DataFrame:
        drop = ['用户类型','用户标识','昵称','自定义字段',
        '3.您居住或工作的省市是？In whichprovince or city do you livein?',
        '4.您和孩子的关系是？What&#39;s your relationship with the student?[选项填空]']
        new_data = self.data.drop(labels=drop, axis=1)
        return new_data

    '''重命名column_names，分为两部分，用户基础信息字段以及具体问题字段'''
    def col_rename(self,data:pd.DataFrame) -> pd.DataFrame:
        user_info = self.user_info

        '''用户基础信息字段之外的，字段名称转换成q1,q2,q3...的格式'''
        ques_id = []
        n = 1 + data.shape[1] - len(user_info)
        for i in range(1,n):
            id = 'q{}'.format(i)
            ques_id.append(id)

        new_col_names = user_info + ques_id
        data.columns = new_col_names

        ''''某些情况下，导入的csv会出现某一列全部为空的情况，通过dropna处理一下'''
        data = data.dropna(axis=1, how='all')
        data = data.dropna(axis=0, how='all')
        return data

    def prepare_data(self) -> pd.DataFrame:
        prepared_data = self.col_drop()
        prepared_data = self.col_rename(data=prepared_data)

        '''需要把选项的ABCD以及 . 去掉'''
        sub = lambda x: re.sub('[a-zA-Z0-9 .]','',x)

        for i in ['relationship', 'school', 'grade']:
            l = list(map(sub, [x for x in prepared_data[i]]))
            prepared_data[i] = pd.Series(l)

        prepared_data['class'] = prepared_data['grade'] + ' ' + prepared_data['class']

        return prepared_data

    def write_prepared_data(self, path:str):

        t = time.localtime()
        t = '{year}_{mon}_{day}'.format(year=str(t.tm_year), mon=str(t.tm_mon),day = str(t.tm_mday)) 

        csv = self.prepare_data()
        file_name = t+'_prepared.csv'
        csv.to_csv(path+file_name)
        print((path+file_name))

if __name__ == '__main__':
    data = Data_Prepare(file=r'D:/test/2021.csv')
    data.write_prepared_data(path=r'D:/test/')