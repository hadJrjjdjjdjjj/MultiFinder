"""
@file gui.py
@brief 多功能计算器应用程序的图形用户界面模块
@details
此模块包含了多功能计算器应用程序的图形用户界面（GUI）。它提供了用户交互界面，用于输入方程、选择运算类型，并显示计算结果。
主要功能包括：
- 非线性方程求解
- 线性方程组求解
- 矩阵运算（行列式、逆矩阵、转置、秩、幂、特征值和特征向量等）
- 历史记录查看

@version 1.0
@date 2024-06-02
"""

import tkinter as tk

import numpy as np

from solver import *
import sympy as sp
from utils import *
from historyManager import HistoryManager
from PIL import Image, ImageTk


class EquationSolverApp:
    """
    @brief 多功能计算器应用程序类
    """

    def __init__(self, root):
        """
        @brief 初始化EquationSolverApp类
        @param root 根窗口
        """
        self.history_button = None
        self.history_manager = None
        self.multiply_radio = None
        self.power_radio = None
        self.rank_radio = None
        self.transpose_radio = None
        self.inverse_radio = None
        self.determinant_radio = None
        self.operation = None
        self.operation_label = None
        self.operation_frame = None
        self.multiply_a_col_entry = None
        self.multiply_b_col_entry = None
        self.multiply_b_label = None
        self.multiply_a_row_entry = None
        self.multiply_a_label = None
        self.matrix_multiply_frame = None
        self.eigen_radio = None
        self.button_frame = None
        self.solve_button = None
        self.solve_newton_button = None
        self.test_button = None
        self.clear_button = None
        self.quit_button = None
        self.output_frame = None
        self.output_label = None
        self.output_text = None
        self.matrix_power_frame = None
        self.power_entry = None
        self.multiply_button = None
        self.power_label = None
        self.matrix_frame = None
        self.matrix_row_col_button = None
        self.matrix_col_entry = None
        self.matrix_dim_button = None
        self.matrix_dim_entry = None
        self.linear_var_entry = None
        self.matrix_dim_label = None
        self.matrix_col_label = None
        self.linear_dim_button = None
        self.matrix_row_entry = None
        self.linear_var_label = None
        self.linear_dim_frame = None
        self.equation_text = None
        self.matrix_row_col_frame = None
        self.matrix_row_label = None
        self.equation_label = None
        self.input_frame = None
        self.matrix_radio = None
        self.linear_radio = None
        self.nonlinear_radio = None
        self.mode_frame = None
        self.matrix_dim_frame = None
        self.linear_frame = None
        self.root = root
        self.root.title("多功能计算器")
        self.create_widgets()
        self.update_ui()  # 初始化时调用一次更新UI以设置默认状态
        self.history_manager = HistoryManager()  # 初始化历史记录管理器
        self.clear_history_button = None
        self.output_text.tag_config("error", foreground="red")  # 配置错误文本样式

    def create_widgets(self):
        """
        @brief 创建应用程序的所有控件
        """
        self.mode = tk.StringVar(value="nonlinear")  # 设置默认模式为非线性方程

        self.mode_frame = tk.Frame(self.root, bg="lightblue")
        self.mode_frame.pack(pady=10)

        self.nonlinear_radio = tk.Radiobutton(self.mode_frame, text="非线性方程求根", variable=self.mode,
                                              value="nonlinear", command=self.update_ui, bg="lightblue")
        self.nonlinear_radio.pack(side=tk.LEFT, padx=10)
        self.linear_radio = tk.Radiobutton(self.mode_frame, text="线性方程组求解", variable=self.mode,
                                           value="linear", command=self.update_ui, bg="lightblue")
        self.linear_radio.pack(side=tk.LEFT, padx=10)
        self.matrix_radio = tk.Radiobutton(self.mode_frame, text="矩阵运算", variable=self.mode,
                                           value="matrix", command=self.update_ui, bg="lightblue")
        self.matrix_radio.pack(side=tk.LEFT, padx=10)

        self.input_frame = tk.Frame(self.root, bg="lightgrey")
        self.input_frame.pack(pady=10)

        self.equation_label = tk.Label(self.input_frame, text="请输入非线性方程表达式", bg="lightgrey")
        self.equation_label.pack()

        self.equation_text = tk.Text(self.input_frame, width=50, height=10, bg="white", fg="black")
        self.equation_text.pack()

        self.linear_dim_frame = tk.Frame(self.input_frame, bg="lightgrey")
        self.linear_var_label = tk.Label(self.linear_dim_frame, text="请输入变量个数：", bg="lightgrey")
        self.linear_var_label.pack(side=tk.LEFT)
        self.linear_var_entry = tk.Entry(self.linear_dim_frame, width=5, bg="white", fg="black")
        self.linear_var_entry.pack(side=tk.LEFT)
        self.linear_dim_button = tk.Button(self.linear_dim_frame, text="确定", command=self.create_linear_entries,
                                           bg="lightblue")
        self.linear_dim_button.pack(side=tk.LEFT)
        self.linear_dim_frame.pack(pady=10)

        self.linear_frame = tk.Frame(self.input_frame, bg="lightgrey")

        self.matrix_dim_frame = tk.Frame(self.input_frame, bg="lightgrey")
        self.matrix_dim_label = tk.Label(self.matrix_dim_frame, text="请输入方阵维度：", bg="lightgrey")
        self.matrix_dim_label.pack(side=tk.LEFT)
        self.matrix_dim_entry = tk.Entry(self.matrix_dim_frame, width=5, bg="white", fg="black")
        self.matrix_dim_entry.pack(side=tk.LEFT)
        self.matrix_dim_button = tk.Button(self.matrix_dim_frame, text="确定", command=self.create_matrix_entries,
                                           bg="lightblue")
        self.matrix_dim_button.pack(side=tk.LEFT)
        self.matrix_dim_frame.pack(pady=10)

        self.matrix_row_col_frame = tk.Frame(self.input_frame, bg="lightgrey")
        self.matrix_row_label = tk.Label(self.matrix_row_col_frame, text="请输入矩阵行数：", bg="lightgrey")
        self.matrix_row_label.pack(side=tk.LEFT)
        self.matrix_row_entry = tk.Entry(self.matrix_row_col_frame, width=5, bg="white", fg="black")
        self.matrix_row_entry.pack(side=tk.LEFT)
        self.matrix_col_label = tk.Label(self.matrix_row_col_frame, text="请输入矩阵列数：", bg="lightgrey")
        self.matrix_col_label.pack(side=tk.LEFT)
        self.matrix_col_entry = tk.Entry(self.matrix_row_col_frame, width=5, bg="white", fg="black")
        self.matrix_col_entry.pack(side=tk.LEFT)
        self.matrix_row_col_button = tk.Button(self.matrix_row_col_frame, text="确定",
                                               command=self.create_non_square_matrix_entries, bg="lightblue")
        self.matrix_row_col_button.pack(side=tk.LEFT)
        self.matrix_row_col_frame.pack(pady=10)

        self.matrix_frame = tk.Frame(self.input_frame, bg="lightgrey")
        self.matrix_power_frame = tk.Frame(self.input_frame, bg="lightgrey")
        self.power_label = tk.Label(self.matrix_power_frame, text="请输入矩阵幂次：", bg="lightgrey")
        self.power_label.pack(side=tk.LEFT)
        self.power_entry = tk.Entry(self.matrix_power_frame, width=5, bg="white", fg="black")
        self.power_entry.pack(side=tk.LEFT)

        self.matrix_multiply_frame = tk.Frame(self.input_frame, bg="lightgrey")
        self.multiply_a_label = tk.Label(self.matrix_multiply_frame, text="请输入A矩阵的行数和列数：", bg="lightgrey")
        self.multiply_a_label.pack(side=tk.LEFT)
        self.multiply_a_row_entry = tk.Entry(self.matrix_multiply_frame, width=5, bg="white", fg="black")
        self.multiply_a_row_entry.pack(side=tk.LEFT)
        self.multiply_a_col_entry = tk.Entry(self.matrix_multiply_frame, width=5, bg="white", fg="black")
        self.multiply_a_col_entry.pack(side=tk.LEFT)
        self.multiply_b_label = tk.Label(self.matrix_multiply_frame, text="请输入B矩阵的列数：", bg="lightgrey")
        self.multiply_b_label.pack(side=tk.LEFT)
        self.multiply_b_col_entry = tk.Entry(self.matrix_multiply_frame, width=5, bg="white", fg="black")
        self.multiply_b_col_entry.pack(side=tk.LEFT)
        self.multiply_button = tk.Button(self.matrix_multiply_frame, text="确定",
                                         command=self.create_matrix_multiply_entries, bg="lightblue")
        self.multiply_button.pack(side=tk.LEFT)

        self.operation_frame = tk.Frame(self.input_frame, bg="lightgrey")
        self.operation_frame.pack(pady=10)

        self.operation_label = tk.Label(self.operation_frame, text="请选择矩阵运算：", bg="lightgrey")
        self.operation_label.pack(side=tk.LEFT)
        self.operation = tk.StringVar(value="determinant")
        self.determinant_radio = tk.Radiobutton(self.operation_frame, text="求行列式", variable=self.operation,
                                                value="determinant", command=self.update_ui, bg="lightgrey")
        self.determinant_radio.pack(side=tk.LEFT, padx=5)
        self.inverse_radio = tk.Radiobutton(self.operation_frame, text="求逆矩阵", variable=self.operation,
                                            value="inverse", command=self.update_ui, bg="lightgrey")
        self.inverse_radio.pack(side=tk.LEFT, padx=5)
        self.transpose_radio = tk.Radiobutton(self.operation_frame, text="求转置矩阵", variable=self.operation,
                                              value="transpose", command=self.update_ui, bg="lightgrey")
        self.transpose_radio.pack(side=tk.LEFT, padx=5)
        self.rank_radio = tk.Radiobutton(self.operation_frame, text="求矩阵秩", variable=self.operation,
                                         value="rank", command=self.update_ui, bg="lightgrey")
        self.rank_radio.pack(side=tk.LEFT, padx=5)
        self.power_radio = tk.Radiobutton(self.operation_frame, text="求方阵幂", variable=self.operation,
                                          value="power", command=self.update_ui, bg="lightgrey")
        self.power_radio.pack(side=tk.LEFT, padx=5)
        self.multiply_radio = tk.Radiobutton(self.operation_frame, text="矩阵乘法", variable=self.operation,
                                             value="multiply", command=self.update_ui, bg="lightgrey")
        self.multiply_radio.pack(side=tk.LEFT, padx=5)
        self.eigen_radio = tk.Radiobutton(self.operation_frame, text="求特征值和特征向量", variable=self.operation,
                                          value="eigen", command=self.update_ui, bg="lightgrey")
        self.eigen_radio.pack(side=tk.LEFT, padx=5)

        self.button_frame = tk.Frame(self.root, bg="lightgrey")

        self.solve_button = tk.Menubutton(self.button_frame, text="求解", bg="lightgreen", activebackground="lightgreen")
        self.solve_button.pack(side=tk.LEFT, padx=10)
        filemenu = tk.Menu(self.solve_button, tearoff=False)
        filemenu.add_command(label='内置方法', command=self.solve)
        filemenu.add_command(label='牛顿法', command=self.solve_newton)
        # 在此处添加方法
        filemenu.add_command(label='其他')
        self.solve_button.config(menu=filemenu)
        # self.solve_button = tk.Button(self.button_frame, text="求解", command=self.solve, bg="lightgreen")
        # self.solve_button.pack(side=tk.LEFT, padx=10)

        self.test_button = tk.Button(self.button_frame, text="测试验证", command=self.test_solution, bg="lightblue")
        self.test_button.pack(side=tk.LEFT, padx=10)

        self.clear_button = tk.Button(self.button_frame, text="清空输入输出", command=self.clear_text, bg="lightcoral")
        self.clear_button.pack(side=tk.LEFT, padx=10)

        self.quit_button = tk.Button(self.button_frame, text="退出", command=self.root.quit, bg="lightpink")
        self.quit_button.pack(side=tk.LEFT, padx=10)

        self.history_button = tk.Button(self.button_frame, text="显示历史记录", command=self.show_history,
                                        bg="lightyellow")
        self.history_button.pack(side=tk.RIGHT, padx=10)

        self.clear_history_button = tk.Button(self.button_frame, text="清空历史记录", command=self.clear_history,
                                              bg="lightgray")
        self.clear_history_button.pack(side=tk.RIGHT, padx=10)

        self.button_frame.pack(pady=10)

        self.output_frame = tk.Frame(self.root, bg="lightgrey")
        self.output_label = tk.Label(self.output_frame, text="输出结果", bg="lightgrey")
        self.output_label.pack()

        self.output_text = tk.Text(self.output_frame, width=50, height=10, state=tk.DISABLED, bg="white", fg="black")
        self.output_text.pack()

        self.output_frame.pack()

    def update_ui(self):
        """
         @brief 根据选择的模式更新UI
         """
        self.clear_text()  # 切换模式时清空输入和输出区域
        self.equation_text.pack_forget()
        self.linear_dim_frame.pack_forget()
        self.linear_frame.pack_forget()
        self.matrix_dim_frame.pack_forget()
        self.matrix_frame.pack_forget()
        self.operation_frame.pack_forget()
        self.matrix_power_frame.pack_forget()
        self.matrix_multiply_frame.pack_forget()
        self.matrix_row_col_frame.pack_forget()

        self.test_button.pack_forget()
        self.history_button.pack_forget()

        if self.mode.get() == "nonlinear":
            self.equation_label.config(text="请输入非线性方程表达式")
            self.equation_text.pack()
            self.test_button.pack(side=tk.LEFT, padx=10)  # 确保测试验证按钮在非线性方程模式下可见
            self.history_button.pack(side=tk.LEFT, padx=10)  # 确保历史记录按钮在非线性方程模式下可见
        elif self.mode.get() == "linear":
            self.equation_label.config(text="请输入变量个数并填充系数矩阵")
            self.linear_dim_frame.pack()
            self.linear_frame.pack()
            self.test_button.pack(side=tk.LEFT, padx=10)  # 确保测试验证按钮在线性方程组模式下可见
            self.history_button.pack(side=tk.LEFT, padx=10)  # 确保历史记录按钮在线性方程组模式下可见
        else:
            self.equation_label.config(text="请选择运算类型")
            self.operation_frame.pack()
            operation = self.operation.get()
            if operation in ["determinant", "inverse", "power", "eigen"]:
                self.matrix_dim_frame.pack()
                if operation == "power":
                    self.matrix_power_frame.pack()
            elif operation in ["transpose", "rank"]:
                self.matrix_row_col_frame.pack()
            elif operation == "multiply":
                self.matrix_multiply_frame.pack()
            self.history_button.pack(side=tk.LEFT, padx=10)  # 确保历史记录按钮在矩阵运算模式下可见

    def clear_text(self):
        """
        @brief 清空输入和输出区域的文本
        """
        self.equation_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.DISABLED)
        self.linear_var_entry.delete(0, tk.END)
        self.matrix_dim_entry.delete(0, tk.END)
        self.multiply_a_row_entry.delete(0, tk.END)
        self.multiply_a_col_entry.delete(0, tk.END)
        self.multiply_b_col_entry.delete(0, tk.END)
        self.power_entry.delete(0, tk.END)
        self.matrix_row_entry.delete(0, tk.END)
        self.matrix_col_entry.delete(0, tk.END)
        for widget in self.linear_frame.winfo_children():
            widget.destroy()
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()

    def create_linear_entries(self):
        """
        @brief 创建线性方程组的输入项
        """
        self.clear_linear_entries()
        try:
            var_count = int(self.linear_var_entry.get())
            if var_count <= 0:
                raise ValueError("变量个数必须是正整数。")
            self.linear_entries = []
            for i in range(var_count):
                row_entries = []
                for j in range(var_count + 1):  # 最后一列为常数项
                    if j == var_count:
                        entry_label = tk.Label(self.linear_frame, text="常数项")
                    else:
                        entry_label = tk.Label(self.linear_frame, text=f"变量{j + 1}")
                    entry_label.grid(row=i * 2, column=j, padx=5, pady=5)
                    entry = tk.Entry(self.linear_frame, width=5)
                    entry.grid(row=i * 2 + 1, column=j, padx=5, pady=5)
                    entry.bind("<Up>",
                               lambda event, row=i, col=j: focus_previous_row(event, row, col, self.linear_entries))
                    entry.bind("<Down>",
                               lambda event, row=i, col=j: focus_next_row(event, row, col, self.linear_entries))
                    entry.bind("<Left>",
                               lambda event, row=i, col=j: focus_previous_col(event, row, col, self.linear_entries))
                    entry.bind("<Right>",
                               lambda event, row=i, col=j: focus_next_col(event, row, col, self.linear_entries))
                    row_entries.append(entry)
                self.linear_entries.append(row_entries)
            self.linear_frame.pack()
        except ValueError as e:
            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(tk.END, f"错误: {str(e)}\n")
            self.output_text.config(state=tk.DISABLED)

    def clear_linear_entries(self):
        """
        @brief 清空线性方程组的输入项
        """
        for widget in self.linear_frame.winfo_children():
            widget.destroy()

    def create_matrix_entries(self):
        """
        @brief 创建方阵的输入项
        """
        self.clear_matrix_entries()
        try:
            dim = int(self.matrix_dim_entry.get())
            if dim <= 0:
                raise ValueError("维度必须是正整数。")
            self.matrix_entries = []
            for i in range(dim):
                row_entries = []
                for j in range(dim):
                    entry_label = tk.Label(self.matrix_frame, text=f"a{i + 1}{j + 1}")
                    entry_label.grid(row=i * 2, column=j, padx=5, pady=5)
                    entry = tk.Entry(self.matrix_frame, width=5)
                    entry.grid(row=i * 2 + 1, column=j, padx=5, pady=5)
                    entry.bind("<Up>",
                               lambda event, row=i, col=j: focus_previous_row(event, row, col, self.matrix_entries))
                    entry.bind("<Down>",
                               lambda event, row=i, col=j: focus_next_row(event, row, col, self.matrix_entries))
                    entry.bind("<Left>",
                               lambda event, row=i, col=j: focus_previous_col(event, row, col, self.matrix_entries))
                    entry.bind("<Right>",
                               lambda event, row=i, col=j: focus_next_col(event, row, col, self.matrix_entries))
                    row_entries.append(entry)
                self.matrix_entries.append(row_entries)
            self.matrix_frame.pack()
        except ValueError as e:
            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(tk.END, f"错误: {str(e)}\n")
            self.output_text.config(state=tk.DISABLED)

    def create_non_square_matrix_entries(self):
        """
        @brief 创建非方阵的输入项
        """

        self.clear_matrix_entries()
        try:
            rows = int(self.matrix_row_entry.get())
            cols = int(self.matrix_col_entry.get())
            if rows <= 0 or cols <= 0:
                raise ValueError("行数和列数必须是正整数。")
            self.matrix_entries = []
            for i in range(rows):
                row_entries = []
                for j in range(cols):
                    entry_label = tk.Label(self.matrix_frame, text=f"a{i + 1}{j + 1}")
                    entry_label.grid(row=i * 2, column=j, padx=5, pady=5)
                    entry = tk.Entry(self.matrix_frame, width=5)
                    entry.grid(row=i * 2 + 1, column=j, padx=5, pady=5)
                    entry.bind("<Up>",
                               lambda event, row=i, col=j: focus_previous_row(event, row, col, self.matrix_entries))
                    entry.bind("<Down>",
                               lambda event, row=i, col=j: focus_next_row(event, row, col, self.matrix_entries))
                    entry.bind("<Left>",
                               lambda event, row=i, col=j: focus_previous_col(event, row, col, self.matrix_entries))
                    entry.bind("<Right>",
                               lambda event, row=i, col=j: focus_next_col(event, row, col, self.matrix_entries))
                    row_entries.append(entry)
                self.matrix_entries.append(row_entries)
            self.matrix_frame.pack()
        except ValueError as e:
            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(tk.END, f"错误: {str(e)}\n")
            self.output_text.config(state=tk.DISABLED)

    def clear_matrix_entries(self):
        """
        @brief 清空矩阵的输入项
        """
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()

    def create_matrix_multiply_entries(self):
        """
        @brief 创建矩阵乘法的输入项
        """
        self.clear_matrix_entries()
        try:
            a_rows = int(self.multiply_a_row_entry.get())
            a_cols = int(self.multiply_a_col_entry.get())
            b_cols = int(self.multiply_b_col_entry.get())
            if a_rows <= 0 or a_cols <= 0 or b_cols <= 0:
                raise ValueError("行数和列数必须是正整数。")
            self.matrix_a_entries = []
            self.matrix_b_entries = []
            for i in range(a_rows):
                row_entries = []
                for j in range(a_cols):
                    entry_label = tk.Label(self.matrix_frame, text=f"A{i + 1}{j + 1}")
                    entry_label.grid(row=i * 2, column=j, padx=5, pady=5)
                    entry = tk.Entry(self.matrix_frame, width=5)
                    entry.grid(row=i * 2 + 1, column=j, padx=5, pady=5)
                    entry.bind("<Up>",
                               lambda event, row=i, col=j: focus_previous_row(event, row, col, self.matrix_a_entries))
                    entry.bind("<Down>",
                               lambda event, row=i, col=j: focus_next_row(event, row, col, self.matrix_a_entries))
                    entry.bind("<Left>",
                               lambda event, row=i, col=j: focus_previous_col(event, row, col, self.matrix_a_entries))
                    entry.bind("<Right>",
                               lambda event, row=i, col=j: focus_next_col(event, row, col, self.matrix_a_entries))
                    row_entries.append(entry)
                self.matrix_a_entries.append(row_entries)
            for i in range(a_cols):
                row_entries = []
                for j in range(b_cols):
                    entry_label = tk.Label(self.matrix_frame, text=f"B{i + 1}{j + 1}")
                    entry_label.grid(row=i * 2 + a_rows * 2, column=j, padx=5, pady=5)
                    entry = tk.Entry(self.matrix_frame, width=5)
                    entry.grid(row=i * 2 + 1 + a_rows * 2, column=j, padx=5, pady=5)
                    entry.bind("<Up>",
                               lambda event, row=i, col=j: focus_previous_row(event, row, col, self.matrix_b_entries))
                    entry.bind("<Down>",
                               lambda event, row=i, col=j: focus_next_row(event, row, col, self.matrix_b_entries))
                    entry.bind("<Left>",
                               lambda event, row=i, col=j: focus_previous_col(event, row, col, self.matrix_b_entries))
                    entry.bind("<Right>",
                               lambda event, row=i, col=j: focus_next_col(event, row, col, self.matrix_b_entries))
                    row_entries.append(entry)
                self.matrix_b_entries.append(row_entries)
            self.matrix_frame.pack()
        except ValueError as e:
            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(tk.END, f"错误: {str(e)}\n")
            self.output_text.config(state=tk.DISABLED)

    def add_to_history(self, operation_type, expression, result):
        """
        @brief 添加运算到历史记录
        @param operation_type 运算类型 ("nonlinear", "linear", "matrix")
        @param expression 运算表达式或矩阵
        @param result 运算结果
        """
        self.history_manager.add_record(operation_type, expression, result)

    def show_history(self):
        """
        @brief 显示历史记录
        """
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        operation_type = self.mode.get()
        sub_operation = self.operation.get() if operation_type == "matrix" else None
        history = self.history_manager.get_history(operation_type, sub_operation)
        if history:
            for record in history:
                self.output_text.insert(tk.END, f"输入:\n{record['expression']}\n结果:\n{record['result']}\n\n")
        else:
            self.output_text.insert(tk.END, "无历史记录。")
        self.output_text.config(state=tk.DISABLED)

    def clear_history(self):
        """
        @brief 清空当前模式的历史记录
        """
        operation_type = self.mode.get()
        sub_operation = self.operation.get() if operation_type == "matrix" else None
        self.history_manager.clear_history(operation_type, sub_operation)
        self.show_history()

    def solve(self):
        """
        @brief 解决方程或矩阵运算，非法输入时抛出异常
        """
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)

        try:
            if self.mode.get() == "matrix":
                operation = self.operation.get()
                if operation == "multiply":
                    if not self.matrix_a_entries or not self.matrix_b_entries:
                        self.output_text.insert(tk.END, "错误: 矩阵A和矩阵B不能为空!\n", "error")
                        return
                    matrix_a = sp.Matrix(get_matrix_from_entries(self.matrix_a_entries))
                    matrix_b = sp.Matrix(get_matrix_from_entries(self.matrix_b_entries))
                    if matrix_a.shape[1] != matrix_b.shape[0]:
                        self.output_text.insert(tk.END, "错误: 矩阵A的列数必须等于矩阵B的行数!\n", "error")
                        return
                    result = matrix_a * matrix_b
                    display_matrix_in_output(self.output_text, result.tolist())
                    self.history_manager.add_record("matrix",
                                                    f"A:\n{format_matrix(matrix_a)}\nB:\n{format_matrix(matrix_b)}",
                                                    format_matrix(result), "multiply")
                else:
                    if not self.matrix_entries:
                        self.output_text.insert(tk.END, "错误: 矩阵不能为空!\n", "error")
                        return
                    matrix = sp.Matrix(get_matrix_from_entries(self.matrix_entries))
                    if operation == "determinant":
                        result = matrix.det()
                        self.output_text.insert(tk.END, f"行列式的结果为: {format_number(result)}")
                        self.history_manager.add_record("matrix", f"矩阵:\n{format_matrix(matrix)}",
                                                        format_number(result), "determinant")
                    elif operation == "inverse":
                        result = matrix.inv()
                        display_matrix_in_output(self.output_text, result.tolist())
                        self.history_manager.add_record("matrix", f"矩阵:\n{format_matrix(matrix)}",
                                                        format_matrix(result), "inverse")
                    elif operation == "transpose":
                        result = matrix.T
                        display_matrix_in_output(self.output_text, result.tolist())
                        self.history_manager.add_record("matrix", f"矩阵:\n{format_matrix(matrix)}",
                                                        format_matrix(result), "transpose")
                    elif operation == "rank":
                        result = matrix.rank()
                        self.output_text.insert(tk.END, f"矩阵秩的结果为: {format_number(result)}")
                        self.history_manager.add_record("matrix", f"矩阵:\n{format_matrix(matrix)}",
                                                        format_number(result), "rank")
                    elif operation == "power":
                        power = int(self.power_entry.get())
                        result = matrix ** power
                        display_matrix_in_output(self.output_text, result.tolist())
                        self.history_manager.add_record("matrix", f"矩阵:\n{format_matrix(matrix)}\n幂次: {power}",
                                                        format_matrix(result), "power")
                    elif operation == "eigen":
                        eigenvalues = matrix.eigenvals()
                        eigenvectors = matrix.eigenvects()
                        eigenvalues_str = "\n".join(
                            f"特征值 {format_number(key)}: 重数 {val}" for key, val in eigenvalues.items())
                        eigenvectors_str = "\n".join(
                            f"特征向量 {i + 1}: {', '.join(format_number(val) for val in vec)}"
                            for i, (val, mult, vecs) in enumerate(eigenvectors)
                            for vec in vecs)
                        self.output_text.insert(tk.END, f"特征值为:\n{eigenvalues_str}\n")
                        self.output_text.insert(tk.END, f"特征向量为:\n{eigenvectors_str}")
                        self.history_manager.add_record("matrix", f"矩阵:\n{format_matrix(matrix)}",
                                                        f"特征值: {eigenvalues_str}, 特征向量: {eigenvectors_str}",
                                                        "eigen")
            else:
                if self.mode.get() == "linear":
                    coefficients = []
                    constants = []
                    for row_entries in self.linear_entries:
                        if all(not entry.get() for entry in row_entries):
                            continue
                        row = []
                        for j, entry in enumerate(row_entries):
                            value = entry.get()
                            if value == "":
                                value = 0.0
                            else:
                                value = float(value)
                            if j == len(row_entries) - 1:
                                constants.append(value)
                            else:
                                row.append(value)
                        coefficients.append(row)
                    if not coefficients or not constants:
                        self.output_text.insert(tk.END, "错误: 方程组不能为空!\n", "error")
                        return

                    augmented_matrix = sp.Matrix([row + [const] for row, const in zip(coefficients, constants)])
                    coefficient_matrix = augmented_matrix[:, :-1]
                    rank_coefficient_matrix = coefficient_matrix.rank()
                    rank_augmented_matrix = augmented_matrix.rank()
                    num_variables = len(coefficients[0])

                    if rank_coefficient_matrix != rank_augmented_matrix:
                        self.output_text.insert(tk.END, "方程组无解。\n")
                        self.history_manager.add_record("linear",
                                                        f"系数矩阵:\n{format_matrix(coefficient_matrix)}\n常数项:\n{constants}",
                                                        "方程组无解")
                    elif rank_coefficient_matrix == num_variables:
                        solutions = sp.linsolve((coefficient_matrix, sp.Matrix(constants)),
                                                *sp.symbols(f'x1:{num_variables + 1}'))
                        solution = next(iter(solutions))
                        results_str = "方程组有唯一解:\n"
                        results_str += "\n".join(
                            [f"{symbol} = {format_number(value)}" for symbol, value in
                             zip(sp.symbols(f'x1:{num_variables + 1}'), solution)])  # 使用 format_number 格式化解
                        self.output_text.insert(tk.END, results_str)
                        self.history_manager.add_record("linear",
                                                        f"系数矩阵:\n{format_matrix(coefficient_matrix)}\n常数项:\n{constants}",
                                                        results_str)
                    else:
                        solutions = sp.linsolve((coefficient_matrix, sp.Matrix(constants)),
                                                *sp.symbols(f'x1:{num_variables + 1}'))
                        results_str = "方程组有无穷多解:\n"
                        for solution in solutions:
                            normalized_solution = [sp.simplify(value) for value in solution]
                            results_str += "\n".join(
                                [f"{symbol} = {value}" for symbol, value in
                                 zip(sp.symbols(f'x1:{num_variables + 1}'), normalized_solution)])
                            results_str += "\n"
                        self.output_text.insert(tk.END, results_str)
                        self.history_manager.add_record("linear",
                                                        f"系数矩阵:\n{format_matrix(coefficient_matrix)}\n常数项:\n{constants}",
                                                        results_str)
                else:
                    equations = []
                    equations_text = self.equation_text.get("1.0", tk.END).strip()
                    equations_lines = equations_text.splitlines()
                    if not equations_lines:
                        self.output_text.insert(tk.END, "错误: 非线性方程不能为空!\n", "error")
                        return
                    for line in equations_lines:
                        if '=' in line:
                            left, right = line.split('=')
                            eq = sp.sympify(preprocess_expression(f"({left}) - ({right})"))
                        else:
                            eq = sp.sympify(preprocess_expression(line))
                        equations.append(eq)

                    if self.mode.get() == "nonlinear" and len(equations) == 1:
                        expr, symbol, coeffs, is_polynomial = parse_expression(equations_lines[0])

                        if is_polynomial:
                            roots = solve_polynomial(coeffs)
                        else:
                            func = sp.lambdify(symbol, expr, 'numpy')
                            initial_guesses = generate_initial_guesses(50, -10, 10)
                            roots = solve_nonpolynomial(func, initial_guesses)

                        verified_roots = verify_roots(roots, expr, symbol)
                        if verified_roots:
                            results_str = "\n".join(
                                [f"{symbol}{i + 1}: {format_number(root.real)} + {format_number(root.imag)}i"
                                 if isinstance(root, complex) else f"{symbol}{i + 1}: {format_number(root)}"
                                 for i, root in enumerate(verified_roots)])
                            self.output_text.insert(tk.END, f"方程的根为:\n{results_str}")
                            self.history_manager.add_record("nonlinear", equations_lines[0], results_str)
                        else:
                            self.output_text.insert(tk.END, "方程没有实数根。\n")
                            self.history_manager.add_record("nonlinear", equations_lines[0], "方程没有实数根。")
                    else:
                        self.output_text.insert(tk.END, "错误: 请确保输入一个非线性方程!\n", "error")
                        return
        except Exception as e:
            self.output_text.insert(tk.END, f"错误: {str(e)}!\n", "error")

        self.output_text.config(state=tk.DISABLED)

    def solve_newton(self):
        """
        @brief 解决方程或矩阵运算，非法输入时抛出异常
        """
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)

        try:
            if self.mode.get() == "matrix":
                operation = self.operation.get()
                if operation == "multiply":
                    if not self.matrix_a_entries or not self.matrix_b_entries:
                        self.output_text.insert(tk.END, "错误: 矩阵A和矩阵B不能为空!\n", "error")
                        return
                    matrix_a = sp.Matrix(get_matrix_from_entries(self.matrix_a_entries))
                    matrix_b = sp.Matrix(get_matrix_from_entries(self.matrix_b_entries))
                    if matrix_a.shape[1] != matrix_b.shape[0]:
                        self.output_text.insert(tk.END, "错误: 矩阵A的列数必须等于矩阵B的行数!\n", "error")
                        return
                    result = matrix_a * matrix_b
                    display_matrix_in_output(self.output_text, result.tolist())
                    self.history_manager.add_record("matrix",
                                                    f"A:\n{format_matrix(matrix_a)}\nB:\n{format_matrix(matrix_b)}",
                                                    format_matrix(result), "multiply")
                else:
                    if not self.matrix_entries:
                        self.output_text.insert(tk.END, "错误: 矩阵不能为空!\n", "error")
                        return
                    matrix = sp.Matrix(get_matrix_from_entries(self.matrix_entries))
                    if operation == "determinant":
                        result = matrix.det()
                        self.output_text.insert(tk.END, f"行列式的结果为: {format_number(result)}")
                        self.history_manager.add_record("matrix", f"矩阵:\n{format_matrix(matrix)}",
                                                        format_number(result), "determinant")
                    elif operation == "inverse":
                        result = matrix.inv()
                        display_matrix_in_output(self.output_text, result.tolist())
                        self.history_manager.add_record("matrix", f"矩阵:\n{format_matrix(matrix)}",
                                                        format_matrix(result), "inverse")
                    elif operation == "transpose":
                        result = matrix.T
                        display_matrix_in_output(self.output_text, result.tolist())
                        self.history_manager.add_record("matrix", f"矩阵:\n{format_matrix(matrix)}",
                                                        format_matrix(result), "transpose")
                    elif operation == "rank":
                        result = matrix.rank()
                        self.output_text.insert(tk.END, f"矩阵秩的结果为: {format_number(result)}")
                        self.history_manager.add_record("matrix", f"矩阵:\n{format_matrix(matrix)}",
                                                        format_number(result), "rank")
                    elif operation == "power":
                        power = int(self.power_entry.get())
                        result = matrix ** power
                        display_matrix_in_output(self.output_text, result.tolist())
                        self.history_manager.add_record("matrix", f"矩阵:\n{format_matrix(matrix)}\n幂次: {power}",
                                                        format_matrix(result), "power")
                    elif operation == "eigen":
                        eigenvalues = matrix.eigenvals()
                        eigenvectors = matrix.eigenvects()
                        eigenvalues_str = "\n".join(
                            f"特征值 {format_number(key)}: 重数 {val}" for key, val in eigenvalues.items())
                        eigenvectors_str = "\n".join(
                            f"特征向量 {i + 1}: {', '.join(format_number(val) for val in vec)}"
                            for i, (val, mult, vecs) in enumerate(eigenvectors)
                            for vec in vecs)
                        self.output_text.insert(tk.END, f"特征值为:\n{eigenvalues_str}\n")
                        self.output_text.insert(tk.END, f"特征向量为:\n{eigenvectors_str}")
                        self.history_manager.add_record("matrix", f"矩阵:\n{format_matrix(matrix)}",
                                                        f"特征值: {eigenvalues_str}, 特征向量: {eigenvectors_str}",
                                                        "eigen")
            else:
                if self.mode.get() == "linear":
                    coefficients = []
                    constants = []
                    for row_entries in self.linear_entries:
                        if all(not entry.get() for entry in row_entries):
                            continue
                        row = []
                        for j, entry in enumerate(row_entries):
                            value = entry.get()
                            if value == "":
                                value = 0.0
                            else:
                                value = float(value)
                            if j == len(row_entries) - 1:
                                constants.append(value)
                            else:
                                row.append(value)
                        coefficients.append(row)
                    if not coefficients or not constants:
                        self.output_text.insert(tk.END, "错误: 方程组不能为空!\n", "error")
                        return

                    augmented_matrix = sp.Matrix([row + [const] for row, const in zip(coefficients, constants)])
                    coefficient_matrix = augmented_matrix[:, :-1]
                    rank_coefficient_matrix = coefficient_matrix.rank()
                    rank_augmented_matrix = augmented_matrix.rank()
                    num_variables = len(coefficients[0])

                    if rank_coefficient_matrix != rank_augmented_matrix:
                        self.output_text.insert(tk.END, "方程组无解。\n")
                        self.history_manager.add_record("linear",
                                                        f"系数矩阵:\n{format_matrix(coefficient_matrix)}\n常数项:\n{constants}",
                                                        "方程组无解")
                    elif rank_coefficient_matrix == num_variables:
                        solutions = sp.linsolve((coefficient_matrix, sp.Matrix(constants)),
                                                *sp.symbols(f'x1:{num_variables + 1}'))
                        solution = next(iter(solutions))
                        results_str = "方程组有唯一解:\n"
                        results_str += "\n".join(
                            [f"{symbol} = {format_number(value)}" for symbol, value in
                             zip(sp.symbols(f'x1:{num_variables + 1}'), solution)])  # 使用 format_number 格式化解
                        self.output_text.insert(tk.END, results_str)
                        self.history_manager.add_record("linear",
                                                        f"系数矩阵:\n{format_matrix(coefficient_matrix)}\n常数项:\n{constants}",
                                                        results_str)
                    else:
                        solutions = sp.linsolve((coefficient_matrix, sp.Matrix(constants)),
                                                *sp.symbols(f'x1:{num_variables + 1}'))
                        results_str = "方程组有无穷多解:\n"
                        for solution in solutions:
                            normalized_solution = [sp.simplify(value) for value in solution]
                            results_str += "\n".join(
                                [f"{symbol} = {value}" for symbol, value in
                                 zip(sp.symbols(f'x1:{num_variables + 1}'), normalized_solution)])
                            results_str += "\n"
                        self.output_text.insert(tk.END, results_str)
                        self.history_manager.add_record("linear",
                                                        f"系数矩阵:\n{format_matrix(coefficient_matrix)}\n常数项:\n{constants}",
                                                        results_str)
                else:
                    equations = []
                    equations_text = self.equation_text.get("1.0", tk.END).strip()
                    equations_lines = equations_text.splitlines()
                    if not equations_lines:
                        self.output_text.insert(tk.END, "错误: 非线性方程不能为空!\n", "error")
                        return
                    for line in equations_lines:
                        if '=' in line:
                            left, right = line.split('=')
                            eq = sp.sympify(preprocess_expression(f"({left}) - ({right})"))
                        else:
                            eq = sp.sympify(preprocess_expression(line))
                        equations.append(eq)

                    if self.mode.get() == "nonlinear" and len(equations) == 1:
                        expr, symbol, coeffs, is_polynomial = parse_expression(equations_lines[0])

                        if is_polynomial:
                            roots = solve_polynomial(coeffs)
                            initial_guesses = np.linspace(-25, 25, 15)
                            solve_and_visualize(expr, initial_guesses)

                            img_win = tk.Toplevel()
                            img = Image.open('pic.jpg')
                            tk_img = ImageTk.PhotoImage(img)

                            tk.Label(img_win, image=tk_img).pack()
                            img_win.mainloop()

                        else:
                            func = sp.lambdify(symbol, expr, 'numpy')
                            initial_guesses = generate_initial_guesses(50, -10, 10)
                            roots = solve_nonpolynomial(func, initial_guesses)
                            solve_and_visualize(expr, initial_guesses)

                            img_win = tk.Toplevel()
                            img = Image.open('pic.jpg')
                            tk_img = ImageTk.PhotoImage(img)

                            tk.Label(img_win, image=tk_img).pack()
                            img_win.mainloop()

                        verified_roots = verify_roots(roots, expr, symbol)
                        if verified_roots:
                            results_str = "\n".join(
                                [f"{symbol}{i + 1}: {format_number(root.real)} + {format_number(root.imag)}i"
                                 if isinstance(root, complex) else f"{symbol}{i + 1}: {format_number(root)}"
                                 for i, root in enumerate(verified_roots)])
                            self.output_text.insert(tk.END, f"方程的根为:\n{results_str}")
                            self.history_manager.add_record("nonlinear", equations_lines[0], results_str)
                        else:
                            self.output_text.insert(tk.END, "方程没有实数根。\n")
                            self.history_manager.add_record("nonlinear", equations_lines[0], "方程没有实数根。")
                    else:
                        self.output_text.insert(tk.END, "错误: 请确保输入一个非线性方程!\n", "error")
                        return
        except Exception as e:
            self.output_text.insert(tk.END, f"错误: {str(e)}!\n", "error")

        self.output_text.config(state=tk.DISABLED)

    def test_solution(self):
        """
        @brief 测试方程组或非线性方程的解是否正确
        """
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)

        try:
            if self.mode.get() == "linear":
                coefficients = []
                constants = []
                for row_entries in self.linear_entries:
                    row = []
                    for j, entry in enumerate(row_entries):
                        value = entry.get()
                        if j == len(row_entries) - 1:
                            if value == "":
                                value = "0"
                            try:
                                constants.append(float(value))
                            except ValueError:
                                raise ValueError("常数项必须是数字。")
                        else:
                            if value == "":
                                value = "0"
                            try:
                                row.append(float(value))
                            except ValueError:
                                raise ValueError("系数项必须是数字。")
                    coefficients.append(row)

                if not coefficients or not constants:
                    self.output_text.insert(tk.END, "错误: 方程组不能为空!\n", "error")
                    raise ValueError("方程组不能为空。")

                augmented_matrix = sp.Matrix([row + [const] for row, const in zip(coefficients, constants)])
                coefficient_matrix = augmented_matrix[:, :-1]
                rank_coefficient_matrix = coefficient_matrix.rank()
                rank_augmented_matrix = augmented_matrix.rank()
                num_variables = len(coefficients[0])

                if rank_coefficient_matrix != rank_augmented_matrix:
                    self.output_text.insert(tk.END, "错误: 无解，不可验证！\n", "error")
                else:
                    solutions = sp.linsolve((coefficient_matrix, sp.Matrix(constants)),
                                            *sp.symbols(f'x1:{num_variables + 1}'))
                    if len(solutions) == 0:
                        self.output_text.insert(tk.END, "错误: 无解，不可验证！\n", "error")
                    else:
                        all_passed = True
                        detailed_results = ""
                        for solution in solutions:
                            normalized_solution = [sp.simplify(value) for value in solution]
                            test_results = test_linear_solution(coefficients, constants, normalized_solution)
                            if not all(test_results.values()):
                                all_passed = False
                                failed_details = "\n".join(
                                    [f"根 {symbol} = {value} 未通过" for symbol, value, passed in
                                     zip(sp.symbols(f'x1:{num_variables + 1}'), normalized_solution,
                                         test_results.values())
                                     if not passed])
                                detailed_results += failed_details + "\n"
                        if all_passed:
                            self.output_text.insert(tk.END, "线性方程组测试结果: 全部通过\n")
                        else:
                            self.output_text.insert(tk.END, f"线性方程组测试结果: 有未通过\n{detailed_results}")

            elif self.mode.get() == "nonlinear":
                equations_text = self.equation_text.get("1.0", tk.END).strip()
                equations_lines = equations_text.splitlines()
                if len(equations_lines) != 1:
                    self.output_text.insert(tk.END, "错误: 无计算结果，请输入方程求解后再测试验证!\n", "error")
                    raise ValueError("无计算结果，请输入方程求解后再测试验证。")

                expr, symbol, coeffs, is_polynomial = parse_expression(equations_lines[0])
                if is_polynomial:
                    roots = solve_polynomial(coeffs)
                else:
                    func = sp.lambdify(symbol, expr, 'numpy')
                    initial_guesses = generate_initial_guesses(50, 0.1, 10)
                    roots = solve_nonpolynomial(func, initial_guesses)

                verified_roots = verify_roots(roots, expr, symbol)
                if not verified_roots:
                    self.output_text.insert(tk.END, "错误: 无实数根，不可验证！\n", "error")
                else:
                    test_results = test_nonlinear_solution(expr, symbol, verified_roots)
                    if all(test_results.values()):
                        self.output_text.insert(tk.END, "非线性方程测试结果: 全部通过\n")
                    else:
                        failed_details = "\n".join(
                            [f"根 {format_number(root)} 未通过" for root, passed in test_results.items() if
                             not passed])
                        self.output_text.insert(tk.END, f"非线性方程测试结果: 有未通过\n{failed_details}")

            else:
                self.output_text.insert(tk.END, "错误: 此功能仅适用于非线性方程和线性方程组的测试验证!\n", "error")

        except Exception as e:
            self.output_text.insert(tk.END, f"错误: {str(e)}!\n", "error")

        self.output_text.config(state=tk.DISABLED)
