# -*- coding: utf-8 -*-
'''
 @Time : 2018/6/28 14:41
 @Author : Baoyu@mail.ustc.edu.cn
 @Site :
 @File : blog.py
 @Software: PyCharm
'''
import numpy as np
from subprocess import Popen
import os

preDir = os.getcwd()
env = os.environ
print(env)
print(os.get_exec_path(env))
a = np.random.standard_normal(10)
f = open(os.path.join(preDir, "data.txt"), "w")
for i in range(10):
    f.write("{} {}\n".format(i, a[i]))
f.close()

in_path = "\'"+os.path.join(preDir, "data.txt")+"\'"
out_path = "\'"+os.path.join(preDir, "data.png")+"\'"
cmd = ['gnuplot',
       '-e',
       "input_fname=" + in_path + ";output_fname=" + out_path + "",
       os.path.join(preDir, "plot.plt")
       ]
Popen(cmd)