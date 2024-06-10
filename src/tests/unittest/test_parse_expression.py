import pytest
import sympy as sp
from src.utils import parse_expression
# TODO: 修改spec
# def parse_expression(expression):
#     """
#     @brief 解析用户输入的方程表达式，并转换为一个可求解的函数。
#     @param expression 方程表达式字符串
#     @return 一个包含 SymPy 表达式、符号变量、多项式系数列表（如果是多项式方程）、是否为多项式的元组
#     @throw ValueError 当方程中变量数量不为一个时抛出异常
#     """

# Testing strategy:
#     expression(符合预处理后的语义): 多项式、指数、三角、对数、复合函数、是否化简、不同的变量
#     异常：ValueError 当方程中变量数量不为一个时
def test_parse_expression():
    expr, symbol, coeffs, bl = parse_expression('x+2')
    assert symbol.name == 'x'
    assert coeffs == [1,2]
    assert sp.simplify('x+2') == expr
    assert bl == True

    expr, symbol, coeffs, bl = parse_expression('x+1+1')
    assert symbol.name == 'x'
    assert coeffs == [1,2]
    assert sp.simplify('x+2') == expr
    assert bl == True

    expr, symbol, coeffs, bl = parse_expression('e^y+1')
    assert symbol.name == 'y'
    assert coeffs == None
    assert sp.simplify('exp(y)+1') == expr
    assert bl == False

    expr, symbol, coeffs, bl = parse_expression('2*e^x+x')
    assert symbol.name == 'x'
    assert coeffs == None
    assert sp.simplify('2*exp(x)+x') == expr
    assert bl == False

    expr, symbol, coeffs, bl = parse_expression('sin(x+1)+x')
    assert symbol.name == 'x'
    assert coeffs == None
    assert sp.simplify('sin(x+1)+x') == expr
    assert bl == False

    expr, symbol, coeffs, bl = parse_expression('ln(x+1)+x')
    assert symbol.name == 'x'
    assert coeffs == None
    assert sp.simplify('ln(x+1)+x') == expr
    assert bl == False

    expr, symbol, coeffs, bl = parse_expression('ln(sin(x)+1)+x')
    assert symbol.name == 'x'
    assert coeffs == None
    assert sp.simplify('ln(sin(x)+1)+x') == expr
    assert bl == False

    expr, symbol, coeffs, bl = parse_expression('x^3+5*x+7*x^2+100')
    assert symbol.name == 'x'
    assert coeffs == [1,7,5,100]
    assert sp.simplify('x^3+5*x+7*x^2+100') == expr
    assert bl == True

    with pytest.raises(ValueError) as e:
        parse_expression('x+y')








