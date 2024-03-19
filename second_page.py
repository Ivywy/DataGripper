
import sys
import time
import importlib

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *

import config
importlib.reload(config)
from config import DefaultConfig

class SecondPage(QWidget):
    close_signal = pyqtSignal(list, bool)
    chosen_button = list()

    def __init__(self):
        super(SecondPage, self).__init__()
        self.setWindowTitle("DataGripper")

        self.check_button = QRadioButton()
        self.check_button.setText("Export data to file(*.csv)")
        ok_button = QPushButton('ok')
        cancel_button = QPushButton('cancel')

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.check_button)
        hbox.addWidget(ok_button)
        hbox.addWidget(cancel_button)

        ok_button.clicked.connect(self.close)
        cancel_button.clicked.connect(self.cancel_btn_choose)

        opt = DefaultConfig()
        self.buttons = opt.items
        self.q_buttons = []


        # 垂直布局排列第二个页面的按钮和 OK 按钮
        vbox = QVBoxLayout()    # 作为整体的布局器，包含vboxBtn+hbox
        vscroll_box=QVBoxLayout()
        btnWidget=QWidget()
        btnWidget.setLayout(vscroll_box)

        scrollArea=QScrollArea()
        scrollArea.setEnabled(True)
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(btnWidget)

        for button in self.buttons:
            q_button=QPushButton(button)
            q_button.setCheckable(True)
            vscroll_box.addWidget(q_button)
            self.q_buttons.append(q_button)
        vscroll_box.addStretch(1)   # 设置为0就靠上了，这个地方为1，下面也为1的话就是在中间
                            # 记住默认的就在右下就可以理解了

        btnWidget.setLayout(vscroll_box)

        # 在垂直布局中增加几个水平布局
        vbox.addWidget(scrollArea)
        vbox.addLayout(hbox)

        self.setLayout(vbox)


    def chosen_btn(self):
        self.chosen_button.clear()

        for q_btn in self.q_buttons:
            if q_btn.isChecked():
                button=q_btn.text()
                self.chosen_button.append(button)

        return self.chosen_button

    def cancel_btn_choose(self):
        for q_btn in self.q_buttons:
            if q_btn.isChecked():
                q_btn.setChecked(False)



    def closeEvent(self, event):
        # 在关闭窗口前执行一些操作
        chosen_items=self.chosen_btn()
        self.close_signal.emit(chosen_items, self.check_button.isChecked())
        super().closeEvent(event)


    def center(self):
        # 获取屏幕的宽高
        screen_geometry = QApplication.desktop().screenGeometry()

        # 获取第二个页面的宽高
        x = (screen_geometry.width() - self.width()) / 2
        y = (screen_geometry.height() - self.height()) / 2

        # 将第二个页面移到屏幕中间
        self.move(x, y)


