# 桌面端豆瓣影评TOP250

基于PySide6（Qt For Python）搭建的“豆瓣影评TOP250”简易管理系统

## 安装依赖
项目环境`python=3.8.19`，运行项目前请执行命令安装依赖
```powershell
pip install -r requirement.txt
```

## 运行程序
本地测试环境等，请在项目文件`src/config.py`中配置

执行如下命令，启动项目
```powershell
python ./src/main.py
```

## 构建可执行文件
项目使用`PyInstaller`打包成可执行文件，执行如下命令
```powershell
pyinstaller -F ./src/main.py
```