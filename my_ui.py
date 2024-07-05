import sys
import time
from tkinter import font

import lunardate
import FestivalTable
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QDesktopWidget, \
    QHBoxLayout, QVBoxLayout, QGroupBox, QCalendarWidget, QTextEdit, QGridLayout, QMenu, QAction, QToolBar, QMainWindow, \
    QScrollArea
from PyQt5.QtCore import QDate, QTimer, Qt, QDateTime, QRect
from PyQt5.QtGui import QIcon, QFont, QPalette, QBrush, QPixmap
from weatherfetch import fetch_weather
from VirtualKeyboard import VirtualKeyboard
from sensor_tmp_hmd import get_tmp_hmd

class MyWindow(QWidget):
    def __init__(self):  # 调用父类的init方法
        self.dialog_box = QGroupBox()
        self.virtual_keyboard = None
        super().__init__()
        # 调整窗口在屏幕的中央，同时获取屏幕的信息
        self.center_pointer = QDesktopWidget().availableGeometry().center()  # 获取当前屏幕的可用区域，得到的是屏幕中心点的坐标
        self.width = 2 * self.center_pointer.x()  # 得到中心点坐标的x，则其2倍为屏幕宽
        self.height = 2 * self.center_pointer.y()  # 得到中心点坐标的y，则其2倍为屏幕长
        self.resize(self.width, self.height)
        self.move(0, 0)  # 窗口铺满整个屏幕，移到左上角
        self.main_layout = QVBoxLayout()  # 主布局为垂直布局器
        self.main_layout.setSpacing(1)
        self.virtual_keyboard = VirtualKeyboard(QLineEdit(), 0, 0, 0, 0)
        # 设置窗口背景图片
        palette = self.palette()
        background_image = QPixmap('/home/pi/UI/images/background_1/background.jpg')
        scaled_background = background_image.scaled(self.width, self.height)
        palette.setBrush(QPalette.Background, QBrush(QPixmap('/home/pi/UI/images/background_1/background.jpg')))  # 设置背景图片
        palette.setBrush(QPalette.Background, QBrush(scaled_background))  # 设置背景图片
        self.setPalette(palette)
        self.setAutoFillBackground(True)  # 自动填充背景色

        # 创建时间显示区域
        self.time_label = QLabel()  # 显示日期的标签控件
        self.time_label.setStyleSheet(  # "font-family: 微软雅黑;"
            # "font-size:120px;color:rgb(0,0,0);"
            # "background-color:blue;"  # 修改背景颜色
            "border-image:url(/home/pi/UI/images/background_1/background.jpg);"
            # 如果这里使用background-image的话随着窗口大小的增大会重复的出现很多图片
            "x y z q stretch stretch;"  # 把贴上去的背景图朝四个方向裁剪x y z q的大小
        )  # 设置标签背景
        self.time_label.setWordWrap(True)  # 允许自动换行
        self.update_time_label()  # 调用方法，更新日期和时间
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time_label)
        self.timer.start(1000)  # 每秒刷新一次
        self.time_label.setAlignment(Qt.AlignCenter)  # 文本居中
        self.time_box = QGroupBox()  # 创建时间显示组
        self.time_box_layout = QVBoxLayout()  # 创建时间组的垂直布局
        self.time_box_layout.addWidget(self.time_label)  # 布局中添加时间文本控件
        self.time_box.setLayout(self.time_box_layout)  # 将布局应用在当前组

        # 创建日历
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.setStyleSheet(
            "background-image: url(/home/pi/UI/images/background_1/background1);"
            "x y z q stretch stretch;"  # 把贴上去的背景图朝四个方向裁剪x y z q的大小
        )  # 设置日历背景
        self.calendar.clicked[QDate].connect(self.update_selected_dates)  # 点击可查看任何一天的农历
        # 设置日历字体
        self.calendar_font = QFont()
        self.calendar_font.setFamily("宋体")
        self.calendar_font.setBold(True)
        self.calendar_font.setPointSize(8)
        self.calendar.setFont(self.calendar_font)
        # calendar.setFixedHeight(self.height // 12 + self.height // 6)
        # 显示查看的年份月日
        self.choose_date_label = QLabel(self)
        self.choose_date_label.setFixedHeight(self.height // 28)
        self.choose_date_label.setStyleSheet(
            "color: rgb(0, 0, 0);"
            "border-image:url(/home/pi/UI/images/background_1/background2.jpg);"  # bg5
            "x y z q stretch stretch;"  # 把贴上去的背景图朝四个方向裁剪x y z q的大小
        )  # 设置标签背景
        self.current_date_label()
        self.date_box = QGroupBox()
        self.date_box_layout = QVBoxLayout()  # 设置日历布局为垂直布局
        self.date_box_layout.addWidget(self.calendar)
        self.date_box_layout.addWidget(self.choose_date_label)
        
        # 室内温度显示区，待更新

        self.temperature_label = QLabel()  
        # self.temperature_label.clicked.connect(self.update_temperature)
       # self.temperature_label.setFixedHeight(self.height // 25)
        self.temperature_label.setStyleSheet("color: rgb(0, 0, 0);font-family: Comic Sans MS;font-size:12pt;font-weight: "
                                        "bold;border-image:url(/home/pi/UI/images/background_1/background2.jpg);x y z q stretch "  # bg6
                                        "stretch;")  # 设置标签背景
        # self.temperature_label.setAlignment(Qt.AlignCenter)
        self.date_box_layout.addWidget(self.temperature_label)
        # 室内湿度显示区，待更新
        # self.humidity_label = QLabel()
        # self.humidity_label.clicked.connect(self.update_humidity)
        # self.humidity_label.setFixedHeight(self.height // 25)
        # self.humidity_label.setStyleSheet("color: rgb(0, 0, 0);font-family: Comic Sans MS;font-size:24pt;font-weight: "
                                    # "bold;border-image:url(/home/pi/UI/images/background_1/background1.jpg);x y z q stretch "  # bg4
                                     # "stretch;")
        # self.humidity_label.setAlignment(Qt.AlignCenter)
        # self.date_box_layout.addWidget(self.humidity_label)
        # 温湿度实时显示区
        tmp, hmd = get_tmp_hmd()
        tmp_str = str(tmp)
        hmd_str = str(hmd)
        tmp_text = "室内温度：" + tmp_str + "°C|"+"室内湿度：" + hmd_str + '%'
        self.temperature_label.setText(tmp_text)
        # hmd_str = str(hmd)
        # hmd_text = "   室内湿度：" + hmd_str + '%'
        # self.humidity_label.setText(hmd_text)
        # 定时刷新
        self.timer_tmp_hmd = QTimer()
        self.timer_tmp_hmd.timeout.connect(self.auto_update_tmp_hmd)
        self.timer_tmp_hmd.start(10000) # 10秒更新一次
        # 本地地址标签
        # self.local_site_layout = QHBoxLayout()
        # local_site = QLabel("输入您所在地拼音\n如beijing")
        # local_site.setFixedHeight(self.height // 20)
        # local_site.setStyleSheet("color: rgb(0, 0, 0);font-family: Comic Sans MS;font-size:4pt;font-weight: "
          #                       "bold;border-image:url(/home/pi/UI/images/background_1/background(2).jpg);x y z q stretch stretch;")
        # local_site_layout.addWidget(local_site)
        # 输入城市名
        self.local_site_input = QLineEdit("pidu") # 默认郫都区
        self.local_site_input.setFixedWidth(self.width // 10)
        self.local_site_input.setStyleSheet("color: rgb(0, 0, 0);font-family: 宋体;font-size:10pt;font-weight:bold;")
        self.date_box_layout.addWidget(self.local_site_input)
        # self.local_site_layout.addWidget(self.local_site_input)
        # 查询按钮
        self.search_button = QPushButton("查询")
        self.search_button.setFixedWidth(self.width // 12)
        self.search_button.setStyleSheet("color: rgb(0, 0, 0);font-family: Comic Sans MS;font-size:8pt;font-weight:bold")
        self.search_button.clicked.connect(self.get_weather)  # 添加查询天气的方法
        self.date_box_layout.addWidget(self.search_button)
        # self.local_site_layout.addWidget(self.search_button)
        # self.local_site_layout.setSpacing(1)
        # 将三个控件放入一个组中
        # self.local_site_box = QGroupBox()
        # self.local_site_box.setMinimumSize(18,20)
        # local_site_box.setFixedHeight(self.height // 11)
        #  local_site_box.setFixedHeight(self.height // 10)
        # self.local_site_box.setLayout(self.local_site_layout)
        # self.date_box_layout.addWidget(self.local_site_box)
        # 虚拟键盘
        self.keyboard_button = QPushButton("点击打开键盘")
        self.keyboard_button.setStyleSheet("color: rgb(255, 20, 20);font-family: Comic Sans MS;font-size:8pt;font-weight:"
                                      "bold;border-image:url(/home/pi/UI/images/background_1/background1.jpg);x y z q stretch "
                                      "stretch;")
        self.keyboard_button.clicked.connect(self.show_virtual_keyboard)
        self.date_box_layout.addWidget(self.keyboard_button)
        # self.local_site_layout.addWidget(self.keyboard_button)
        # self.local_site_layout.setSpacing(1)
        # 将三个控件放入一个组中
        self.local_site_box = QGroupBox()
        self.local_site_box.setMinimumSize(12,20)
        self.local_site_box.setFixedHeight(self.height // 11)
        #  local_site_box.setFixedHeight(self.height // 10)
        # self.local_site_box.setLayout(self.local_site_layout)
        # self.date_box_layout.addWidget(self.local_site_box)
        # self.date_box_layout.addWidget(keyboard_button)
        self.date_box_layout.setSpacing(1)
        # 将布局应用在当前组
        self.date_box.setLayout(self.date_box_layout)
        # 将时间和日历控件添加到一个布局中
        self.time_date_box = QGroupBox()
        self.time_date_layout = QHBoxLayout()
        self.time_date_layout.addWidget(self.time_box,6)
        self.time_date_layout.addWidget(self.date_box,1)  # 设置时钟和日历的比例为14：5
        self.time_date_layout.setSpacing(0)
        self.time_date_box.setLayout(self.time_date_layout)
        self.time_date_box.setFixedSize(self.width, (self.height // 2 + self.height // 4))  # 高度占三分之二
        self.main_layout.addWidget(self.time_date_box)
        #
        # 创建一个水平布局
        #
        self.horizon_layout = QHBoxLayout()
        self.horizon_box = QGroupBox()
        self.horizon_box.setLayout(self.horizon_layout)
        # 创建语音对话显示区
        # self.dialog_show()
        # 创建一个天气网格布局组
        self.weather_grid = QGroupBox()
        self.weather_grid.setFixedWidth(self.width) 
        # self.weather_grid.setFixedHeight(self.height // 2)
        self.weather_layout = QGridLayout()
        self.font_style = "color: rgb(0, 0, 0);font-family: 楷体;font-size:16pt;font-weight:bold;"
        # 创建网格布局中的天气信息提示组
        self.day_title = QLabel("日期")
        self.day_title.setStyleSheet(self.font_style)
        self.weather_prompt_box = QGroupBox()
        self.weather_prompt_box.setFixedWidth(self.width // 3 + self.width // 3 + self.width // 8)
        self.weather_prompt_box_layout = QHBoxLayout()
        for k in range(5):
            text0_data = QLabel()
            if k == 0:
                prompt_str = '天气状况'
            elif k == 1:
                prompt_str = '最高温度'
            elif k == 2:
                prompt_str = '最低温度'
            elif k == 3:
                prompt_str = '风向'
            elif k == 4:
                prompt_str = '风力'
            text0_data.setText(prompt_str)
            text0_data.setStyleSheet(self.font_style)
            text0_data.setAlignment(Qt.AlignCenter)
            self.weather_prompt_box_layout.addWidget(text0_data)
        self.weather_prompt_box.setLayout(self.weather_prompt_box_layout)
        self.weather_layout.addWidget(self.day_title, 0, 0)
        self.weather_layout.addWidget(self.weather_prompt_box, 0, 1)
        # 完成网格布局剩余部分，显示天气信息
        self.weather_data = fetch_weather("101270107")
        for i, data in enumerate(self.weather_data):
            label = QLabel(f"{data[0]}")  # 日期
            label.setStyleSheet(self.font_style)
            weather0_box = QGroupBox()
            weather0_box_layout = QHBoxLayout()
            for j in range(5):
                text_data = QLabel()
                text_data.setStyleSheet(self.font_style)
                # if j == 0:
                #     text_data.setStyleSheet("border-image:{}".format(self.weather_image))
                data_str = data[j + 1]
                # if j == 1:
                #        data_str = data_str +"°C"
                text_data.setText(data_str)
                text_data.setAlignment(Qt.AlignCenter)
                weather0_box_layout.addWidget(text_data)
            weather0_box.setLayout(weather0_box_layout)
            # 这两个for循环将天气信息整理出来，一标签+一个水平布局组显示一天的信息，并将它们逐个添加到网格布局组
            self.weather_layout.addWidget(label, i + 1, 0)
            self.weather_layout.addWidget(weather0_box, i + 1, 1)
        self.weather_grid.setLayout(self.weather_layout)  # 将网格布局应用到网格布局组
        # self.weather_grid.setFixedWidth(self.width)  # 设置天气网络宽为屏幕宽
        self.scroll_area = QScrollArea()
        self.scroll_area.setFixedWidth(self.width // 2 + self.width // 4 + self.width // 5 + self.width // 25)
        self.scroll_area.setWidget(self.weather_grid)
        # self.horizon_layout.addWidget(self.dialog_box, 1)
        # self.horizon_layout.addWidget(self.scroll_area)
        # self.main_layout.addWidget(self.horizon_box)
        self.main_layout.addWidget(self.scroll_area)
        # 自动滚动,timer_scroll无反应
        self.timer_scroll = QTimer()
        self.timer_scroll.timeout.connect(self.auto_scroll)
        self.timer_scroll.start(50)
        # 设置窗口主布局
        self.main_layout.addStretch()
        self.setLayout(self.main_layout) 
        
    def auto_update_tmp_hmd(self):
        tmp, hmd = get_tmp_hmd()
        tmp_str = str(tmp)
        hmd_str = str(hmd)
        tmp_text = "室内温度：" + tmp_str + "°C|"+"室内湿度：" + hmd_str + '%'
        self.temperature_label.setText(tmp_text)
        # hmd_str = str(hmd)
        # hmd_text = "   室内湿度：" + hmd_str + '%'
        # self.humidity_label.setText(hmd_text)
        
    def auto_scroll(self):
        # 每次滚动一个像素
        bar = self.scroll_area.verticalScrollBar()
        current_value = bar.value()
        max_value = bar.maximum()
        if current_value + 1 > max_value:
            bar.setValue(0)
        else:
            bar.setValue(bar.value()+1)
        
    def dialog_show(self):
        # 暂时不需要
        self.dialog_layout = QVBoxLayout()
        # self.dialog_label = QLabel("<font style='font-family: Comic Sans MS; font-size: 8pt;'><b>语  音  对  话  框</b></font>")
        # self.dialog_label.setAlignment(Qt.AlignCenter)
        # self.dialog_label.setFixedHeight(self.height // 50 )
        self.dialog_text= QTextEdit('展示语音对话内容')
        self.dialog_text.setStyleSheet("color: rgb(0, 0, 0);font-family: Comic Sans MS;font-size:12pt;font-weight:bold;")
        self.dialog_text.setFixedWidth(self.width // 5 + self.width // 2)
        self.dialog_text.setFixedHeight(self.height // 2)
        dialog_area = QScrollArea()
        dialog_area.setFixedWidth(self.width // 5 + self.width // 4)
        dialog_area.setWidget(self.dialog_text)
        # self.dialog_layout.addWidget(self.dialog_label)
        self.dialog_layout.addWidget(dialog_area)
        self.dialog_box = QGroupBox()
        self.dialog_box.setLayout(self.dialog_layout)
        #self.horizon_layout.addWidget(self.dialog_box)
    def update_time_label(self):
        current_datetime = QDateTime.currentDateTime()
        current_date_str = current_datetime.toString("yyyy年MM月dd日")
        current_time_str = current_datetime.toString("hh:mm:ss")
        self.time_label.setText(
            "<font style='font-family: Comic Sans MS; font-size: 132pt;'><b>%s</b></font>" % current_time_str[0:5] +
            "<font style='font-family: Comic Sans MS; font-size: 48pt;'><b>%s</b><br></font>" % current_time_str[-3:] +
            "<font style='font-family: Comic Sans MS; font-size: 32pt;'><b>%s</b></font>" % current_date_str)
            
    def update_temperature(self):
        # 直接设置按钮，绑定温湿度检测函数,不需要
        tmp, hmd = get_tmp_hmd()
        tmp_str = str(tmp)
        tmp_text = "   室内温度：" + tmp_str + "°C"
        self.temperature_label.setText(tmp_text)
        
    def update_humidity(self):
        # 直接设置按钮，绑定温湿度检测函数，不需要
        tmp, hmd = get_tmp_hmd()
        hmd_str = str(hmd)
        hmd_text = "室内湿度：" + hmd_str
        self.humidity_label.setText(hmd_text)
        
    def switch_case(self,weekday):
            weekday_copy = weekday
            return {
            "Mo": "Mon.",
            "Tu": "Tues.",
            "We": "Wed.",
            "Th": "Thurs.",
            "Fr": "Fri.",
            "Sa": "Sat.",
            "Su": "Sun.",
            }.get(weekday,weekday_copy)
            
    def current_date_label(self):
        current_date0 = QDate.currentDate()
        current_date = current_date0.toPyDate()
        current_date_string = current_date0.toString()
        weekday = current_date_string[0] + current_date_string[1]  # 星期
        weekday = self.switch_case(weekday)
        # 母亲节，五月的第二个星期日
        mother_day = ''
        if current_date.month == 5:
            if current_date.day > 7 and current_date.day < 15:
                if weekday == 'Sun.' or '周日':
                    mother_day = ' 母亲节 |'
        # 父亲节，六月的第三个星期日
        father_day = ''
        if current_date.month == 6:
            if current_date.day > 14 and current_date.day < 22:
                if weekday == 'Sun.'or '周日':
                    father_day = ' 父亲节 |'

        lunar_date = lunardate.LunarDate.fromSolarDate(current_date.year, current_date.month, current_date.day)
        lunar_day = str(lunar_date.month) + '-' + str(lunar_date.day)
        solar_day = str(current_date.month) + '-' + str(current_date.day)
        # print(type(lunar_date.month)) # int类型
        lunar_festival = FestivalTable.lunar_festival(lunar_day)
        solar_festival = FestivalTable.solar_festival(solar_day)
        solar_term = FestivalTable.solar_terms(current_date.year, solar_day)
        self.choose_date_label.setText(
            "<font style='font-family: Comic Sans MS; font-size: 12pt;'><b>{0}{1}{0}|</b></font>".format(' ', weekday) +
            "<font style='font-family: Comic Sans MS; font-size: 12pt;'><b>{0}</b></font>".format(lunar_festival) +
            "<font style='font-family: Comic Sans MS; font-size: 12pt;'><b>{0}</b></font>".format(solar_festival) +
            "<font style='font-family: Comic Sans MS; font-size: 12pt;'><b>{0}</b></font>".format(mother_day) +
            "<font style='font-family: Comic Sans MS; font-size: 12pt;'><b>{0}</b></font>".format(father_day) +
            "<font style='font-family: Comic Sans MS; font-size: 12pt;'><b>{0}</b></font>".format(solar_term) +
            "<font style='font-family: Comic Sans MS; font-size: 12pt;'><b>{3}农历：{0}-{1}-{2}{3}</b></font>".format(
                lunar_date.year, lunar_date.month, lunar_date.day, ' ')
        )

    def update_selected_dates(self, date):
        solar_date = date.toPyDate()
        solar_date_string = date.toString()
        weekday = solar_date_string[0] + solar_date_string[1]  # 星期
        weekday = self.switch_case(weekday)
        # 母亲节，五月的第二个星期日
        mother_day = ''
        if solar_date.month == 5:
            if solar_date.day > 7 and solar_date.day < 15:
                if weekday == 'Sun.'or '周日':
                    mother_day = ' 母亲节 |'
        # 父亲节，六月的第三个星期日
        father_day = ''
        if solar_date.month == 6:
            if solar_date.day > 14 and solar_date.day < 22:
                if weekday == 'Sun.'or '周日':
                    father_day = ' 父亲节 |'

        lunar_date = lunardate.LunarDate.fromSolarDate(solar_date.year, solar_date.month, solar_date.day)
        lunar_day = str(lunar_date.month) + '-' + str(lunar_date.day)
        solar_day = str(solar_date.month) + '-' + str(solar_date.day)
        # print(type(lunar_date.month)) # int类型
        lunar_festival = FestivalTable.lunar_festival(lunar_day)
        solar_festival = FestivalTable.solar_festival(solar_day)
        solar_term = FestivalTable.solar_terms(solar_date.year, solar_day)
        self.choose_date_label.setText(
            "<font style='font-family: Comic Sans MS; font-size: 12pt;'><b>{0}{1}{0}|</b></font>".format(" ", weekday) +
            "<font style='font-family: Comic Sans MS; font-size: 12pt;'><b>{0}</b></font>".format(lunar_festival) +
            "<font style='font-family: Comic Sans MS; font-size: 12pt;'><b>{0}</b></font>".format(solar_festival) +
            "<font style='font-family: Comic Sans MS; font-size: 12pt;'><b>{0}</b></font>".format(mother_day) +
            "<font style='font-family: Comic Sans MS; font-size: 12pt;'><b>{0}</b></font>".format(father_day) +
            "<font style='font-family: Comic Sans MS; font-size: 12pt;'><b>{3}农历：{0}-{1}-{2}{3}</b></font>".format(
                lunar_date.year, lunar_date.month, lunar_date.day, ' ')
        )

    def get_weather(self):
        self.virtual_keyboard.close_keyboard()  # 关闭虚拟键盘
        import city_convert
        city = self.local_site_input.text()
        city_code = city_convert.get_city_code(city)
        weather_grid = QGroupBox()
        weather_grid.setFixedWidth(self.width)
        weather_layout = QGridLayout()
        
        # 创建网格布局中的天气信息提示组
        day_title = QLabel("日期")
        day_title.setStyleSheet(self.font_style)
        weather_prompt_box = QGroupBox()
        weather_prompt_box.setFixedWidth(self.width // 3 + self.width // 2)
        weather_prompt_box_layout = QHBoxLayout()
        for k in range(5):
            text0_data = QLabel()
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
            text0_data.setStyleSheet(self.font_style)
            text0_data.setAlignment(Qt.AlignCenter)
            weather_prompt_box_layout.addWidget(text0_data)
        weather_prompt_box.setLayout(weather_prompt_box_layout)
        weather_layout.addWidget(day_title, 0, 0)
        weather_layout.addWidget(weather_prompt_box, 0, 1)
        # 完成网格布局剩余部分，显示天气信息
        weather_data = fetch_weather(city_code)
        for i, data in enumerate(weather_data):
            label = QLabel(f"{data[0]}")  # 日期
            label.setStyleSheet(self.font_style)
            weather0_box = QGroupBox()
            weather0_box_layout = QHBoxLayout()
            for j in range(5):
                text_data = QLabel()
                text_data.setStyleSheet(self.font_style)
                data_str = data[j + 1]
                text_data.setText(data_str)
                text_data.setAlignment(Qt.AlignCenter)
                # weather_layout.addWidget(text_data, i+1, j+1)
                weather0_box_layout.addWidget(text_data)
            weather0_box.setLayout(weather0_box_layout)
            # 这两个for循环将天气信息整理出来，一标签+一个水平布局组显示一天的信息，并将它们逐个添加到网格布局组
            weather_layout.addWidget(label, i + 1, 0)
            weather_layout.addWidget(weather0_box, i + 1, 1)
        weather_grid.setLayout(weather_layout)  # 将网格布局应用到网格布局组
        # weather_grid.setFixedWidth(self.width)
        scroll_area = QScrollArea()
        scroll_area.setFixedWidth(self.width // 2 + self.width // 4 + self.width // 5 + self.width // 25)
        scroll_area.setWidget(weather_grid)
        self.main_layout.replaceWidget(self.scroll_area, scroll_area)  # 替换之前的天气布局
        self.scroll_area = scroll_area  # 替代原先的布局

    def show_virtual_keyboard(self):
        # local
        self.virtual_keyboard = VirtualKeyboard(self.local_site_input, 0,
                                                self.height // 8,
                                                self.width // 3 + self.width // 3,
                                                self.height // 50, )
        self.virtual_keyboard.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)  # 创建qpp变量，指向QApplication对象，其中的参数sys.argv指的是运行程序的环境参数，是一个列表
    w = MyWindow()  # 创建一个自己创建的类
    # w.show()
    w.showFullScreen()  # 全屏展示窗口，ctrl+Esc 退出
    app.exec_()  # 必有调用exec,相当于死循环使程序一直运行，监测用户是否进行某些操作
