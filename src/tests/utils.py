import numpy as np


def arrays_equal(arr1, arr2, tol=1e-6*2):
    """
    @brief: 判断解是否预估值相同
    @param tol: 容许误差范围的大小
    """
    if len(arr1) != len(arr2):
        return False
    
    sorted_arr1 = np.sort(arr1)
    sorted_arr2 = np.sort(arr2)
    
    return np.allclose(sorted_arr1, sorted_arr2, atol=tol)