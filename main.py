from PyQt5.QtCore import QThread
from src.LogWriter import LogWriter
from src.qt import Ui_MainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal
import os, sys
from src.url_generator import UrlGenerator
from src.pdf_saver import PDFSaver
from func_timeout import FunctionTimedOut
from pandas import read_excel
from typing import List
import json

class PDFGenerateThread(QThread):
    show_info = pyqtSignal(str, bool)
    update_info = pyqtSignal(list)   # 定义信号
    fail_item = pyqtSignal(str)
    def __init__(self, filename_url_data, index, pdf_savedir, pdf_saver):
        super().__init__()
        self.data = filename_url_data
        self.stop_ = False
        self.index = index
        self.pdf_savedir = pdf_savedir
        self.pdf_saver = pdf_saver

    def run(self):
        for i, (filename, url) in enumerate(self.data):
            if self.stop_:
                # return all those not processed data
                self.fail_item.emit('\n'.join(['\t'.join(d) for d in self.data[i:]]))
                self.show_info.emit('线程{}已停止'.format(self.index), True)
                return

            pdfpath = os.path.join(self.pdf_savedir, filename)+'.pdf'
            if os.path.exists(pdfpath):
                self.update_info.emit(['success', 1])
                # success += 1
            else:
                urlitem = filename + '\t' + url
                try:
                    self.pdf_saver.print_topdf(url, pdfpath)
                    # self.write_info('完成:'+url, to_user=False)
                    self.show_info.emit('完成:'+url, False)
                    if (os.stat(pdfpath).st_size / 1024) > 50:
                        self.update_info.emit(['success', 1])
                        # success += 1
                    else:
                        os.remove(pdfpath)
                        self.fail_item.emit(urlitem)
                        # with open(fail_url_savepath, 'a+', encoding='utf-8')as f:
                        #     f.writelines(urlitem)
                except FunctionTimedOut as e:
                # except Exception:
                    # self.write_info('超时:'+url, to_user=False)
                    # with open(fail_url_savepath, 'a+', encoding='utf-8')as f:
                    #     f.writelines(urlitem)
                    self.show_info.emit('超时:'+url, False)
                    self.fail_item.emit(urlitem)
                except KeyboardInterrupt:
                    return
                except Exception as e:
                    self.show_info.emit(str(e), False)
                    # self.write_info('失败:'+url, to_user=False)
                    # with open(fail_url_savepath, 'a+', encoding='utf-8')as f:
                    #     f.writelines(urlitem)
                    self.show_info.emit('失败:'+url, False)
                    self.fail_item.emit(urlitem)
                
                if os.path.exists(pdfpath) and (os.stat(pdfpath).st_size / 1024) <= 50:
                    os.remove(pdfpath)
                    self.fail_item.emit(urlitem)
        self.show_info.emit('线程{}运行完毕'.format(self.index), True)
        return

        


