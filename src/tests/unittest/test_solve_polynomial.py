import pytest
from src.solver import solve_polynomial
from src.tests.utils import *

# def solve_polynomial(coeffs):
#     """
#     @brief 使用 NumPy 的 roots 函数求解多项式的根。
#     @param coeffs 多项式的系数列表
#     @return 多项式的根
#     """

# Testing strategy:
#     coeffs.len: 1~n
#     coeffs 有无虚数根
def test_solve_polynomial():
    # 常数项多项式，无解
    roots = solve_polynomial([1])
    assert roots.size == 0
    
    # 仅实数根
    roots = solve_polynomial([1,-5,6])
    assert arrays_equal(roots, [2,3])
    
    roots = solve_polynomial([1,-6,11,-6])
    assert arrays_equal(roots, [1,2,3])
    
    roots = solve_polynomial([1,-10,35,-50,24])
    assert arrays_equal(roots, [1,2,3,4])
    
    # 含虚数根
    roots = solve_polynomial([1,0,1])
    assert arrays_equal(roots, [0+1j,0+-1j])
    
    roots = solve_polynomial([1,1,1,1])
    assert arrays_equal(roots, [-1, -1j, 1j])
