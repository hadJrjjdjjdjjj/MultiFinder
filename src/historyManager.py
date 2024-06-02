"""
@file history_manager.py
@brief 历史记录管理模块
@details
此模块包含用于管理运算历史记录的HistoryManager类。该类提供添加、获取和清空历史记录的功能。
历史记录包括非线性方程、线性方程组以及矩阵运算的记录。
主要功能包括：
- 添加一条记录到历史记录中
- 获取某种运算类型的历史记录
- 清空某种运算类型的历史记录

@version 1.0
@date 2024-06-02
"""

import tkinter as tk
import sympy as sp
import numpy as np


class HistoryManager:
    """
    @brief 历史记录管理类
    @details 此类用于管理运算的历史记录，包括添加记录、获取记录和清空记录。
    """
    def __init__(self):
        """
        @brief 初始化HistoryManager类
        @details 创建一个空的历史记录字典，用于存储不同类型的运算记录。
        """
        self.history = {
            "nonlinear": [],
            "linear": [],
            "matrix": {
                "determinant": [],
                "inverse": [],
                "transpose": [],
                "rank": [],
                "power": [],
                "multiply": [],
                "eigen": []
            }
        }

    def add_record(self, operation_type, expression, result, sub_operation=None):
        """
        @brief 添加一条记录到历史记录中
        @param operation_type 运算类型，可以是"nonlinear"、"linear"或"matrix"
        @param expression 运算表达式或矩阵
        @param result 运算结果
        @param sub_operation 子运算类型，仅用于矩阵运算
        """
        if operation_type == "matrix" and sub_operation:
            self.history[operation_type][sub_operation].insert(0, {
                "expression": expression,
                "result": result
            })
        elif operation_type in self.history:
            self.history[operation_type].insert(0, {
                "expression": expression,
                "result": result
            })

    def get_history(self, operation_type, sub_operation=None):
        """
        @brief 获取某种运算类型的历史记录
        @param operation_type 运算类型，可以是"nonlinear"、"linear"或"matrix"
        @param sub_operation 子运算类型，仅用于矩阵运算
        @return 对应运算类型的历史记录列表
        """
        if operation_type == "matrix" and sub_operation:
            return self.history[operation_type].get(sub_operation, [])
        return self.history.get(operation_type, [])

    def clear_history(self, operation_type, sub_operation=None):
        """
        @brief 清空某种运算类型的历史记录
        @param operation_type 运算类型，可以是"nonlinear"、"linear"或"matrix"
        @param sub_operation 子运算类型，仅用于矩阵运算
        """
        if operation_type == "matrix" and sub_operation:
            self.history[operation_type][sub_operation] = []
        elif operation_type in self.history:
            self.history[operation_type] = []
