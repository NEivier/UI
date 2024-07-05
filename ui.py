import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QDesktopWidget, \
    QHBoxLayout, QVBoxLayout, QGroupBox, QCalendarWidget, QTextEdit, QGridLayout
from PyQt5.QtCore import QDate, QTimer, Qt, QDateTime, QRect
from PyQt5.QtGui import QIcon, QFont
from weatherfetch import fetch_weather

import Adafruit_DHT
import RPi.GPIO as GPIO

class MyWindow(QWidget):
    def __init__(self):  # 调用父类的init方法
        global prompt_str
        super().__init__()
        # 调整窗口在屏幕的中央，同时获取屏幕的信息
        self.center_pointer = QDesktopWidget().availableGeometry().center()  # 获取当前屏幕的可用区域，得到的是屏幕中心点的坐标
        self.width = 2 * self.center_pointer.x()  # 得到中心点坐标的x
        self.height = 2 * self.center_pointer.y()  # 得到中心点坐标的y
        # old_x, old_y, width, height, = w.frameGeometry().getRect()  # getRect得到的是当前窗口的位置和大小信息，是一个元组，则对元组进行拆包
        # w.move(x - width // 2, y - height // 2)
        self.resize(self.width, self.height)
        self.move(0, 0)  # 窗口铺满整个屏幕
        self.main_layout = QVBoxLayout()  # 最外层的垂直布局器

        self.temperature=0
        self.humidity=0
        
        # 创建时间日期显示区域
        self.date_label = QLabel()  # 显示日期的标签控件
        self.time_label = QLabel()  # 显示时间的标签控件
        date_font = self.date_label.font()
        date_font.setPointSize(36) 
        self.date_label.setFont(date_font)  # 设置日期标签的字体大小为 36
        time_font = self.time_label.font()
        time_font.setPointSize(36)
        self.time_label.setFont(time_font)   # 设置时间标签的字体大小为 36
        self.update_time_label()  # 调用方法，更新日期和时间
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time_label)
        self.timer.start(1000)  # 每秒刷新一次
        self.date_label.setAlignment(Qt.AlignCenter)  # 文本居中
        self.time_label.setAlignment(Qt.AlignCenter)  # 文本居中
        self.time_box = QGroupBox()  # 创建时间显示组
        self.time_box_layout = QVBoxLayout()  # 创建时间组的垂直布局
        self.time_box_layout.addWidget(self.time_label)  # 布局中添加时间文本控件
        self.time_box_layout.addWidget(self.date_label)  # 布局中添加日期文本控件
        self.time_box.setLayout(self.time_box_layout)  # 将布局应用在当前组

        #创建温度湿度显示区域
        self.get_tem_hmd()  # 调用方法，更新温湿度
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.get_tem_hmd)
        self.timer.start(1000)  # 每秒刷新一次
        #self.temperature_text = QTextEdit('温度:{0:0.1f}°C'.format(self.temperature))
        #self.temperature_text.setReadOnly(True)#待添加方法
        #temperature_font = self.temperature_text.font()
        #temperature_font.setPointSize(12)
        #self.temperature_text.setFont(temperature_font)
        #self.temperature_text.setAlignment(Qt.AlignCenter)
        #self.humidity_text = QTextEdit('湿度:{0:0.1f}'.format(self.humidity))
        #self.humidity_text.setReadOnly(True)
        #humidity_font = self.humidity_text.font()
        #humidity_font.setPointSize(12)
        #self.humidity_text.setFont(humidity_font)
        #self.humidity_text.setAlignment(Qt.AlignCenter)
        #self.refresh_btn = QPushButton('刷新')#待删除
        #refresh_btn_font = self.refresh_btn.font()
        #refresh_btn_font.setPointSize(12)
        #self.refresh_btn.setFont(refresh_btn_font)
        #
        #self.temperature_box_0 = QGroupBox()
        #self.temperature_box_0_layout = QHBoxLayout()
        #self.temperature_box_0_layout.addWidget(self.temperature_text)
        #self.temperature_box_0_layout.addWidget(self.humidity_text)
        #self.temperature_box_0.setLayout(self.temperature_box_0_layout)
        #self.temperature_box_all = QGroupBox()
        #self.temperature_box_all_layout = QHBoxLayout()
        #self.temperature_box_all_layout.addWidget(self.refresh_btn)
        #self.temperature_box_all_layout.addWidget(self.temperature_box_0)
        #self.temperature_box_all.setFixedWidth(self.width // 3)
        #self.temperature_box_all.setLayout(self.temperature_box_all_layout)

        # 创建语音功能区域
        self.start_btn = QPushButton('开始对话')
        start_btn_font = self.start_btn.font()
        start_btn_font.setPointSize(12)
        self.start_btn.setFont(start_btn_font)
        self.end_btn = QPushButton('结束对话')
        end_btn_font = self.end_btn.font()
        end_btn_font.setPointSize(12)
        self.end_btn.setFont(end_btn_font)
        self.voice_box = QGroupBox()
        self.voice_box_layout = QHBoxLayout()
        self.voice_box_layout.addWidget(self.start_btn)
        self.voice_box_layout.addWidget(self.end_btn)
        self.voice_box.setLayout(self.voice_box_layout)

        self.status_label = QLabel()
        self.status_label.setText('成都市郫都区未来一周天气')

        # 创建一个网格布局组
        self.weather_grid = QGroupBox()
        self.weather_layout = QGridLayout()

        # 创建网格布局中的天气信息提示组
        self.label_title = QLabel("日期")
        self.weather_prompt_box = QGroupBox()
        self.weather_prompt_box_layout = QHBoxLayout()
        self.weather_prompt_box_layout.addWidget(self.label_title)
        for k in range(5):
            text0_data = QTextEdit()
            text0_data.setReadOnly(True)
            if k == 0:
                prompt_str = '天气情况'
            elif k == 1:
                prompt_str = '最高温度'
            elif k == 2:
                prompt_str = '最低温度'
            elif k == 3:
                prompt_str = '风向'
            elif k == 4:
                prompt_str = '风力'
            text0_data.setText(prompt_str)
            text0_data.setAlignment(Qt.AlignCenter)
            self.weather_prompt_box_layout.addWidget(text0_data)
        self.weather_prompt_box.setFixedHeight(self.height // 12)
        self.weather_prompt_box.setLayout(self.weather_prompt_box_layout)
        # 完成网格布局剩余部分，显示天气信息
        self.weather_data = fetch_weather()
        for i, data in enumerate(self.weather_data):
            label = QLabel(f"{data[0]}")
            weather0_box = QGroupBox()
            weather0_box_layout = QHBoxLayout()
            for j in range(5):
                text_data = QLabel()
                # text_data.setReadOnly(True)
                data_str = ' '.join(data[j + 1])
                text_data.setText(data_str)
                text_data.setAlignment(Qt.AlignCenter)
                weather0_box_layout.addWidget(text_data)
            weather0_box.setLayout(weather0_box_layout)
            # 这两个for循环将天气信息整理出来，一标签+一个水平布局组显示一天的信息，并将它们逐个添加到网格布局组
            self.weather_layout.addWidget(label, i + 1, 0)
            self.weather_layout.addWidget(weather0_box, i + 1, 1)
        self.weather_layout.addWidget(self.label_title, 0, 0)
        self.weather_layout.addWidget(self.weather_prompt_box, 0, 1)
        self.weather_grid.setLayout(self.weather_layout)  # 将网格布局应用到网格布局组

        # 创建一个水平布局组，组里放下时间布局组、温湿度布局组和语音布局组
        self.level1_box = QGroupBox()
        self.level1_box_layout = QHBoxLayout()
        self.level1_box_layout.addWidget(self.time_box)  # 只有布局才可以添加控件，这里是将一个组看作是一个控件
        self.level1_box_layout.addWidget(self.temperature_box_all)
        self.level1_box_layout.addWidget(self.voice_box)
        self.level1_box.setFixedSize(self.width, self.height // 6)  # 设置水平组的固定大小为上半个屏幕
        self.level1_box.setLayout(self.level1_box_layout)
        # 创建一个垂直布局组，组里放下状态提示文本控件和天气信息显示布局组
        self.vertical_box = QGroupBox()
        self.vertical_box_layout = QVBoxLayout()
        self.vertical_box_layout.addWidget(self.status_label)  # 状态提示栏，成都市郫都区未来一周天气
        self.vertical_box_layout.addWidget(self.weather_grid)  # 垂直布局核心，网格布局组，天气信息显示部分
        self.vertical_box.setLayout(self.vertical_box_layout)  # 将垂直布局应用到垂直布局组

        self.main_layout.addWidget(self.level1_box)
        self.main_layout.addWidget(self.vertical_box)
        self.main_layout.addStretch()
        self.setLayout(self.main_layout)  # 让当前串口按照创建的布局排列

    def update_time_label(self):
        current_datetime = QDateTime.currentDateTime()
        current_date_str = current_datetime.toString("yyyy年MM月dd日")
        current_time_str = current_datetime.toString("hh:mm:ss")
        self.date_label.setText(current_date_str)
        self.time_label.setText(current_time_str)
        
    def get_tem_hmd(self):
        # 温湿度实时获取
        self.sensor = Adafruit_DHT.DHT11 # 设置传感器的型号和引脚
        self.pin = 22
       
        GPIO.setwarnings(False) # 初始化GPIO库
        GPIO.setmode(GPIO.BCM)
       
        self.humidity,self.temperature = Adafruit_DHT.read_retry(self.sensor,self.pin) # 读取传感器数据
        #while True:
        if self.humidity is not None and self.temperature is not None: # ，则输出温湿度数值
                print("湿度={0:0.1f} 温度={1:0.1f}°C".format(self.humidity,self.temperature))
                #self.temperature_text = QTextEdit('温度:{0:0.1f}°C'.format(self.temperature))
                #self.temperature_text.setReadOnly(True)
                #self.humidity_text = QTextEdit('湿度:{0:0.1f}'.format(self.humidity))
                #self.humidity_text.setReadOnly(True)
                self.temperature_text = QTextEdit('温度:{0:0.1f}°C'.format(self.temperature))
                self.temperature_text.setReadOnly(True)#待添加方法
                temperature_font = self.temperature_text.font()
                temperature_font.setPointSize(12)
                self.temperature_text.setFont(temperature_font)
                self.temperature_text.setAlignment(Qt.AlignCenter)
                self.humidity_text = QTextEdit('湿度:{0:0.1f}'.format(self.humidity))
                self.humidity_text.setReadOnly(True)
                humidity_font = self.humidity_text.font()
                humidity_font.setPointSize(12)
                self.humidity_text.setFont(humidity_font)
                self.humidity_text.setAlignment(Qt.AlignCenter)
                self.refresh_btn = QPushButton('刷新')#待删除
                refresh_btn_font = self.refresh_btn.font()
                refresh_btn_font.setPointSize(12)
                self.refresh_btn.setFont(refresh_btn_font)
        
                self.temperature_box_0 = QGroupBox()
                self.temperature_box_0_layout = QHBoxLayout()
                self.temperature_box_0_layout.addWidget(self.temperature_text)
                self.temperature_box_0_layout.addWidget(self.humidity_text)
                self.temperature_box_0.setLayout(self.temperature_box_0_layout)
                self.temperature_box_all = QGroupBox()
                self.temperature_box_all_layout = QHBoxLayout()
                self.temperature_box_all_layout.addWidget(self.refresh_btn)
                self.temperature_box_all_layout.addWidget(self.temperature_box_0)
                self.temperature_box_all.setFixedWidth(self.width // 3)
                self.temperature_box_all.setLayout(self.temperature_box_all_layout)
                
        else:
                print('读取传感器数值失败')

if __name__ == "__main__":
    app = QApplication(sys.argv)  # 创建qpp变量，指向QApplication对象，其中的参数sys.argv指的是运行程序的环境参数，是一个列表
    w = MyWindow()  # 创建一个自己创建的类
    w.show()  # 展示窗口
    
    app.exec_()  # 必有调用exec,相当于死循环使程序一直运行，监测用户是否进行某些操作
