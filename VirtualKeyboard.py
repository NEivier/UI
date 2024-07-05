import sys

from PyQt5.QtGui import QPalette, QPixmap, QBrush
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QMainWindow, QLineEdit, QWidget, QApplication, \
    QHBoxLayout


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Virtual Keyboard Example")
        self.setGeometry(500, 500, 500, 500)

        # 创建输入框
        self.input_box = QLineEdit(self)
        # 创建虚拟键盘按钮
        self.keyboard_button = QPushButton("Virtual Keyboard")

        # 将输入框和按钮添加到布局
        layout = QVBoxLayout()
        layout.addWidget(self.input_box)
        layout.addWidget(self.keyboard_button)

        # 创建中央窗口部件，并设置布局
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # 连接虚拟键盘按钮的点击事件到自定义的槽函数
        self.keyboard_button.clicked.connect(self.show_virtual_keyboard)

    def show_virtual_keyboard(self):
        # 在这个槽函数中，你可以执行打开虚拟键盘的操作
        # 实际操作可能会依赖于你所使用的虚拟键盘库或工具
        # 这里只是一个示例
        self.virtual_keyboard = VirtualKeyboard(self.input_box)
        self.virtual_keyboard.show()


class VirtualKeyboard(QWidget):
    def __init__(self, target, x, y, width, height):
        super().__init__()

        self.setWindowTitle("Virtual Keyboard")
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.setGeometry(self.x, self.y, self.width, self.height)

        self.target = target  # 此目标为输入框
        self.caps_lock = False  # 跟踪大小写键
        # 设置窗口背景图片
        palette = self.palette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap('/home/pi/UI/images/background_1/background.jpg')))  # 设置背景图片
        self.setPalette(palette)
        self.setAutoFillBackground(True)  # 自动填充背景色
        # 创建主布局
        self.main_layout = QVBoxLayout()

        # 创建键盘字符区域
        digits_layout = QHBoxLayout()  # 数字区域
        chars_layout = QHBoxLayout()  # 特殊字符区
        letters_layout_1 = QHBoxLayout()  # 第一排字母区
        letters_layout_2 = QHBoxLayout()  # 第二排字母区
        letters_layout_3 = QHBoxLayout()  # 第三排字母区
        # self.digits = ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '+', '=']
        # self.chars = ['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '——', '_', '℃']
        # self.letters_1 = [';', '；', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '·', '[', ']', '|', '\\']
        # self.letters_2 = ['{', '}', ':', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', '<', '>', '‘', '’', '“', '”']
        # self.letters_3 = ['?', '/', '：', 'z', 'x', 'c', 'v', 'b', 'n', 'm', '\'', ',', '.', '，', '。', '…']
        self.digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '+']
        self.chars = ['!', '@', '#', '$', '%', '^', '*', '(', ')', '·', '_', '=']
        self.letters_1 = [';', '|', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']']
        self.letters_2 = ['{', '}', ':', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', '<', '>', '‘', '’']
        self.letters_3 = ['?', '/', '…', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '，', '。']
        # 插入数字
        for digit in self.digits:
            button = QPushButton(digit)
            button.setFixedSize(self.width // 20, self.width // 20)
            button.setStyleSheet("QPushButton { background-image: url('/home/pi/UI/images/background_1/background.jpg');"
                                 "color: white;border-width: 2px;border-style: solid;border-color: black;"
                                 "font-weight: bold;font-size:10pt;}")
            button.clicked.connect(lambda checked, l=digit: self.insert_letter(l))
            digits_layout.addWidget(button)
        # 插入特殊字符
        for char in self.chars:
            button = QPushButton(char)
            button.setFixedSize(self.width // 20, self.width // 20)
            button.setStyleSheet("QPushButton { background-image: url('/home/pi/UI/images/background_1/background.jpg');"
                                 "color: white;border-width: 2px;border-style: solid;border-color: black;"
                                 "font-weight: bold;font-size:10pt;}")
            button.clicked.connect(lambda checked, l=char: self.insert_letter(l))
            chars_layout.addWidget(button)
        # 插入第一排字母
        for letter in self.letters_1:
            button = QPushButton(letter)
            button.setFixedSize(self.width // 20, self.width // 20)
            button.setStyleSheet("QPushButton { background-image: url('/home/pi/UI/images/background_1/background.jpg');"
                                 "color: white;border-width: 2px;border-style: solid;border-color: black;"
                                 "font-weight: bold;font-size:12pt;}")
            button.clicked.connect(lambda checked, l=letter: self.insert_letter(l))
            letters_layout_1.addWidget(button)
        # 插入第二排字母
        for letter in self.letters_2:
            button = QPushButton(letter)
            button.setFixedSize(self.width // 20, self.width // 20)
            button.setStyleSheet("QPushButton { background-image: url('/home/pi/UI/images/background_1/background.jpg');"
                                 "color: white;border-width: 2px;border-style: solid;border-color: black;"
                                 "font-weight: bold;font-size:12pt;}")
            button.clicked.connect(lambda checked, l=letter: self.insert_letter(l))
            letters_layout_2.addWidget(button)
        # 插入第三排字母
        for letter in self.letters_3:
            button = QPushButton(letter)
            button.setFixedSize(self.width // 20, self.width // 20)
            button.setStyleSheet("QPushButton { background-image: url('/home/pi/UI/images/background_1/background.jpg');"
                                 "color: white;border-width: 2px;border-style: solid;border-color: black;"
                                 "font-weight: bold;font-size:12pt;}")
            button.clicked.connect(lambda checked, l=letter: self.insert_letter(l))
            letters_layout_3.addWidget(button)

        # 向主布局中添加次布局
        self.main_layout.addLayout(digits_layout)
        self.main_layout.addLayout(chars_layout)
        self.main_layout.addLayout(letters_layout_1)
        self.main_layout.addLayout(letters_layout_2)
        self.main_layout.addLayout(letters_layout_3)

        # 功能键区域
        actions_layout = QHBoxLayout()
        # 创建切换 Caps Lock 键的按钮
        self.caps_lock_button = QPushButton("Caps Lock")
        self.caps_lock_button.setStyleSheet("QPushButton {background-color:white; "
                                            "font-weight: bold;font-size:10pt;}")
        self.caps_lock_button.setFixedSize(self.width // 4, self.width // 20)
        self.caps_lock_button.setCheckable(True)
        self.caps_lock_button.clicked.connect(self.toggle_caps_lock)
        actions_layout.addWidget(self.caps_lock_button)
        # 退回键
        backspace_button = QPushButton("←")
        backspace_button.setStyleSheet("QPushButton {background-color:white; "
                                       "font-weight: bold;font-size:10pt;}")
        backspace_button.setFixedSize(self.width // 4, self.width // 20)
        backspace_button.clicked.connect(self.backspace)
        actions_layout.addWidget(backspace_button)
        # 清除键
        clear_button = QPushButton("Clear")
        clear_button.setStyleSheet("QPushButton {background-color:white; "
                                   "font-weight: bold;font-size:10pt;}")
        clear_button.setFixedSize(self.width // 4, self.width // 20)
        clear_button.clicked.connect(self.clear_text)
        actions_layout.addWidget(clear_button)
        # 关闭键
        close_button = QPushButton("Close")
        close_button.setStyleSheet("QPushButton {background-color:white; "
                                   "font-weight: bold;font-size:10pt;}")
        close_button.setFixedSize(self.width // 4, self.width // 20)
        close_button.clicked.connect(self.close_keyboard)
        actions_layout.addWidget(close_button)
        # 添加到主布局
        self.main_layout.addLayout(actions_layout)

        # 设置主布局
        self.setLayout(self.main_layout)

    def add_letter(self, letter):
        current_text = self.target.text()
        self.target.setText(current_text + letter)

    def backspace(self):
        current_text = self.target.text()
        self.target.setText(current_text[:-1])

    def clear_text(self):
        self.target.clear()

    def close_keyboard(self):
        self.close()

    def insert_letter(self, letter):
        if self.caps_lock:
            letter = letter.upper()
        # 在被触发的按键上插入字母到目标输入框
        self.target.insert(letter)

    def toggle_caps_lock(self):
        self.caps_lock = not self.caps_lock
        self.caps_lock_button.setChecked(self.caps_lock)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
