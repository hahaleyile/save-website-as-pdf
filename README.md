# 自动公开核查-网页自动转存pdf
- [自动公开核查-网页自动转存pdf](#自动公开核查-网页自动转存pdf)
  - [项目背景](#项目背景)
  - [python安装及相关依赖包安装](#python安装及相关依赖包安装)
  - [程序说明](#程序说明)
  - [程序使用方法](#程序使用方法)
    - [1. 准备输入文件](#1-准备输入文件)
    - [2. 修改json配置文件（可选）](#2-修改json配置文件可选)
    - [3. 开始使用](#3-开始使用)
  - [特别注意](#特别注意)
  - [Contributing](#contributing)

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

## 程序说明
```
- main.py              # 程序主入口文件
- config.json          # 配置文件
- src
  - LogWriter.py
  - pdf_saver.py
  - url_generator.py
  - untitled.ui        # QT UI设计文件
  - qt.py              # 生成的QT UI 代码
- data
  - rawdata            # 文件示例
    - company.xlsx
    - out_url.xlsx
    - url_list.xlsx
    - fail_url.txt
  - xxx.pdf            # 保存的pdf样例
```

## 程序使用方法
### 1. 准备输入文件
- 包含公司和省市（区）信息的excel
  - 参考company.xlsx格式
  - 第一行标题必须包含`公司`, 从1开始到n的`数字`
  - 1-n的`数字`表达了公司地理位置的层级，比如1表示省，2表示市，3表示区

- 包含核查类别以及对应省市（区）的查询网址excel
  - 参考url_list.xlsx
  - 第一行是核查类别，第一列是省市（区）的名称
  - 对应的单元格中填写url网址
    - 其中url格式遵守如下：
      - 假设该类别该机构的相关信息需要在江苏省工商局网站进行搜索，进入江苏省工商局，搜索“哈哈”，得到网页url:http://www.jiangsu.gov.cn/jrobot/search.do?q=%E5%93%88%E5%93%88&pg=10&p=1&tpl=2&category=&webid=79&x=0&y=0
      - 定位“哈哈”在url中出现的位置，将其替换为{}，上例中替换之后结果为http://www.jiangsu.gov.cn/jrobot/search.do?q={}&pg=10&p=1&tpl=2&category=&webid=79&x=0&y=0，将该结果填入对应单元格中
      - 也可以不用{}，替换成别的内容，但要注意**有一定区分度，不能是常见的字母组合（比如http这种）**
  - 没有符合条件的url的单元格空着即可
- **注意，company.xlsx 和 url_lis.xlsx 的省市区名称应当完全对应，比如统一写“江西省”或“江西”**
- **程序默认没有同名市（区）**

### 2. 修改json配置文件（可选）
- 主目录下的`config.json`参数及其含义如下
```
{
    "log_path": "./log/log.txt",        # 日志保存地址
    "thread_num": 4,                    # 线程数量，一般4-8比较合适，一般情况下线程数越大越快
    "default_data_dir": "./data",       # 默认的数据文件夹，可以修改成自己的数据存放文件夹
    "text_to_replace": "{}"             # url中被替换的文本，默认是{}，可根据你的url_list.xlsx中的替换情况更改
}
```

### 3. 开始使用
- 运行`python main.py`
![image](https://github.com/cyl628/save-website-as-pdf/blob/main/figure/mainwindow.png)
- `生成url列表`，选择你的文件，点击按钮，右侧日志出现生成完毕即可在你指定的位置查看
  - 示例生成文件：out_url.xlsx
- `自动保存pdf`，选择刚刚生成的文件并指定pdf保存位置（文件夹）和`失败的url保存文件`，点击按钮开始
  - 右侧日志会在每成功保存10个时显示当前进度
  - 可以点击`取消`按钮提前取消（此时未处理和处理失败的url都会出现在指定的`失败的url保存文件`中）
  - `失败的url保存文件`示例：fail_url.txt
  - **完成一次生成后（或生成了一部分提前终止后），可以在`失败的url保存文件`基础上再重新开始，操作方法是将`失败的url保存文件`当作之前的out_url.xlsx使用即可**

## 特别注意
- 务必手工检查程序输出结果，部分pdf会出现空白情况，一般可以从pdf文件大小看出（此类文件都特别小），这种网页需要手动重新保存
- 第二步中，如果提前取消任务，等到所有线程都停止时再关闭主页面，同理任务运行完毕的标志是所有线程都运行完毕

![image](https://github.com/cyl628/save-website-as-pdf/blob/main/figure/logwindow1.png)
![image](https://github.com/cyl628/save-website-as-pdf/blob/main/figure/logwindow2.png)

## Contributing
