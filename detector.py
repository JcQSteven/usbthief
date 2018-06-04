#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/16 8:51 AM
# @Author  : Steven
# @Contact : 523348709@qq.com
# @Site    : 
# @File    : detector.py
# @Software: PyCharm
import os

def usb_detetor():
    import os
    output = os.popen("wmic LogicalDisk where \"DriveType='2'\" get DeviceID /value")
    usb_disk = output.read().replace('\r\n', '').split('DeviceID=')
    output.close()
    del usb_disk[0]
    return usb_disk

def get_all(usb_path,full_path=True,end_name=None):
    file_name_list=[]

    for root, dirs, files in os.walk(usb_path):
        for file_name in files:
            if full_path:
                file_name=os.path.join(root, file_name)
            if end_name!=None:
                if file_name.endswith(end_name):
                    file_name_list.append(file_name)
            else:
                file_name_list.append(file_name)
    return file_name_list

def get_all_type(usb_path,full_path=True,*type):
    file_name_list = []
    type=type[0]
    for root, dirs, files in os.walk(usb_path):
        for file_name in files:
            if full_path:
                file_name=os.path.join(root, file_name)
            if len(type)!=0:
                for i in type:
                    if file_name.endswith(i):
                        file_name_list.append(file_name)
                        break
            else:
                file_name_list.append(file_name)
    return file_name_list


def split_file_path(*file_path_list):
    file_path_list=file_path_list[0]
    split_file_path_list=[]
    for file_path in file_path_list:
        file_path=file_path.split('/')[-1]
        split_file_path_list.append(file_path)
    return split_file_path_list
