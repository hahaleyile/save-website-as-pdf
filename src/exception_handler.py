import traceback
from PyQt5.QtWidgets import QMessageBox


def catch_except(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            error_info = traceback.format_exc()
            # print(error_info)
            msg_box = QMessageBox(QMessageBox.Warning, f"函数{func.__name__}发生错误", error_info)
            msg_box.show()
            msg_box.exec_()
            return "error"
    return wrapper