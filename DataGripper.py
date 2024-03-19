import csv
import math
import os.path
import sys
import time

import pandas
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from second_page import SecondPage
from PyQt5.QtChart import QChart, QLineSeries, QValueAxis
from PyQt5.QtGui import QIcon

import pandas as pd

Selected_file_name=""

class Mainwin(QWidget):
    chosen_item = list()
    is_checked = bool()
    def __init__(self):
        super().__init__()
        self.second_page = SecondPage()
        self.second_page.setWindowModality(Qt.ApplicationModal)
        self.data_timer = QTimer(self)
        self.init_ui()
        self.last_modify_time = None
        self.timer_count = int()


    def init_ui(self):
        if getattr(sys,'frozen',False):
            bundle_dir=sys._MEIPASS
        else:
            bundle_dir=os.path.dirname(os.path.abspath(__file__))
        self.ui=uic.loadUi(bundle_dir+'./gripper.ui',self)

        # 设置图标及标题
        self.ui.setWindowTitle("DataGripper")
        self.ui.setWindowIcon(QIcon('amd.jpg'))

        # 设置最大化图标
        self.menu_bar=QMenuBar()
        view_menu = self.menu_bar.addMenu('View')
        max_action = QAction('Maximize', self)
        max_action.triggered.connect(self.maximizeWindow)
        view_menu.addAction(max_action)

        # 从ui文件中加载控件
        self.lineedit=self.ui.lineEdit
        self.btn1=self.ui.pushButton
        self.setlog_btn=self.ui.pushButton_2
        self.start_btn=self.ui.pushButton_3
        self.chart_view=self.ui.graphicsView
        self.Exit_button=self.ui.pushButton_4

        # 给按钮绑定槽函数
        self.btn1.clicked.connect(self.get_file) # 绑定槽函数
        self.setlog_btn.clicked.connect(self.second_page.show)
        self.second_page.close_signal.connect(self.events_after_close)
        self.start_btn.clicked.connect(self.collect_data)
        self.Exit_button.clicked.connect(sys.exit)
        self.data_timer.timeout.connect(self.realtime_update)

    def timer_start(self):
        if not self.data_timer.isActive():
            self.data_timer.start(500)

    def maximizeWindow(self):
        # 最大化窗口
        self.showMaximized()

    def get_file(self):
        #实例化QFileDialog
        dig=QFileDialog()
        #设置可以打开任何文件
        dig.setFileMode(QFileDialog.AnyFile)
        #文件过滤
        dig.setFilter(QDir.Files)

        if dig.exec_():
            #接受选中文件的路径，默认为列表
            filenames=dig.selectedFiles()
            #列表中的第一个元素即是文件路径，以只读的方式打开文件
            self.lineedit.setText(filenames[0])
            global Selected_file_name
            Selected_file_name = filenames[0]

            # 将下一个按钮设置为可编辑
            self.setlog_btn.setEnabled(True)


    def events_after_close(self, chosen_items, is_checked):
        self.chosen_item = chosen_items
        print("chosen_item=",chosen_items)
        self.is_checked = is_checked
        self.start_btn.setEnabled(True)


    def collect_data(self):
        print("enter collect_data")

        if self.check_columns() == True:
            try:
                data = pd.read_csv(Selected_file_name, usecols=self.chosen_item)
            except Exception as e:
                print("Error: Selected column were not found in file", e)

            # 保存为新的 CSV 文件
            try:
                new_file_path=os.path.dirname(Selected_file_name)
                if self.is_checked:
                    file_name,suffix=os.path.splitext(Selected_file_name)
                    new_file_name=os.path.join(new_file_path,os.path.basename(file_name + "_" + str(int(time.time())) + suffix))
                    data.to_csv(new_file_name, index=False)
                    print("CSV file saved successfully.")
            except Exception as e:
                print("Error: File export error", e)

            # 将列表中的字符串值转换成数字
            new_data=self.convert_data(data)
            # print("new_data=",new_data)

            self.chart_window(new_data,self.chosen_item)

            self.timer_start()

    def realtime_update(self):
        file_time = os.path.getmtime(Selected_file_name)
        if file_time != self.last_modify_time:
            self.collect_data()
            self.last_modify_time = file_time
        else:
            self.timer_count +=1
            if self.timer_count >= 100:
                self.data_timer.stop()

    def check_columns(self):
        # 查看所选列名是否存在
        df=pandas.read_csv(Selected_file_name,header=0)
        set_columns=set(df.columns.tolist())
        set_chosen_item=set(self.chosen_item)
        print(f"set_columns={set_columns}\n,set_item={set_chosen_item}")
        if set_chosen_item.issubset(set_columns):
            return True
        else:
            outrange_columns=set()
            for item in set_chosen_item:
                if item not in set_columns:
                    outrange_columns.add(item)

            print("err_column=",outrange_columns)
            self.message_dialog(outrange_columns)
            return False

    def message_dialog(self,err_list):
        # app = QApplication(sys.argv)
        msg_box = QMessageBox(QMessageBox.Warning, 'Warning', f'{err_list} are not found in file {Selected_file_name}, Please check the file.')
        # app.setWindowIcon(msg_box.exec_())
        msg_box.exec_()

    def get_max_data(self,data):
        max_value=float
        if data.shape[1]>1:
            max_values = data.max()

            max_value=max(max_values)
        else:
            max_value = data.iloc[:,0].max()


        return max_value

    def convert_data(self,data):
        conv_item="CPU0 MISC Power Source"
        if conv_item in data.columns.tolist():
            conv_value=data[conv_item]

            data[conv_item]=[1 if item.strip() == 'AC' else (0 if item.strip() == 'DC' else item) for item in conv_value]
            # print("after_convert=",data[conv_item])

        return data



    def chart_window(self,data,column_list):
        print(1111111111111111111111111)

        chart = QChart()  # 创建 chart
        # chart.setTitle("简单函数曲线")
        axis_x = QValueAxis()
        axis_y = QValueAxis()
        axis_x.setTickCount(20)
        axis_y.setTickCount(8)

        max_y=self.get_max_data(data)
        axis_x.setRange(0,data.shape[0]+data.shape[0]/10)
        axis_y.setRange(0,math.ceil(max_y+max_y/10))


        self.chart_view.setChart(chart)  # chart添加到chartView
        # self.setCentralWidget(self.chart_view)

        for item in column_list:
            print(2222222222222222222222)
            self.build_chart(data[item],chart,data.shape[0],item,axis_x,axis_y)


    def build_chart(self,data,chart,rows,column_value,axis_x,axis_y):
        print("start function build_chart")
        # print(f"data={data},chart={chart},rows={rows},column_value={column_value}")

        # 创建曲线序列

        # chart.setAnimationOptions(QChart.SeriesAnimations)
        # chart.legend().hide()
        series = QLineSeries()
        series.setName(column_value)

        # 序列添加数值
        for i in range(rows):
            y_value=data.iloc[i]
            series.append(i,y_value)

        chart.addSeries(series)
        ##创建坐标轴
        # axis_x= QValueAxis()  # x轴
        axis_x.setLabelFormat("%d")
        # axis_x.setRange(0,rows)
        # axis_x.setTitleText("x")
        # chart.addAxis(axis_x, Qt.AlignBottom)
        # series.attachAxis(axis_x)

        # axis_y = QValueAxis()
        axis_y.setLabelFormat("%.2f")
        # axis_y.setMin(0)
        # axis_y.setTitleText(column_value)
        # chart.addAxis(axis_y, Qt.AlignLeft)
        # series.attachAxis(axis_y)

        ##为序列设置坐标轴
        chart.setAxisX(axis_x, series)  # 为序列series0设置坐标轴
        chart.setAxisY(axis_y, series)




if __name__ == '__main__':
    app=QApplication(sys.argv)

    w=Mainwin()

    # 展示窗口
    w.ui.show()

    app.exec()
