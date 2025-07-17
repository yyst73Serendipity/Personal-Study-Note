import sys
import os
import json
from PyQt5 import QtCore, QtGui, QtWidgets

# 资源路径
IMG_DIR = os.path.join(os.path.dirname(__file__), 'images2')
# 仅使用images2下的gif文件
GIFS = {
    'music': 'music.gif',
    'cake': 'cake.gif',
    'tired': 'tired.gif',
    'cry': 'cry.gif',
    'jump': 'jump.gif',
    'default': 'default.gif',
}
# 菜单项配置（emoji+文字）
MENU_ITEMS = [
    ('🎵', '听音乐', 'music'),
    ('🍰', '吃蛋糕', 'cake'),
    ('😪', '累趴了', 'tired'),
    ('😭', '好想哭', 'cry'),
    ('🐷', '跳跳跳', 'jump'),
]
MOOD_FILE = os.path.join(os.path.dirname(__file__), 'mood_pig.json')

# DPI 适配
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

def check_resources():
    missing = []
    for f in GIFS.values():
        if not os.path.exists(os.path.join(IMG_DIR, f)):
            missing.append(f)
    if missing:
        QtWidgets.QMessageBox.critical(None, '资源缺失', '缺少资源文件:\n' + '\n'.join(missing) + '\n请将其放入 ./images2/ 目录下')
        sys.exit(1)

