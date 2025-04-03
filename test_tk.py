import tkinter as tk

# 最终怀疑是我的MacOs对tcl/tk的渲染有问题，放弃用这个库做界面

root = tk.Tk()
root.title("背景色测试")
root.geometry("400x300")

# 测试1：直接设置root背景（修复后应生效）
#root.tk.call("::tk::unsupported::MacWindowStyle", "style", root, "plain")
root.configure(bg="#FFE4B5")  # 珊瑚色


# 测试2：用Frame覆盖背景（验证子组件继承）
frame = tk.Frame(root, bg="#00FF00", width=200, height=200)  # 绿色块
frame.pack(pady=50)

# 测试3：显示颜色值（用Label显示RGB）
color_label = tk.Label(
    root,
    text=f"#FFE4B5",
    bg="#FFE4B5",
    fg="#333",
    font=("Courier New", 18)
)
color_label.pack()

root.mainloop()