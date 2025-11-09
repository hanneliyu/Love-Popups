import tkinter as tk
import random
import sys
import os

# 全局变量
exit_flag = False
all_windows = []
MAX_WINDOWS = 300  # 减少窗口数量，提高响应性
CREATE_INTERVAL = 100  # 增加创建间隔

def show_warm_tip():
    """创建单个提示窗口"""
    if exit_flag:
        return

    try:
        window = tk.Toplevel()  # 使用Toplevel而不是Tk
        all_windows.append(window)

        screen_w = window.winfo_screenwidth()
        screen_h = window.winfo_screenheight()
        win_w, win_h = 259, 60
        x = random.randrange(0, screen_w - win_w)
        y = random.randrange(0, screen_h - win_h)

        window.title("Love Message")
        window.geometry(f"{win_w}x{win_h}+{x}+{y}")
        window.attributes('-topmost', True)

        tips = ['🖕']

        tk.Label(
            window,
            text=random.choice(tips),
            font=('Arial', 40),
            width=3,
            height=3
        ).pack()

        # 绑定键盘事件到每个窗口
        window.bind('<Control-Alt-q>', lambda e: force_exit())
        window.bind('<Control-Alt-Q>', lambda e: force_exit())
        window.bind('<Control-c>', lambda e: force_exit())
        window.bind('<Control-C>', lambda e: force_exit())

        # 检查退出标志
        def check_exit():
            if exit_flag:
                try:
                    window.destroy()
                except:
                    pass
            else:
                window.after(50, check_exit)
        check_exit()

    except Exception as e:
        print(f"创建窗口出错: {e}")

def create_windows_periodically():
    """主线程定时创建窗口"""
    if exit_flag or len(all_windows) >= MAX_WINDOWS:
        return
    show_warm_tip()
    root.after(CREATE_INTERVAL, create_windows_periodically)

def force_exit():
    """强制退出程序"""
    global exit_flag
    if exit_flag:
        return

    print("正在退出程序...")
    exit_flag = True

    # 关闭所有窗口
    for win in all_windows:
        try:
            win.destroy()
        except:
            pass

    # 关闭主窗口
    try:
        root.quit()
        root.destroy()
    except:
        pass

    # 强制退出
    os._exit(0)

if __name__ == "__main__":
    # 初始化tkinter主窗口
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    # 设置15秒后自动退出（15000毫秒）
    root.after(15000, force_exit)

    # 在主窗口绑定全局快捷键
    root.bind('<Control-Alt-q>', lambda e: force_exit())
    root.bind('<Control-Alt-Q>', lambda e: force_exit())
    root.bind('<Control-c>', lambda e: force_exit())
    root.bind('<Control-C>', lambda e: force_exit())

    # 添加手动退出按钮
    exit_btn = tk.Button(
        root,
        text="Exit (Ctrl+Alt+Q)",
        command=force_exit,
        bg="red",
        fg="white",
        font=('Arial', 10)
    )
    exit_btn.pack(pady=10)
    # root.deiconify()  # 显示主窗口，方便退出

    # 定时创建窗口
    create_windows_periodically()

    try:
        root.mainloop()
    except Exception as e:
        print(f"Error: {e}")
        force_exit()