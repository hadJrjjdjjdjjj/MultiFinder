"""
@file utils.py
@brief 包含辅助函数的工具模块
@details
此模块包含了一些辅助函数，用于在其他模块中使用。这些函数包括：
- 在输出区域显示矩阵
- 格式化数字
- 预处理用户输入的方程表达式
- 解析用户输入的方程表达式
- 生成初始猜测值

@version 1.0
@date 2024-06-02
"""

import tkinter as tk
import sympy as sp
import numpy as np


def display_matrix_in_output(output_text, matrix):
    """
    @brief 在输出区域显示矩阵
    @param matrix 矩阵
    :param output_text:
    :param output_text:
    """
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    for row in matrix:
        row_str = "\t".join(format_number(num) for num in row)
        output_text.insert(tk.END, f"{row_str}\n")
    output_text.config(state=tk.DISABLED)


def format_number(num):
    """
    @brief 格式化数字
    @param num 数字
    @return 格式化后的字符串
    """
    if num == int(num):
        return str(int(num))
    else:
        return f"{num:.6f}"


def preprocess_expression(expression):
    """
    @brief 预处理用户输入的方程表达式，确保格式正确。
    @param expression 方程表达式字符串
    @return 预处理后的表达式字符串
    """
    expression = expression.replace('−', '-')
    expression = expression.replace('×', '*')
    expression = expression.replace(' ', '')
    expression = expression.replace('e', str(sp.E))
    processed_expr = ''
    for i in range(len(expression)):
        if expression[i].isalpha() and i > 0 and (expression[i - 1].isdigit() or expression[i - 1] == ')'):
            processed_expr += '*' + expression[i]
        else:
            processed_expr += expression[i]
    return processed_expr


def parse_expression(expression):
    """
    @brief解析用户输入的方程表达式，并转换为一个可求解的函数。
    @param expression 方程表达式字符串
    @return 一个包含 SymPy 表达式、符号变量、多项式系数列表（如果是多项式方程）、是否为多项式的元组
    @throw ValueError 当方程中变量数量不为一个时抛出异常
    """
    expression = preprocess_expression(expression)

    if '=' in expression:
        left, right = expression.split('=')
        expression = f'({left}) - ({right})'

    symbols = list(sp.sympify(expression).free_symbols)
    if len(symbols) != 1:
        raise ValueError("方程中必须包含且仅包含一个变量。")

    symbol = symbols[0]
    expr = sp.sympify(expression)

    try:
        poly = sp.Poly(expr, symbol)
        coeffs = poly.all_coeffs()
        return expr, symbol, coeffs, True
    except sp.PolynomialError:
        return expr, symbol, None, False


def generate_initial_guesses(n, range_min=0.1, range_max=10):
    """
    @brief 生成初始猜测值，范围不包括无效值 (如对数函数的非正数输入)。
    @param n 初始猜测值的数量
    @param range_min 范围最小值 (默认值为 0.1)
    @param range_max 范围最大值 (默认值为 10)
    @return 初始猜测值列表
    """
    return np.linspace(range_min, range_max, n)
