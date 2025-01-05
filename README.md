# 批量删除文件夹

## 接单：实用小工具、深度学习机器学习代码复现

**批量删除文件夹** 是一款用于根据文件夹最后修改日期删除指定文件夹的程序。用户可以选择删除某个指定日期之前的文件夹，默认情况下会删除以 "pack" 开头的文件夹。

![image-20250105183005541](E:\实训\pythonProject\assets\image-20250105183005541.png)

## 功能

- 用户可以手动选择文件夹路径。
- 支持设置一个日期范围，删除指定日期前的文件夹。
- 可以设置默认路径，下次启动程序时自动加载上次使用的文件夹路径。
- 支持图形界面操作，简化用户操作流程。
- 用户删除操作前会收到确认提示，避免误操作。

## 特性

- 删除以特定前缀（默认为 `pack`）开头的文件夹。
- 支持图标设置，提供自定义图标功能。
- 操作简单，适用于 Windows 平台。
- 打包成 `.exe` 文件，用户无需安装 Python 即可运行。

## 安装与使用

### 1. 下载

下载 `.exe` 文件并直接运行，或者根据以下步骤从源代码构建可执行文件。

### 2. 配置文件

程序会在首次运行时创建一个配置文件 `settings.ini`，存储当前文件夹路径和删除时间点（以便下次使用）。

### 3. 使用

1. 启动程序后，用户可以点击 **浏览** 按钮选择目标文件夹路径。
2. 输入删除的天数（`0` 代表删除今天修改的文件夹，其他数值代表删除指定天数之前的文件夹）。
3. 设置是否将当前路径保存为默认路径，下次启动时自动加载。
4. 点击 **删除旧文件夹** 后，会显示确认框，确认无误后执行删除操作。

### 4. 删除操作确认

在删除操作前，程序会弹出确认框，提示用户删除文件夹的时间点和文件夹列表。用户可以选择确认或取消操作。

### 5. 联系我们

如果遇到问题或需要技术支持，请点击 **联系我们**，查看联系方式。

------

## 打包为 `.exe` 文件

如果你希望自己打包此程序为 `.exe` 文件，遵循以下步骤：

### 1. 安装依赖

确保已安装 `PyInstaller`，通过以下命令进行安装：

```bash
pip install pyinstaller
```

### 2. 打包程序

将 Python 脚本打包成 `.exe` 文件，命令如下：

```bash
pyinstaller --onefile --windowed --icon=APP.ico --name="批量删除文件夹" --add-data "settings.ini;." test.py
```

- `--onefile`：将所有文件打包为单个 `.exe` 文件。
- `--windowed`：避免显示命令行窗口（适用于 GUI 应用）。
- `--icon=APP.ico`：为 `.exe` 文件设置自定义图标。
- `--name="批量删除文件夹"`：指定生成的 `.exe` 文件名称。
- `--add-data "settings.ini;."`：将配置文件 `settings.ini` 添加到 `.exe` 文件中。

### 3. 运行 `.exe` 文件

打包完成后，您可以在 `dist` 文件夹找到 `批量删除文件夹.exe` 文件。双击该文件即可运行程序。

------

## 项目结构

```
批量删除文件夹/
│
├── settings.ini          # 配置文件，存储路径和删除日期
├── test.py               # 主程序文件
├── APP.ico               # 程序图标文件（用于 `.exe`）
├── dist/                 # 打包后的文件夹，包含生成的 `.exe` 文件
└── README.md             # 项目说明文件
```

## 联系我们

- **技术支持**: 杜先生
- **联系方式**: 15100578801（微信同号）

------

## 注意事项

- 本程序仅支持 Windows 平台。
- 在运行程序之前，请确保选择正确的目标文件夹路径，以免误删数据。
- 请定期备份重要数据，避免误删除操作造成数据丢失。