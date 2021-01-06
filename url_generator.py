'''
this file generate all urls to be saved as pdf file
input:
a table of companies and locations, with form:
    xxx公司   xx省;xx市
a table of base url for each location and each website
'''


# %%
import pandas as pd
import pickle

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

print('读入机构列表...')
df = pd.read_csv('company.txt', sep='\t')
com2addr = dict(zip(list(df['公司']), list(df['省市'])))
len(com2addr)
# %%
#生成字典 {xx公司:[xx省, xx市]}
com2addr_new = {}
for com in com2addr:
    l =  com2addr[com].split(';')
    l_new = []
    l_new.append(l[0][:3])
    if '赣江' in l[1]:
        l_new.append('赣江新区')
    else:
        l_new.append(l[1][:3])
    com2addr_new[com] = l_new
print('一共{}个机构'.format(len(com2addr_new)))
with open('com2addr.pkl', 'wb')as f:
    pickle.dump(com2addr_new, f)
print('完成')

print('读入url列表...')
# %%
#生成字典 {xx省:{工商:base_url, 国土:base_url, ...}}
urldic = {}
urldf = pd.read_csv('url_list.txt', sep='\t')
for item in urldf.iterrows():
    #print(type(item[1]))
    urldic[item[1]['省市']] = dict(zip(list(item[1].keys())[1:], list(item[1][1:])))
print('一共{}个省市'.format(len(urldic)))
print('完成')

# %%
#生成最终列表
#九江银行股份有限公司-江西省-工商  url
print('生成url列表...')
with open('com2addr.pkl', 'rb')as f:
    com2addr = pickle.load(f)
linestowrite = []
for com in com2addr:
    for addr in com2addr[com]:
        urls = urldic[addr]
        for typename in urls:
            if str(urls[typename]).startswith('http') and not is_chinese(str(urls[typename])):
                url = urls[typename].replace('{}', com)
                linestowrite.append('{}-{}-{}\t{}'.format(com, addr, typename, url))
with open('htmlpdf_url.txt', 'w', encoding='utf-8')as f:
    f.writelines('\n'.join(linestowrite))
print('完成，生成文件：{}'.format('htmlpdf_url.txt'))
# %%
