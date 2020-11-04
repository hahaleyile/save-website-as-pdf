  
  
import pdfkit  
import requests  
import datetime 
import eventlet
import time
import os
from multiprocessing import  Process

path_wkthmltopdf = r'wkhtmltopdf.exe'
#path_wkthmltopdf = r'/usr/local/bin/wkhtmltopdf'
config = pdfkit.configuration(wkhtmltopdf = path_wkthmltopdf)

def main(urlitemlist, index):
    print('进程{}启动'.format(index))
    failurl = []
    for urlitem in urlitemlist:
        l = urlitem.strip().split('\t')
        filename = l[0]
        filename_list = filename.split('-')
        url = l[1]
        dirname = './data/'+'/'.join([filename_list[0], filename_list[2]])
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        eventlet.monkey_patch()
        try:
            with eventlet.Timeout(30, True):
                print_topdf(url, filename, dirname)
        except: #eventlet.timeout.Timeout:
            print('[FAIL]:', urlitem)
            failurl.append(urlitem)
    with open('failurl{}.txt'.format(index), 'w')as f:
        f.writelines(''.join(failurl))
    print('进程{}完成'.format(index))

def print_topdf(url, filename, dirname):
    curr_time = datetime.datetime.now().date()
    date = curr_time.strftime("%Y/%m/%d") 
    #print(date)
    options = {
        'page-size': 'A4',
        'margin-top': '10mm',
        'margin-right': '10mm',
        'margin-bottom': '10mm',
        'margin-left': '10mm',
        'encoding': "UTF-8",
        'no-outline': None,
        'header-left':date,
        'header-font-size':12,
        'lowquality':''
    }
    pdfpath = os.path.join(dirname, filename)+'.pdf'
    pdfkit.from_url(url, pdfpath, options = options, configuration = config)

if __name__ == '__main__': 
    with open('htmlpdf_url.txt', encoding='utf-8')as f:
        lines = f.readlines()
    #lines = lines[:20]
    num = int(len(lines) / 8) + 1
    process_list = []
    for i in range(8):  #开启5个子进程执行fun1函数
        p = Process(target=main,args=(lines[i*num:(i+1)*num], i, )) #实例化进程对象
        p.start()
        process_list.append(p)
    for i in process_list:
        p.join()

    print('结束')