def load_mood():
    if os.path.exists(MOOD_FILE):
        try:
            with open(MOOD_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return int(data.get('mood', 100))
        except Exception:
            return 100
    return 100

def save_mood(mood):
    try:
        with open(MOOD_FILE, 'w', encoding='utf-8') as f:
            json.dump({'mood': mood}, f)
    except Exception:
        pass

class MoodBar(QtWidgets.QWidget):
    """心情状态栏，左侧emoji，进度条，进度条末端显示心情数值"""
    def __init__(self, mood=100, parent=None):
        super().__init__(parent)
        self.mood = mood
        self.setFixedHeight(32)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.font = QtGui.QFont("Helvetica Neue", 13, QtGui.QFont.Light)
        self.emoji = '😊'
        self.update_emoji()

    def set_mood(self, mood):
        self.mood = max(0, min(100, mood))
        self.update_emoji()
        self.update()

    def update_emoji(self):
        if self.mood >= 70:
            self.emoji = '😊'
        elif self.mood >= 30:
            self.emoji = '😐'
        else:
            self.emoji = '😢'

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setFont(self.font)
        # 画emoji
        emoji_x = 10
        emoji_y = 22
        painter.setPen(QtGui.QColor('#8B4513'))
        painter.drawText(emoji_x, emoji_y, self.emoji)
        # 进度条参数
        bar_x = emoji_x + 28
        bar_y = 10
        bar_w = 110
        bar_h = 14
        radius = bar_h / 2
        # 背景条（未填部分粉色）
        bg_color = QtGui.QColor('#F9C6D3')
        painter.setBrush(bg_color)
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRoundedRect(bar_x, bar_y, bar_w, bar_h, radius, radius)
        # 已填部分（深粉色）
        fg_color = QtGui.QColor('#F7A1B0')
        painter.setBrush(fg_color)
        val_w = int(bar_w * max(0, min(self.mood, 100)) / 100)
        if val_w > 0:
            painter.drawRoundedRect(bar_x, bar_y, val_w, bar_h, radius, radius)
        # 画心情数值
        painter.setFont(self.font)
        painter.setPen(QtGui.QColor('#8B4513'))
        num_x = bar_x + val_w + 8
        num_y = 22
        painter.drawText(num_x, num_y, str(self.mood))

class PigWindow(QtWidgets.QWidget):
    """主窗口"""
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.Tool
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFixedSize(220, 240)
        # 主布局
        self.vbox = QtWidgets.QVBoxLayout(self)
        self.vbox.setContentsMargins(10, 10, 10, 10)
        self.vbox.setSpacing(0)
        # 状态栏
        self.mood = load_mood()
        self.mood_bar = MoodBar(self.mood)
        self.vbox.addWidget(self.mood_bar, alignment=QtCore.Qt.AlignTop)
        # GIF展示区
        self.gif_label = QtWidgets.QLabel()
        self.gif_label.setFixedSize(200, 180)
        self.gif_label.setStyleSheet('background: transparent;')
        self.vbox.addWidget(self.gif_label, alignment=QtCore.Qt.AlignHCenter)
        # 默认显示default.gif
        self.movie = QtGui.QMovie(os.path.join(IMG_DIR, GIFS['default']))
        self.movie.setScaledSize(QtCore.QSize(200, 180))
        self.gif_label.setMovie(self.movie)
        self.movie.start()
        # 绑定GIF点击事件
        self.gif_label.mousePressEvent = self.show_menu
        # ESC退出
        QtWidgets.QShortcut(QtGui.QKeySequence('Esc'), self, self.close)
        # 右下角定位
        QtCore.QTimer.singleShot(100, self.move_to_bottom_right)

    def move_to_bottom_right(self):
        screen = QtWidgets.QApplication.primaryScreen().availableGeometry()
        x = screen.right() - self.width() - 20
        y = screen.bottom() - self.height() - 20
        self.move(x, y)

    def show_menu(self, event):
        menu = QtWidgets.QMenu(self)
        menu.setStyleSheet('''
            QMenu {
                background: #F9C6D3;
                border-radius: 10px;
                padding: 2px 4px;
                font-size: 13px;
                min-width: 55px;
            }
            QMenu::item {
                padding: 3px 8px 3px 4px;
                border-radius: 5px;
                color: #8B4513;
                min-height: 18px;
            }
            QMenu::item:selected {
                background: #F7A1B0;
                color: #D2691E;
            }
        ''')
        actions = []
        for emoji, text, key in MENU_ITEMS:
            act = QtWidgets.QAction(f"{emoji} {text}", self)
            act.triggered.connect(lambda checked, k=key: self.menu_action(k))
            menu.addAction(act)
            actions.append(act)
        menu.addSeparator()
        exit_act = QtWidgets.QAction('退出', self)
        exit_act.triggered.connect(self.close)
        menu.addAction(exit_act)
        menu.exec_(self.mapToGlobal(event.pos()))

    def menu_action(self, key):
        tip = None
        # 这里可自定义心情变化规则
        if key in ['music', 'cake', 'jump']:
            if self.mood >= 100:
                tip = '已经是最大心情值啦！'
            else:
                self.mood += 1
        elif key in ['tired', 'cry']:
            if self.mood <= 0:
                tip = '已经是最小心情值啦！'
            else:
                self.mood -= 1
        self.mood = max(0, min(100, self.mood))
        self.mood_bar.set_mood(self.mood)
        save_mood(self.mood)
        self.switch_gif(key)
        if tip:
            QtWidgets.QToolTip.showText(self.mapToGlobal(self.gif_label.pos()), tip, self, self.rect(), 1200)

    def switch_gif(self, key):
        gif_path = os.path.join(IMG_DIR, GIFS.get(key, GIFS['default']))
        if os.path.exists(gif_path):
            self.movie.stop()
            self.movie = QtGui.QMovie(gif_path)
            self.movie.setScaledSize(QtCore.QSize(200, 180))
            self.gif_label.setMovie(self.movie)
            self.movie.start()
        else:
            QtWidgets.QMessageBox.warning(self, '资源缺失', f'缺少GIF文件: {GIFS.get(key, "default.gif")}')

    def closeEvent(self, event):
        save_mood(self.mood)
        event.accept()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    try:
        check_resources()
        win = PigWindow()
        win.show()
        sys.exit(app.exec_())
    except Exception as e:
        QtWidgets.QMessageBox.critical(None, '错误', str(e))
        sys.exit(1) 