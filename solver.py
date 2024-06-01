import numpy as np
import sympy as sp
from scipy.optimize import fsolve

def preprocess_expression(expression):
    """
    预处理用户输入的方程表达式，确保格式正确。

    @param expression 方程表达式字符串
    @return 预处理后的表达式字符串
    """
    expression = expression.replace('−', '-')
    expression = expression.replace('×', '*')
    expression = expression.replace(' ', '')
    processed_expr = ''
    for i in range(len(expression)):
        if expression[i].isalpha() and i > 0 and (expression[i - 1].isdigit() or expression[i - 1] == ')'):
            processed_expr += '*' + expression[i]
        else:
            processed_expr += expression[i]
    return processed_expr

def parse_expression(expression):
    """
    解析用户输入的方程表达式，并转换为一个可求解的函数。

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

def solve_linear_system(equations, variables):
    """
    使用 SymPy 求解线性方程组。

    @param equations 线性方程表达式列表
    @param variables 变量列表
    @return 线性方程组的解
    @throw ValueError 当方程组无解时抛出异常
    """
    solutions = sp.linsolve(equations, variables)
    if not solutions:
        raise ValueError("方程组无解。")
    return np.array(list(solutions)[0], dtype=float)

def solve_polynomial(coeffs):
    """
    使用 NumPy 的 roots 函数求解多项式的根。

    @param coeffs 多项式的系数列表
    @return 多项式的根
    """
    roots = np.roots(coeffs)
    return roots

def solve_nonpolynomial(func, initial_guesses):
    """
    使用 SciPy 的 fsolve 函数求解非多项式的根。

    @param func 方程的 lambda 函数
    @param initial_guesses 初始猜测值的列表
    @return 非多项式方程的根
    """
    roots = []
    for guess in initial_guesses:
        try:
            root = fsolve(func, guess, xtol=1e-8, maxfev=1000)
            if not any(np.isclose(root, r, atol=1e-5) for r in roots):
                roots.append(root[0])
        except (ValueError, RuntimeWarning):
            continue
    return np.array(roots)

def generate_initial_guesses(n, range_min=0.1, range_max=10):
    """
    生成初始猜测值，范围不包括无效值 (如对数函数的非正数输入)。

    @param n 初始猜测值的数量
    @param range_min 范围最小值 (默认值为 0.1)
    @param range_max 范围最大值 (默认值为 10)
    @return 初始猜测值列表
    """
    return np.linspace(range_min, range_max, n)

def verify_roots(roots, expr, symbol, tol=1e-6):
    """
    验证求出的根是否为方程的根。

    @param roots 求出的根
    @param expr 方程表达式
    @param symbol 方程中的变量符号
    @param tol 验证的容差
    @return 仅包含验证通过的根列表
    """
    verified_roots = []
    for root in roots:
        value = expr.subs(symbol, root)
        if abs(sp.N(value)) < tol:
            verified_roots.append(root)
    return verified_roots

def calculate_determinant(matrix):
    """
    计算矩阵的行列式。

    @param matrix 输入的矩阵
    @return 矩阵的行列式
    """
    return sp.Matrix(matrix).det()

def calculate_inverse(matrix):
    """
    计算矩阵的逆矩阵。

    @param matrix 输入的矩阵
    @return 矩阵的逆矩阵
    """
    return sp.Matrix(matrix).inv()

def calculate_transpose(matrix):
    """
    计算矩阵的转置。

    @param matrix 输入的矩阵
    @return 矩阵的转置
    """
    return sp.Matrix(matrix).T

def calculate_rank(matrix):
    """
    计算矩阵的秩。

    @param matrix 输入的矩阵
    @return 矩阵的秩
    """
    return sp.Matrix(matrix).rank()

def matrix_power(matrix, power):
    """
    计算矩阵的幂。

    @param matrix 输入的矩阵
    @param power 幂次
    @return 矩阵的幂
    """
    return sp.Matrix(matrix)**power

def multiply_matrices(matrix1, matrix2):
    """
    计算两个矩阵的乘积。

    @param matrix1 第一个矩阵
    @param matrix2 第二个矩阵
    @return 两个矩阵的乘积
    """
    return sp.Matrix(matrix1) * sp.Matrix(matrix2)

def calculate_eigenvalues_and_vectors(matrix):
    """
    计算矩阵的特征值和特征向量。

    @param matrix 输入的矩阵
    @return 特征值和特征向量的列表
    """
    eigensystem = sp.Matrix(matrix).eigenvals()
    eigenvalues = list(eigensystem.keys())
    eigenvectors = [sp.Matrix(matrix).eigenvects()[i][2][0] for i in range(len(eigenvalues))]
    return eigenvalues, eigenvectors

def test_nonlinear_solution(expr, symbol, solutions, tol=1e-6):
    """
    测试非线性方程的根是否满足方程。

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
    测试线性方程组的解是否满足方程组。

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
