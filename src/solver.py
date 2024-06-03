"""
@file solver.py
@brief 包含用于求解方程和矩阵运算的函数模块
@details
此模块包含了一些用于求解线性方程组、多项式方程和非多项式方程的函数，以及一些矩阵运算函数。
这些函数包括：
- 使用 SymPy 求解线性方程组
- 使用 NumPy 的 roots 函数求解多项式的根
- 使用 SciPy 的 fsolve 函数求解非多项式的根
- 验证求出的根是否为方程的根
- 计算矩阵的行列式、逆矩阵、转置、秩、幂
- 计算两个矩阵的乘积
- 计算矩阵的特征值和特征向量
- 测试非线性方程和线性方程组的解是否满足方程
- 求解周期性函数的根

@version 1.0
@date 2024-06-02
"""

import numpy as np
import sympy as sp
from scipy.optimize import fsolve
import math
from utils import *
import matplotlib.pyplot as plt
from PIL import Image


def newton_raphson(f, df, x0, tol=1e-6, max_iter=1000):
    """
    Newton-Raphson method for finding roots of the equation f(x) = 0.

    Parameters:
    f: The function for which we are finding the root
    df: The derivative of the function f
    x0: Initial guess for the root
    tol: Tolerance for the root value
    max_iter: Maximum number of iterations

    Returns:
    x: The estimated root of the function
    iter_values: List of values of x during iteration
    """
    x = x0
    iter_values = [x0]
    for _ in range(max_iter):
        fx = f(x)
        dfx = df(x)
        if abs(dfx) < tol:
            raise ValueError("Derivative near zero; no convergence.")
        x_new = x - fx / dfx
        iter_values.append(x_new)
        if abs(x_new - x) < tol:
            return x_new, iter_values
        x = x_new
    raise ValueError("Maximum iterations exceeded; no convergence.")


def solve_and_visualize(expr, initial_guesses, filename='pic.png'):
    """
    Solve an equation using Newton-Raphson method for multiple initial guesses and visualize the process.

    Parameters:
    expr: The equation to solve (sympy expression)
    initial_guesses: List of initial guesses for the root
    """
    # Define the function and its derivative
    x = sp.symbols('x')
    f = sp.lambdify(x, expr, 'numpy')
    df = sp.lambdify(x, sp.diff(expr, x), 'numpy')

    plt.figure(figsize=(12, 8))

    for i, x0 in enumerate(initial_guesses):
        try:
            root, iter_values = newton_raphson(f, df, x0)
            print(f"Initial guess {x0}: Converged to root {root}")

            # Prepare data for plotting
            iter_steps = list(range(len(iter_values)))

            # Plot the iteration process
            plt.plot(iter_steps, iter_values, marker='o', linestyle='dashed',
                     label=f'Initial guess {x0}, root {root:.6f}')
        except ValueError as e:
            print(f"Initial guess {x0}: {e}")

    plt.xlabel('Iteration step')
    plt.ylabel('Root value')
    plt.title('Newton-Raphson Iteration for Multiple Initial Guesses')
    plt.legend()
    plt.grid(True)
    plt.savefig(filename)
    image = Image.open(filename)
    image.show()
    plt.show()


def solve_periodic_function(func, symbol, period, range_min=-10, range_max=10):
    """
    @brief 求解周期性函数的根
    @param func 方程的 lambda 函数
    @param symbol 方程中的变量符号
    @param period 函数的周期
    @param range_min 搜索范围的最小值
    @param range_max 搜索范围的最大值
    @return 周期性函数的根
    """
    roots = []
    initial_guesses = generate_initial_guesses(100, range_min, range_max)
    for guess in initial_guesses:
        try:
            root = fsolve(func, guess, xtol=1e-12, maxfev=10000)
            root_value = root[0]
            k = math.floor((range_min - root_value) / period)
            while k * period + root_value <= range_max:
                candidate_root = k * period + root_value
                if not any(np.isclose(candidate_root, r, atol=1e-5) for r in roots):
                    roots.append(candidate_root)
                k += 1
        except (ValueError, RuntimeWarning) as e:
            continue
    return roots


def solve_linear_system(equations, variables):
    """
    @brief 使用 SymPy 求解线性方程组。
    @param equations 线性方程表达式列表
    @param variables 变量列表
    @return 线性方程组的解或无穷多解的参数化形式
    @throw ValueError 当方程组无解时抛出异常
    """
    solutions = sp.linsolve(equations, variables)
    if not solutions:
        raise ValueError("方程组无解。")
    solution_list = list(solutions)
    if len(solution_list) == 1:
        return np.array(solution_list[0], dtype=float)
    else:
        return solution_list


def solve_polynomial(coeffs):
    """
    @brief 使用 NumPy 的 roots 函数求解多项式的根。
    @param coeffs 多项式的系数列表
    @return 多项式的根
    """
    roots = np.roots(coeffs)
    return roots


def solve_nonpolynomial(func, initial_guesses):
    """
    @brief 使用 SciPy 的 fsolve 函数求解非多项式的根。
    @param func 方程的 lambda 函数
    @param initial_guesses 初始猜测值的列表
    @return 非多项式方程的根
    """
    roots = []
    for guess in initial_guesses:
        try:
            root = fsolve(func, guess, xtol=1e-15, maxfev=10000)
            if not any(np.isclose(root, r, atol=1e-5) for r in roots):
                roots.append(root[0])
        except (ValueError, RuntimeWarning):
            continue
    return np.array(roots)


