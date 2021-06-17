from jieba.finalseg import cut
import pandas as pd
import jieba
import jieba.analyse

class NLP :

    def __init__(self, data) -> None:
        self.useless = ['学生', '学校', '孩子', '老师', '希望', '加强', '可以', '能够', '', '没有', '提高', '暂时', '建议', '幼儿园', '小学', '初中', '高中']
        self.data = data

    '''获取每个unit的主观题回复'''
    def get_opinion(self, unit:str) -> dict:
        unit_dict = {}
        data = self.data
        if unit != 'all':
            for name in data[unit].unique():
                rows = data.loc[data[unit] == name]
                unit_dict[str(name)] = rows['q20'].to_list()
    
        else:
            unit_dict['all'] = data['q20'].to_list()
        return unit_dict

    '''TF IDF计算每个层级回复的主题，去除无意义的多个关键词'''
    def get_topic(self, unit_dict) -> dict:
        key_words_dict = {}
        for name in unit_dict.keys():
            full_text = ''
            for opinion in unit_dict[str(name)]:
                full_text += opinion
            keywords = jieba.analyse.extract_tags(full_text, topK=25)
            for word in self.useless:
                if word in keywords:
                    keywords.remove(word)
                else:
                    pass
            keywords = keywords[0:6]
            key_words_dict[str(name)] = keywords
            key_words_data = (pd.DataFrame(key_words_dict)).transpose()
        return key_words_data

    def write_keywords_data(self, unit:str, path:str):
        a = self.get_opinion(unit=unit)
        b = self.get_topic(unit_dict=a)
        path = path + '{}'.format(unit)+'_keywords.csv'
        b.to_csv(path)
        print(b)



