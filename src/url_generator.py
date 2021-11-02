'''
this file generate all urls to be saved as pdf file
input:
a table of companies and locations, with form:
    xxx公司   xx省;xx市
a table of base url for each location and each website
'''


# %%
from pandas import read_excel, DataFrame
import copy

def is_chinese(string):
    """
    检查整个字符串是否包含中文
    :param string: 需要检查的字符串
    :return: bool
    """
    for ch in string:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True

    return False

def is_digit(string):
    for s in string:
        if s not in '0123456789':
            return False
    return True

def valid_column(string):
    # return if column name indicates place for a company
    return type(string) == int

class UrlGenerator:
    '''
    given 
    1. company and its location (including 省市区... (multi-hierarchy))
    2. required type (e.g. 工商、人社, ...) and the website url for each location (multi-hierarchy)
    return
    a txt file of targeted pdf name and corresponding url, each line is
    ```
    xxx公司-xx(省/市/区/县...)-类型(e.g. 工商、人社, ...)\turl
    ```
    '''
    def __init__(self, logwriter=None, text_to_replace="{}"):
        self.logwriter = logwriter
        self.text_to_replace = text_to_replace

    def write_info(self, info):
        print(info)
        if self.logwriter is not None:
            self.logwriter.write(info)

    def load_company_data(self, filepath):
        '''
        return: {company_name: (place1, place2, ..., place_n)}
        '''
        self.write_info(f'加载{filepath}')
        df = read_excel(filepath)
        n = []
        for c_name in df.columns:
            if valid_column(c_name):
                n.append(c_name)
        place = list(df[n].apply(tuple, axis=1))
        com2place = dict(zip(list(df['公司']), place))
        self.write_info('完成')
        return com2place

    def filter_invalid_url(self, place2url):
        '''
        remove invalid url
        an invalid url is 
        1. chinese or
        2. empty or
        3. too short in length (<2)
        '''
        new_place2url = copy.deepcopy(place2url)
        for place in place2url:
            for typename in place2url[place]:
                if type(place2url[place][typename]) != str:
                    new_place2url[place].pop(typename)
                elif is_chinese(place2url[place][typename]) or len(place2url[place][typename]) < 2:
                    new_place2url[place].pop(typename)
        return new_place2url

    def load_url_data(self, filepath):
        # {地区:{类别:url}}
        self.write_info(f'加载{filepath}')
        place2url = {}
        urldf = read_excel(filepath)
        for item in urldf.iterrows():
            place2url[item[1]['地区']] = dict(zip(list(item[1].keys())[1:], list(item[1][1:])))

        place2url = self.filter_invalid_url(place2url)

        self.write_info('完成')
        return place2url

    def fetch_type_url_dic(self, place):
        url_dic = self.place2url[place]
        return url_dic

    def process(self, company_path, url_path, outfile):
        try:
            self.com2place = self.load_company_data(company_path)
            # return
            self.place2url = self.load_url_data(url_path)
            d = {'filename':[], 'url':[]}
            for com in self.com2place:
                for place in self.com2place[com]:
                    type2url = self.fetch_type_url_dic(place)
                    for typename in type2url:
                        url = type2url[typename].replace(self.text_to_replace, com)
                        d['filename'].append('{}-{}-{}'.format(com, place, typename))
                        d['url'].append(url)
            #outfile = os.path.join(outdir, filename)+'.txt'
            data = DataFrame(d)
            data.to_excel(outfile, index=False)
            self.write_info('完成，生成文件：{}'.format(outfile))
            return (True, '')
        except Exception as e:
            return (False, str(e))



# %%
if __name__ == '__main__':
    #a = 1
    g = UrlGenerator()
    g.process('company.xlsx', 'url_list.xlsx', 'out_url.txt')