class MyMainWindow(QMainWindow, Ui_MainWindow):  
    def __init__(self, MainWindow, config):
        super(MyMainWindow, self).__init__(MainWindow)
        self.setupUi(MainWindow)
        self.logwriter = LogWriter(config['log_path'], self.log_content)
        self.urlgenerator = UrlGenerator(self.logwriter, config['text_to_replace'])
        self.pdf_saver = PDFSaver(logwriter=self.logwriter)
        self.bind_action()
        self.default_dir = config['default_data_dir']
        self.thread_num = config['thread_num']
    
    def write_info(self, info, to_user=True):
        if self.logwriter is not None:
            self.logwriter.write(info, to_user=to_user)

    # open window to choose existing file
    def get_file(self, default_dir, widget, filetype):
        fileName, _ = QFileDialog.getOpenFileName(self, "选取文件", default_dir, filetype)
        if fileName:
            widget.setText(fileName)
        return
    
    def get_dir(self, default_dir, widget):
        directory = QFileDialog.getExistingDirectory(self, '选取文件夹', default_dir)
        if directory:
            widget.setText(directory)

    def get_company_file(self):
        self.get_file(self.default_dir, self.company_file, 'EXCEL(*.xlsx;*.xls)')

    def get_base_url_file(self):
        self.get_file(self.default_dir, self.base_url_infile, 'EXCEL(*.xlsx;*.xls)')

    def get_url_list_infile(self):
        self.get_file(self.default_dir, self.url_list_infile, 'File(*.xlsx;*.txt)')

    def get_pdf_savepath(self):
        self.get_dir(self.default_dir, self.pdf_save_dir)

    # set file save path
    def set_excel_save_path(self, default_dir, default_name,  widget):
        filename, _ = QFileDialog.getSaveFileName(None, '选择保存路径', os.path.join(default_dir, default_name), 'excel(*.xlsx)')
        widget.setText(filename)

    def set_txt_save_path(self, default_dir, default_name,  widget):
        filename, _ = QFileDialog.getSaveFileName(None, '选择保存路径', os.path.join(default_dir, default_name), 'TXT(*.txt)')
        widget.setText(filename)

    def set_url_list_outfile(self):
        self.set_excel_save_path(self.default_dir, 'out_url.xlsx', self.url_list_outfile)

    def set_fail_url_outpath(self):
        self.set_txt_save_path(self.default_dir, 'fail_url.txt', self.fail_url_outfile)

    def handle_status(self, status):
        if not status[0]:
            self.write_info(status[1])
            QMessageBox.critical(self, 'failure', '失败，请确认输入文件格式正确，请查看log日志并联系开发者')

    def generate_urls(self):
        if not (self.company_file.text() and self.base_url_infile.text() and self.url_list_outfile.text()):
            QMessageBox.information(self, 'warning', '请选择相应的输入和输出文件！')
            return
        status = self.urlgenerator.process(str(self.company_file.text()), str(self.base_url_infile.text()), str(self.url_list_outfile.text()))
        self.handle_status(status)

    def generate_pdf(self):
        if not (self.url_list_infile.text() and self.pdf_save_dir.text() and self.fail_url_outfile.text()):
            QMessageBox.information(self, 'warning', '请选择相应的输入和输出文件！')
            return

        # get file path
        filepath = str(self.url_list_infile.text())
        pdf_savedir = str(self.pdf_save_dir.text())
        self.fail_url_savepath = str(self.fail_url_outfile.text())

        # necessary start param
        self.click_start()

        # read file
        if filepath.endswith('txt'):
            with open(filepath, encoding='utf-8')as f:
                lines = f.readlines()
                data = list(map(lambda x:x.strip().split('\t'), lines))
        else:
            data = read_excel(filepath)
            data = list(zip(data['filename'], data['url']))

        self.write_info('开始')
        # i= 0
        thread_num = self.thread_num
        chunk_size = int(len(data) / thread_num)
        if len(data) - chunk_size * thread_num > 0:
            chunk_size += 1
        for i in range(thread_num):
            new_thread = PDFGenerateThread(data[i*chunk_size:(i+1)*chunk_size], i, pdf_savedir, self.pdf_saver)
            new_thread.fail_item.connect(self.handle_fail_item)
            new_thread.update_info.connect(self.handle_update_info)
            new_thread.show_info.connect(self.handle_show_info)
            new_thread.start()
            self.write_info('线程{}启动'.format(i))
            self.thread_list.append(new_thread)
    
    def handle_fail_item(self, urlitem):
        with open(self.fail_url_savepath, 'a+', encoding='utf-8')as f:
            f.writelines(urlitem + '\n')
    
    def handle_show_info(self, info: str, to_user: bool):
        self.write_info(info, to_user=to_user)

    def handle_update_info(self, info: List):
        if info[0] == 'success':
            self.success += info[1]
            if self.success % 10 == 0:
                self.write_info('已完成{}个'.format(self.success))

    def click_stop(self):
        for thread in self.thread_list:
            thread.stop_ = True
        self.stop.setEnabled(False)
        self.save_pdf.setEnabled(True)
        QApplication.processEvents()
    
    def click_start(self):
        self.save_pdf.setEnabled(False)
        self.stop.setEnabled(True)
        self.success = 0
        self.thread_list = []

        if os.path.exists(self.fail_url_savepath):
            os.remove(self.fail_url_savepath)

    def reset_log_content(self):
        self.log_content.clear()

    def bind_action(self):
        self.choose_company_file.clicked.connect(self.get_company_file)
        self.choose_base_url_file.clicked.connect(self.get_base_url_file)
        self.choose_url_list_outdir.clicked.connect(self.set_url_list_outfile)
        self.generate_url_list.clicked.connect(self.generate_urls)

        self.choose_url_list_infile.clicked.connect(self.get_url_list_infile)
        self.choose_fail_url_outpath.clicked.connect(self.set_fail_url_outpath)
        self.choose_pdf_savedir.clicked.connect(self.get_pdf_savepath)
        self.save_pdf.clicked.connect(self.generate_pdf)

        self.clear_log.clicked.connect(self.reset_log_content)

        self.stop.clicked.connect(self.click_stop)
# %%
if __name__ == '__main__':
    with open('./config.json')as f:
        config = json.loads(f.read())
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = MyMainWindow(MainWindow, config)
    MainWindow.show()
    sys.exit(app.exec_())
# %%
