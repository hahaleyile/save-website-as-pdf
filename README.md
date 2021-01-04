# 自动公开核查-网页自动转存pdf
## 项目背景
支持各省市工商、国土、外汇、社保、公积金、劳动、中国人民银行、银保监会、中国人民银行地方支行、银保监会地方局对特定机构公开信息搜索页面的pdf文件自动保存，并在保存的pdf上加入保存时间

## python安装及相关依赖包安装
- python3
  - 安装教程详见 
    - windows: https://blog.csdn.net/qq_25814003/article/details/80609729
    - mac: https://www.runoob.com/note/52675
- python安装完成后在该文件夹下打开命令行输入 `pip install -r requirements.txt` 完成安装
  - 关于如何在特定文件夹打开命令行
    - windows: https://blog.csdn.net/sinat_32238399/article/details/85927822
    - mac: https://www.jianshu.com/p/3e1b5fe48952

## 目录文件说明
- company.txt & url_list.txt
  输入文件示例，需要替换成自己需要的内容
- pdf_saver.py
  将网页保存成pdf的代码
- url_generator.py
  根据输入生成url地址的代码

## 程序使用方法
- 下载wkhtmltopdf.exe, 放在同一目录下
  - 百度网盘链接：https://pan.baidu.com/s/1K4z5OdLTrn8dJJX0eIanGg 
  - 提取码：1je8 
- 修改输入文件
  - 更改覆盖company.txt文件，格式如下（每一项之间用tab制表符分隔，参考company.txt）  
    公司  省市  
    xxx公司 北京市;大兴区  
    ……  
  - 更改覆盖url_list.txt文件，格式如下（每一项之间用tab制表符分隔，参考url_list.txt）  
    省市  类别1 类别2 类别3……  
    北京市 url1  url2……  
    大兴区 ……  
    - 其中url格式遵守如下：
      - 假设该类别该机构的相关信息需要在江苏省工商局网站进行搜索，进入江苏省工商局，搜索“哈哈”，得到网页url:http://www.jiangsu.gov.cn/jrobot/search.do?q=%E5%93%88%E5%93%88&pg=10&p=1&tpl=2&category=&webid=79&x=0&y=0
      - 定位“哈哈”在url中出现的位置，将其替换为{}，上例中替换之后结果为http://www.jiangsu.gov.cn/jrobot/search.do?q={}&pg=10&p=1&tpl=2&category=&webid=79&x=0&y=0，将该结果填入url_list.txt的对应位置
  - **输入文件每一列用tab制表符分隔，可以直接从excel文件中复制粘贴到txt文本文件**
  - **比如将`九江银行-分支机构&村镇银行行政处罚统计表.xls`中的公司、省市两列选中复制粘贴到文本文件中即可获得company.txt相同格式的文本，url_list.txt同样可以通过excel表格复制粘贴生成**

- 在该文件夹下打开命令行输入如下命令，生成pdf
  - 这里有个暂时未解决的bug，第二个命令可能会长时间卡住不动，时间过长可以按ctrl+c强制退出）  
```
python url_generator.py
python pdf_saver.py
```
- 保存的pdf文件在data文件夹中，按照`公司/类别/xxxxx.pdf`目录结构分类放置
- 失败的url在failurl{}.txt中

## 特别注意
- 务必手工检查程序输出结果，部分pdf会出现空白情况，一般可以从pdf文件大小看出（此类文件都特别小），这种网页需要手动重新保存
- `htmlpdf_url.txt`是一个包含了所有需要保存的网页网址的文件，由程序根据输入自动生成，后期手动保存时可以用来提高效率

## Contributing
