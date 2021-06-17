import pandas as pd
import time
'''NPS计算器：输出各个层级的NPS值'''
class NPS_Calculator:

    def __init__(self, data:pd.DataFrame) -> None:
        self.data = data

    '''计算一列回复的NPS score'''
    def cal_nps_score(self, indidual_nps:list) -> float:
        pro = 0
        neu = 0
        dis = 0
        for i in indidual_nps:
            if i > 8:
                pro += 1
            elif i < 7:
                dis += 1
            else: 
                neu += 1
        
        nps_socre = round(100*((pro - dis) / len(indidual_nps)),2)
        return nps_socre

    '''找到并存储所选层级（全校、学部、年级、班级）下每个人的response'''
    def get_nps_response(self, level:str) -> dict:
        '''这部分默认问卷问卷倒数第二题是NPS打分，其中data的-1列是validity，-2列是开放题，-3是实际的倒数第2题NPS打分'''
        level_dict = {}
        if level != 'whole':
            for unit_name in self.data[level].unique():
                rows = self.data.loc[self.data[level] == str(unit_name)]
                level_dict[str(unit_name)] = rows.iloc[:,-3].tolist()
        else:
            level_dict['whole'] = self.data.iloc[:,-3].tolist()
        return level_dict

    '''计算一个层级下，所有单元的nps_score'''
    def get_nps_score(self, level_dict:dict) -> pd.DataFrame:
        unit_nps_score = []
        unit_names = []
        for key in level_dict.keys():
            nps_score = self.cal_nps_score(indidual_nps=level_dict[key])
            unit_nps_score.append(nps_score)
            unit_names.append(key)
        level_nps_data = pd.DataFrame({'unit':unit_names, 'nps_score':unit_nps_score})
        return level_nps_data

    def prepare_data(self, level:str) ->pd.DataFrame:
        if level != 'all':
            level_dict = self.get_nps_response(level=level)
            prepared_data = self.get_nps_score(level_dict=level_dict)
            prepared_data['level'] = [level]*len(prepared_data)

        else:
            level_dict = self.get_nps_response(level='whole')
            prepared_data = self.get_nps_score(level_dict=level_dict)
            prepared_data['level'] = ['whole']*len(prepared_data)

            for l in ['school','grade','class']:
                level_dict = self.get_nps_response(level=l)
                level_data = self.get_nps_score(level_dict=level_dict)
                level_data['level'] = [l]*len(level_data)
                prepared_data = pd.concat([prepared_data,level_data])
        return prepared_data

    '''保存某个层级下所有单元的nps_score到本地'''
    def write_nps_data(self, level:str, path:str):
       
        t = time.localtime()
        t = '{year}_{mon}_{day}'.format(year=str(t.tm_year), mon=str(t.tm_mon),day = str(t.tm_mday)) 

        csv = self.prepare_data(level=level)
        file_name = t+'_{}_NPS.csv'.format(level)
        csv.to_csv(path+file_name)
        return csv

if __name__ == '__main__':

    data = pd.read_csv(r'D:/test/2021_6_16_clean.csv')

    nps = NPS_Calculator(data=data)
    nps.write_nps_data(level='all', path=r'D:/test/')
