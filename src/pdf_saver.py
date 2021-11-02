  
# %%
import pdfkit 
from datetime import datetime
from multiprocessing import Process
import multiprocessing
from func_timeout import func_set_timeout

multiprocessing.freeze_support()

class PDFSaver:
    def __init__(self, path_wkthmltopdf='wkhtmltopdf.exe', logwriter=None):
        self.logwriter = logwriter
        self.config = pdfkit.configuration(wkhtmltopdf = path_wkthmltopdf)
    
    def log_time(func):
        def make_decorater(self, *args, **kwargs):  # 接受调用语句的实参，在下面传递给被装饰函数（原函数）
            return func_set_timeout(self.wait_second)  # 因为被装饰函数里有return，所以需要给调用语句（test（2））一个返回，又因为test_func = func(*args,**kwargs)已经调用了被装饰函数，这里就不用带（）调用了，区别在于运行顺序的不同。
        return make_decorater

    def write_info(self, info, to_user=True):
        print(info)
        if self.logwriter is not None:
            self.logwriter.write(info, to_user=to_user)

    @func_set_timeout(10)
    def print_topdf(self, url, pdfpath):
        curr_time = datetime.now().date()
        date = curr_time.strftime("%Y/%m/%d")
        header_text = str(date) + '\n' + url
        #print(date)
        options = {
            'page-size': 'A4',
            'margin-top': '10mm',
            'margin-right': '10mm',
            'margin-bottom': '10mm',
            'margin-left': '10mm',
            'encoding': "UTF-8",
            'no-outline': None,
            'header-left':header_text,
            'header-spacing': '5',
            'header-font-size':8,
            'lowquality':'',
            'quiet': ''
        }
        pdfkit.from_url(url, pdfpath, options = options, configuration = self.config)
# %%
if __name__ == '__main__': 
    saver = PDFSaver()
    saver.process('test_url.txt', 'data', 'fail_url.txt')

    print('结束')

# %%
