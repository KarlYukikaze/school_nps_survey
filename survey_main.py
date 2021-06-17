from school_survey_prepare import Data_Prepare
from school_survey_validity import Validity_Check
from school_survey_NPS import NPS_Calculator
import time

class DataCleaner():

    def __init__(self,file:str, save_path:str) -> None:
        self.file = file
        self.save_path = save_path

    def run(self):
        prepare = Data_Prepare(file=self.file)
        prepare.write_prepared_data(path=self.save_path)
        time.sleep(0.5)
        print('已输出仅包含必要字段的数据')
        print('\n')
        data = prepare.prepare_data()

        vcheck = Validity_Check(data=data)

        vcheck.write_new_data(type='validity',path=self.save_path)
        time.sleep(0.5)
        print('已输出包含校验结果的原始数据数据')
        print('\n')

        vcheck.write_new_data(type='clean',path=self.save_path)
        time.sleep(0.5)
        print('已输出清洗完成的数据')
        print('\n')

        data = vcheck.prepare_data(type='clean', show=True)
        cal = NPS_Calculator(data=data)
        cal.write_nps_data(level='all', path=self.save_path)
        time.sleep(0.5)
        print('已输出各个层级的NPS数据')
        print('\n')
        time.sleep(0.5)
        print('数据预处理已完成 \n请前往目录查看相应csv文件')

if __name__ == '__main__':
    pass