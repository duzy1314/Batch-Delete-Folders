import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime, timedelta
import configparser

# 配置文件路径
config_file = "settings.ini"


def load_config():
    # 尝试加载配置文件，获取默认路径和日期信息
    config = configparser.ConfigParser()
    if os.path.exists(config_file):
        config.read(config_file)
        if 'Settings' in config:
            default_path = config['Settings'].get('folderPath', '')
            last_deleted_date = config['Settings'].get('lastDeletedDate', '')
            prefix = config['Settings'].get('prefix', 'pack')  # 获取文件夹前缀
            return default_path, last_deleted_date, prefix
    return "", "", "pack"  # 默认前缀为 "pack"


def save_config(folder_path, last_deleted_date, prefix):
    # 保存当前的文件夹路径、日期信息和前缀到配置文件
    config = configparser.ConfigParser()
    config['Settings'] = {
        'folderPath': folder_path,
        'lastDeletedDate': last_deleted_date,
        'prefix': prefix  # 保存文件夹前缀
    }
    with open(config_file, 'w') as configfile:
        config.write(configfile)


def delete_old_folders():
    # 获取用户选择的文件夹路径
    folder_path = folder_path_entry.get()
    if not folder_path:
        messagebox.showerror("错误", "请先选择一个文件夹路径")
        return

    # 获取用户输入的删除天数
    try:
        days_to_delete = int(delete_days_entry.get())
        if days_to_delete < 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("错误", "请输入有效的天数（正整数或0）")
        return

    # 获取当前日期，并计算指定天数前的日期
    today = datetime.today()
    if days_to_delete == 0:
        # 如果是0，表示删除今天修改过的文件夹
        cutoff_date = today
    else:
        cutoff_date = today - timedelta(days=days_to_delete)
    cutoff_date_str = cutoff_date.strftime('%Y%m%d')

    # 获取用户输入的文件夹前缀
    folder_prefix = prefix_entry.get().strip() or "pack"  # 默认为"pack"

    # 确认用户的操作
    confirmation = messagebox.askyesno("确认删除",
                                       f"您确定删除{folder_path}下，修改日期早于{cutoff_date_str}的以'{folder_prefix}'开头的文件夹吗？")
    if not confirmation:
        return

    # 保存默认路径、删除日期和前缀（如果选择了默认路径）
    if default_path_var.get():
        save_config(folder_path, cutoff_date_str, folder_prefix)

    # 遍历文件夹内以指定前缀开头的文件夹
    deleted_folders = []
    try:
        for folder in os.listdir(folder_path):
            folder_dir = os.path.join(folder_path, folder)
            if os.path.isdir(folder_dir) and folder.lower().startswith(folder_prefix.lower()):
                # 获取文件夹的最后修改时间
                folder_modified_time = os.path.getmtime(folder_dir)
                modify_date = datetime.fromtimestamp(folder_modified_time).strftime('%Y%m%d')

                # 比较修改日期和截止日期
                if modify_date == cutoff_date_str or modify_date < cutoff_date_str:
                    # 删除文件夹
                    shutil.rmtree(folder_dir)
                    deleted_folders.append(folder_dir)

        # 更新删除时间点
        if deleted_folders:
            save_config(folder_path, cutoff_date_str, folder_prefix)  # 保存删除时间点到配置文件
            messagebox.showinfo("完成", f"已删除以下文件夹:\n" + "\n".join(deleted_folders))
        else:
            messagebox.showinfo("完成", "没有找到符合条件的文件夹。")
    except Exception as e:
        messagebox.showerror("错误", f"发生错误: {e}")


def browse_folder():
    folder_path = filedialog.askdirectory(title="选择目标文件夹")
    if folder_path:
        folder_path_entry.delete(0, tk.END)
        folder_path_entry.insert(0, folder_path)


def update_time():
    # 实时更新当前时间标签
    current_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    current_date_label.config(text=f"当前日期: {current_time}")

    # 每秒钟更新一次
    root.after(1000, update_time)


def show_contact_info():
    # 弹出联系我们的信息框
    messagebox.showinfo("联系我们",
                        "技术支持：杜先生\n"
                        "联系方式：15100578801（微信同号）")


# 创建主窗口
root = tk.Tk()
root.title("删除旧文件夹")

# 设置窗口尺寸
root.geometry("450x400")
root.resizable(False, False)

# 设置标题标签
title_label = tk.Label(root, text="删除旧文件夹", font=("Arial", 16, "bold"), bg="#4CAF50", fg="white")
title_label.pack(fill=tk.X, pady=10)

# 文件夹路径标签和输入框
folder_path_frame = tk.Frame(root)
folder_path_frame.pack(pady=5)

folder_path_label = tk.Label(folder_path_frame, text="选择文件夹路径:", font=("Arial", 12))
folder_path_label.pack(side=tk.LEFT)

folder_path_entry = tk.Entry(folder_path_frame, width=30, font=("Arial", 12))
folder_path_entry.pack(side=tk.LEFT, padx=5)

# 浏览按钮
browse_button = tk.Button(folder_path_frame, text="浏览", command=browse_folder, font=("Arial", 10), bg="#4CAF50",
                          fg="white")
browse_button.pack(side=tk.LEFT)

# 如果有默认路径，填充进去
default_folder, last_deleted_date, default_prefix = load_config()
if default_folder:
    folder_path_entry.insert(0, default_folder)

# 默认路径复选框
default_path_var = tk.BooleanVar(value=bool(default_folder))
default_path_check = tk.Checkbutton(root, text="设为默认路径", variable=default_path_var, font=("Arial", 12))
default_path_check.pack(pady=5)

# 文件夹前缀标签和输入框
prefix_label = tk.Label(root, text="文件夹前缀 (默认为 'pack'):", font=("Arial", 12))
prefix_label.pack(pady=5)

prefix_entry = tk.Entry(root, width=20, font=("Arial", 12))
prefix_entry.pack(pady=5)

# 如果有默认前缀，填充进去
prefix_entry.insert(0, default_prefix)

# 删除天数标签和输入框
delete_days_label = tk.Label(root, text="删除多少天前的文件夹 (0表示今天):", font=("Arial", 12))
delete_days_label.pack(pady=5)

delete_days_entry = tk.Entry(root, width=10, font=("Arial", 12))
delete_days_entry.pack(pady=5)

# 当前日期标签
current_date_label = tk.Label(root, text=f"当前日期: {datetime.today().strftime('%Y-%m-%d %H:%M:%S')}",
                              font=("Arial", 12))
current_date_label.pack(pady=5)

# 确认删除按钮
delete_button = tk.Button(root, text="确定删除", command=delete_old_folders, font=("Arial", 12), bg="#FF6347",
                          fg="white")
delete_button.pack(pady=20)

# 联系我们按钮
contact_button = tk.Button(root, text="联系我们", command=show_contact_info, font=("Arial",8), bg="#2196F3",
                           fg="white")
contact_button.pack(pady=10)

# 启动实时更新时间
update_time()

# 运行主界面
root.mainloop()
