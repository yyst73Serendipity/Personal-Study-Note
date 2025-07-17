# PinkPig 桌面宠物

## 项目简介

PinkPig 是一个可爱的桌面宠物程序，基于 Python + PyQt5 开发。它会以小猪的形象常驻在你的桌面右下角，支持多种互动表情和心情状态显示。你可以通过点击宠物，选择不同的动作，改变它的心情值。

## 功能特色
- 多种动态表情（如听音乐、吃蛋糕、跳跃、哭泣等）
- 心情值实时显示，支持持久化保存
- 菜单栏支持 emoji+文字，交互友好
- 支持高DPI屏幕

## 启动方式
你可以通过以下三种方式启动 PinkPig 桌宠：

### 1. dist 文件夹下的 .exe 可执行文件
已经用 PyInstaller 打包过，直接进入 `dist` 文件夹，双击 `pinkpig.exe` 即可启动，无需安装 Python 环境。

### 2. start.bat 启动脚本
在 Windows 下，双击 `start.bat` 脚本，会自动调用本地 Python 环境运行 pinkpig.py。

### 3. 终端命令方式
确保已安装 Python 3 和 PyQt5，在 `PinkPig` 目录下打开命令行，输入：

```
python pinkpig.py
```

即可启动桌宠。

## 资源说明
- 所有表情动图（gif）均存放于 `images2` 文件夹下。
- 心情值数据保存在 `mood_pig.json` 文件中。

## 依赖环境
- Python 3.x
- PyQt5

如需打包为 exe，可使用 PyInstaller：
```
pyinstaller -F -w pinkpig.py
```

---

欢迎体验和二次开发！ 