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

@version 1.0
@date 2024-06-02
"""

import numpy as np
import sympy as sp
from scipy.optimize import fsolve


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
    # 这部分逻辑比较无脑，算是转空子了吧
    # 将表达式转换为字符串形式
    expr_str = str(expr)

    # 检查是否为单个指数项 a^x 形式，并且处理 e^x 特殊情况
    if "exp" in expr_str or "**" in expr_str:
        base, exp = expr.as_base_exp()
        if base == sp.E or base.is_number:
            # 直接返回空列表，因为 e^x = 0 和 a^x = 0 (a > 0) 没有实数根
            return verified_roots

    for root in roots:
        value = expr.subs(symbol, root)
        if abs(sp.N(value)) < tol:
            verified_roots.append(root)

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
