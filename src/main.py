"""
@file main.py
@brief 应用程序的主入口文件
@details
此模块包含了应用程序的主入口点，负责启动多功能计算器应用程序。应用程序的图形用户界面（GUI）由 `gui.py` 模块中的 `EquationSolverApp` 类实现。

@version 1.0
@date 2024-06-02
"""

import tkinter as tk
from gui import EquationSolverApp

if __name__ == "__main__":
    root = tk.Tk()
    app = EquationSolverApp(root)
    root.mainloop()



