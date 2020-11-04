# 自动公开核查-网页自动转存pdf
## 项目背景
支持各省市工商、国土、外汇、社保、公积金、劳动、中国人民银行、银保监会、中国人民银行地方支行、银保监会地方局对特定机构公开信息搜索页面的pdf文件自动保存

## 安装
- python 3.7
- ```pip install -r requirements.txt```

## 使用方法
- 下载wkhtmltopdf.exe, 放在同一目录下
  - 百度网盘链接：https://pan.baidu.com/s/1K4z5OdLTrn8dJJX0eIanGg 
  - 提取码：1je8 
- 更改覆盖company.txt文件，格式如下（参考company.txt）  
  公司  省市  
  xxx公司 北京市;大兴区  
  ……  
- 更改覆盖url_list.txt文件，格式如下（参考url_list.txt）  
  省市  类别1 类别2 类别3……  
  北京市 url1  url2……  
  大兴区 ……  
- 其中url格式遵守如下：
  - 举例进入江苏省工商局，搜索“哈哈”，得到网页url:http://www.jiangsu.gov.cn/jrobot/search.do?q=%E5%93%88%E5%93%88&pg=10&p=1&tpl=2&category=&webid=79&x=0&y=0
  - 定位“哈哈”在url中出现的位置，将其替换为{}，上例中替换之后结果为http://www.jiangsu.gov.cn/jrobot/search.do?q={}&pg=10&p=1&tpl=2&category=&webid=79&x=0&y=0
- 在cmd中运行如下命令（若最后一个命令长时间不结束，cmd长时间不更新，可以按ctrl+c）  
```
python url_generator.py
python pdf_saver.py
```
- 保存的pdf文件在data文件夹中
- 失败的url在failurl{}.txt中

## Contributing
