from school_survey_prepare import Data_Prepare
from school_survey_validity import Validity_Check
from school_survey_NPS import NPS_Calculator

file = r'D:/test/2021.csv'
prepare = Data_Prepare(file=file)
prepare.write_prepared_data(path=r'D:/test/苏州')
data = prepare.prepare_data()

vcheck = Validity_Check(data=data, ques_num=20)
vcheck.write_new_data(type='clean',path=r'D:/test/苏州')
vcheck.write_new_data(type='validity',path=r'D:/test/苏州')
data = vcheck.prepare_data(type='clean', show=True)

cal = NPS_Calculator(data=data)
cal.write_nps_data(level='all', path=r'D:/test/苏州')
nps_data = cal.prepare_data(level='all')
