import pytest
import sympy as sp
import numpy as np
from src.solver import (
    calculate_determinant,
    calculate_inverse,
    calculate_transpose,
    calculate_rank,
    matrix_power,
    multiply_matrices,
    calculate_eigenvalues_and_vectors,
)


# def calculate_determinant(matrix):
#     """
#     @brief 计算矩阵的行列式。
#     @param matrix 输入的矩阵
#     @return 矩阵的行列式
#     """
def test_calculate_determinant():
    assert calculate_determinant(sp.Matrix([[1, 2], [3, 4]])) == -2
    assert calculate_determinant(sp.Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])) == 0
    assert (
        calculate_determinant(
            sp.Matrix([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]])
        )
        == 0
    )


# def calculate_inverse(matrix):
#     """
#     @brief 计算矩阵的逆矩阵。
#     @param matrix 输入的矩阵
#     @return 矩阵的逆矩阵
#     """
def test_calculate_inverse():
    imat = calculate_inverse(sp.Matrix([[1, 2], [3, 4]]))
    assert np.array_equal(imat, [[-2, 1], [1.5, -0.5]])
    imat = calculate_inverse(sp.Matrix([[1, 2, 3], [0, 1, 4], [5, 6, 0]]))
    assert np.array_equal(imat, [[-24, 18, 5], [20, -15, -4], [-5, 4, 1]])


# def calculate_transpose(matrix):
#     """
#     @brief 计算矩阵的转置。
#     @param matrix 输入的矩阵
#     @return 矩阵的转置
#     """
def test_calculate_transpose():
    tmat = calculate_transpose(sp.Matrix([[1, 2], [3, 4]]))
    assert np.array_equal(tmat, [[1, 3], [2, 4]])
    tmat = calculate_transpose(sp.Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
    assert np.array_equal(tmat, [[1, 4, 7], [2, 5, 8], [3, 6, 9]])


# def calculate_rank(matrix):
#     """
#     @brief 计算矩阵的秩。
#     @param matrix 输入的矩阵
#     @return 矩阵的秩
#     """
def test_calculate_rank():
    assert calculate_rank(sp.Matrix([[1, 2], [3, 4]])) == 2
    assert calculate_rank(sp.Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])) == 2
    assert (
        calculate_rank(
            sp.Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        )
        == 4
    )


# def matrix_power(matrix, power):
#     """
#     @brief 计算矩阵的幂。
#     @param matrix 输入的矩阵
#     @param power 幂次
#     @return 矩阵的幂
#     """
def test_matrix_power():
    pmat = matrix_power(sp.Matrix([[1, 2], [3, 4]]), 1)
    assert np.array_equal(pmat, [[1, 2], [3, 4]])
    pmat = matrix_power(sp.Matrix([[1, 2], [3, 4]]), 2)
    assert np.array_equal(pmat, [[7, 10], [15, 22]])
    pmat = matrix_power(sp.Matrix([[1, 2], [3, 4]]), 3)
    assert np.array_equal(pmat, [[37, 54], [81, 118]])
    pmat = matrix_power(sp.Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), 2)
    assert np.array_equal(pmat, [[30, 36, 42], [66, 81, 96], [102, 126, 150]])


# def multiply_matrices(matrix1, matrix2):
#     """
#     @brief 计算两个矩阵的乘积。
#     @param matrix1 第一个矩阵
#     @param matrix2 第二个矩阵
#     @return 两个矩阵的乘积
#     """
def test_multiply_matrices():
    mmat = multiply_matrices(sp.Matrix([[1, 2], [3, 4]]), sp.Matrix([[5, 6], [7, 8]]))
    assert np.array_equal(mmat, [[19, 22], [43, 50]])
    m1 = sp.Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    m2 = sp.Matrix([[9, 8, 7], [6, 5, 4], [3, 2, 1]])
    mmat = multiply_matrices(m1, m2)
    assert np.array_equal(mmat, [[30, 24, 18], [84, 69, 54], [138, 114, 90]])


# def calculate_eigenvalues_and_vectors(matrix):
#     """
#     @brief 计算矩阵的特征值和特征向量。
#     @param matrix 输入的矩阵
#     @return 特征值和特征向量的列表
#     """
# def test_calculate_eigenvalues_and_vectors():
#     eval, evec = calculate_eigenvalues_and_vectors(sp.Matrix([[4, 1], [2, 3]]))
#     assert np.array_equal(eval, [5, 2])
#     assert np.array_equal(evec, [[-0.70710678, -0.4472136], [0.70710678, 0.89442719]])
