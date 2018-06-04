#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/16 8:47 AM
# @Author  : Steven
# @Contact : 523348709@qq.com
# @Site    : 
# @File    : duplicate.py
# @Software: PyCharm
import shutil
from detector import *

def copy_file(save_path,*file_path_list):
    file_path_list=file_path_list[0]
    split_file_path_list=split_file_path(file_path_list)
    for i in split_file_path_list:
        shutil.copy(i,save_path)