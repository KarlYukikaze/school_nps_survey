import pandas as pd
import copy
import time
import school_survey_prepare

'''对问卷平台导出的原始回复csv进行清洗，筛出无效回复'''

class Validity_Check:
    def __init__(self, data:pd.DataFrame) -> None:
        self.data = data

    '''判断无效问卷：各客观题全打同一分值and主观题不填写and学部和年级不匹配'''
    def get_validity (self, show=False) -> list:
        validity = []
        invalid_list = []
        unit_dict = {'高中': ['十年级','十一年级','十二年级','高一年级','高二年级','高三年级'],
        '初中': ['九年级','八年级','七年级','初一年级','初二年级','初三年级'],
        '小学': ['一年级','二年级','三年级','四年级','五年级','六年级'],
        '幼儿园': ['幼儿园']}
        
        '''data前面的x列为用户基本信息'''
        x = len(school_survey_prepare.user_info)
        n = self.data.shape[1] - x -1
        for i in range(len(self.data)):

            '''检测各打分题全打同一分值'''
            row = []
            row = []
            for j in range(1,n):
                q_id = 'q{}'.format(str(j))
                response = self.data[q_id][i]
                row.append(response)
            row = pd.Series(row)
            no_repeat = (len(row.unique()) != 1)

            '''检测主观题是否填写。这个 na in ...的判断条件是根据实际csv里的内容来的.
            另外这里假设最后一题是主观题'''

            no_opinion = ('na' in str(self.data.iloc[:,-1][i]))

            '''检验学部和班级填错'''
            school = self.data['school'][i]
            grade = self.data['grade'][i]
            grade_set = set(unit_dict[school])
            matched = grade in grade_set

            '''条件1：:一条回复的客观题全都填写同一个值且主观题未填写。
            条件2：学部和年级不匹配。 两个条件满足一条即为无效'''
            if  ((not no_repeat) and no_opinion) or (not matched): 
                valid = False
                invalid_list.append(i) 
            else:
                valid = True
            validity.append(valid)   
    
        valid_rate = round(100*(validity.count(True) / len(validity)),1)

        '''输出结果'''
        if show == True:
            print('总数： {}'.format(len(self.data)))
            print('无效个数： {}'.format(validity.count(False)))
            print('有效个数： {}'.format(validity.count(True)))
            print('有效率： {}%'.format(valid_rate))
            print('\n')
        validity = pd.Series(validity)
        return validity

    '''在前面的check方法基础上，输出完整dataframe： 
    清理无效回复后的dataframe  or  原始dataframe加上有效性字段'''
    def prepare_data(self, type:str, show=False) ->pd.DataFrame:
            
        new_data = copy.deepcopy(self.data)
        new_data['validity'] = self.get_validity(show=show)
        if type == 'clean':
            clean_data = new_data.loc[new_data.validity == True]
            return clean_data
        
        elif type == 'validity':
            return new_data

    '''保存输出的datafram到本地'''
    def write_new_data(self, type:str, path:str, show=False):
        t = time.localtime()
        t = '{year}_{mon}_{day}'.format(year=str(t.tm_year), mon=str(t.tm_mon),day = str(t.tm_mday)) 

        csv = self.prepare_data(type=type, show=show)
        file_name = t+'_{}.csv'.format(type)
        csv.to_csv(path+file_name)
        print((path+file_name))

if __name__ == '__main__':

    data = pd.read_csv(r'D:/test/2021_6_16_prepared.csv')
    v_check = Validity_Check(data)
    v_check.get_validity()
    v_check.write_new_data(type='validity', path=r'D:/test/')
    v_check.write_new_data(type='clean', path=r'D:/test/', show=True)