# def verify_roots(roots, expr, symbol, tol=1e-6):
#     """
#     @brief 验证求出的根是否为方程的根。
#     @param roots 求出的根
#     @param expr 方程表达式
#     @param symbol 方程中的变量符号
#     @param tol 验证的容差
#     @return 仅包含验证通过的根列表
#     """
#     verified_roots = []
#     # 这部分逻辑比较无脑，算是转空子了吧
#     # 将表达式转换为字符串形式
#     expr_str = str(expr)
#
#     # 检查是否为单个指数项 a^x 形式，并且处理 e^x 特殊情况
#     if "exp" in expr_str or "**" in expr_str:
#         base, exp = expr.as_base_exp()
#         if base == sp.E or base.is_number:
#             # 直接返回空列表，因为 e^x = 0 和 a^x = 0 (a > 0) 没有实数根
#             return verified_roots
#
#     for root in roots:
#         value = expr.subs(symbol, root)
#         if abs(sp.N(value)) < tol:
#             verified_roots.append(root)
#
#     return verified_roots

def verify_roots(roots, expr, symbol, tol=1e-6):
    """
    @brief 验证求出的根是否为方程的根。
    @param roots 求出的根
    @param expr 方程表达式
    @param symbol 方程中的变量符号
    @param tol 验证的容差
    @return 仅包含验证通过的根列表
    """
    verified_roots = []
    expr_str = str(expr)

    # 检查是否为单个指数项 a^x 形式，并且处理 e^x 特殊情况
    if "exp" in expr_str or "**" in expr_str:
        base, exp = expr.as_base_exp()
        if base == sp.E or base.is_number:
            # 直接返回空列表，因为 e^x = 0 和 a^x = 0 (a > 0) 没有实数根
            return verified_roots

    for root in roots:
        try:
            value = expr.subs(symbol, root)
            if abs(sp.N(value)) < tol:
                verified_roots.append(root)
        except (TypeError, ValueError):
            continue

    # 针对特殊函数的特殊处理
    expr_str = str(expr)
    if "acos" in expr_str:
        special_roots = [1, -1]
        for special_root in special_roots:
            if abs(sp.N(expr.subs(symbol, special_root))) < tol and special_root not in verified_roots:
                verified_roots.append(special_root)
    if "asin" in expr_str:
        special_roots = [0, 1, -1]
        for special_root in special_roots:
            if abs(sp.N(expr.subs(symbol, special_root))) < tol and special_root not in verified_roots:
                verified_roots.append(special_root)
    if "arccot" in expr_str or "cot" in expr_str:
        special_roots = [0, sp.oo, -sp.oo]
        for special_root in special_roots:
            if abs(sp.N(expr.subs(symbol, special_root))) < tol and special_root not in verified_roots:
                verified_roots.append(special_root)
    if "arctan" in expr_str:
        special_roots = [0]
        for special_root in special_roots:
            if abs(sp.N(expr.subs(symbol, special_root))) < tol and special_root not in verified_roots:
                verified_roots.append(special_root)

    return verified_roots


def calculate_determinant(matrix):
    """
    @brief 计算矩阵的行列式。
    @param matrix 输入的矩阵
    @return 矩阵的行列式
    """
    return sp.Matrix(matrix).det()


def calculate_inverse(matrix):
    """
    @brief 计算矩阵的逆矩阵。
    @param matrix 输入的矩阵
    @return 矩阵的逆矩阵
    """
    return sp.Matrix(matrix).inv()


def calculate_transpose(matrix):
    """
    @brief 计算矩阵的转置。
    @param matrix 输入的矩阵
    @return 矩阵的转置
    """
    return sp.Matrix(matrix).T


def calculate_rank(matrix):
    """
    @brief 计算矩阵的秩。
    @param matrix 输入的矩阵
    @return 矩阵的秩
    """
    return sp.Matrix(matrix).rank()


def matrix_power(matrix, power):
    """
    @brief 计算矩阵的幂。
    @param matrix 输入的矩阵
    @param power 幂次
    @return 矩阵的幂
    """
    return sp.Matrix(matrix) ** power


def multiply_matrices(matrix1, matrix2):
    """
    @brief 计算两个矩阵的乘积。
    @param matrix1 第一个矩阵
    @param matrix2 第二个矩阵
    @return 两个矩阵的乘积
    """
    return sp.Matrix(matrix1) * sp.Matrix(matrix2)


def calculate_eigenvalues_and_vectors(matrix):
    """
    @brief 计算矩阵的特征值和特征向量。
    @param matrix 输入的矩阵
    @return 特征值和特征向量的列表
    """
    eigensystem = sp.Matrix(matrix).eigenvals()
    eigenvalues = list(eigensystem.keys())
    eigenvectors = [sp.Matrix(matrix).eigenvects()[i][2][0] for i in range(len(eigenvalues))]
    return eigenvalues, eigenvectors


def test_nonlinear_solution(expr, symbol, solutions, tol=1e-6):
    """
    @brief 测试非线性方程的根是否满足方程。
    @param expr 方程表达式
    @param symbol 方程中的变量符号
    @param solutions 求得的根列表
    @param tol 容差
    @return 测试结果字典，键为根，值为布尔值，表示是否满足方程
    """
    results = {}
    for sol in solutions:
        results[sol] = abs(sp.N(expr.subs(symbol, sol))) < tol
    return results


def test_linear_solution(coefficients, constants, solutions, tol=1e-6):
    """
    @brief 测试线性方程组的解是否满足方程组。
    @param coefficients 系数矩阵
    @param constants 常数向量
    @param solutions 求得的解列表
    @param tol 容差
    @return 测试结果字典，键为方程编号，值为布尔值，表示是否满足方程
    """
    results = {}
    for i, (row, const) in enumerate(zip(coefficients, constants)):
        equation_value = sum(coeff * sol for coeff, sol in zip(row, solutions))
        results[i + 1] = abs(equation_value - const) < tol
    return results
