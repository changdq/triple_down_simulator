import tkinter as tk

root = tk.Tk()
root.title("Grid Layout Example")
root.geometry("300x200")

# 创建标签和按钮
label1 = tk.Label(root, text="Label 1")
label2 = tk.Label(root, text="Label 2")
button1 = tk.Button(root, text="Button 1")
button2 = tk.Button(root, text="Button 2")

# 使用 grid() 布局管理器
label1.grid(row=0, column=0)
label2.grid(row=0, column=1)
button1.grid(row=1, column=0)
button2.grid(row=1, column=1)

root.mainloop()
