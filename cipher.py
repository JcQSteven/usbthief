#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/14 4:54 PM
# @Author  : Steven
# @Contact : 523348709@qq.com
# @Site    : 
# @File    : cipher.py
# @Software: PyCharm
import datetime
import time
from Crypto.Hash import MD5
from Crypto.Cipher import AES
import random
import string
from detector import *
class Cipher:
    def __init__(self):
        pass

    def cipher_file(self,save_path,cipher_name='.cipher',*file_path_list):
        file_path_list=file_path_list[0]
        cipher_time=datetime.datetime.now()
        record_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        md5=MD5.new()
        md5.update(str(cipher_time))
        key=md5.hexdigest()
        iv = ''.join(random.sample(string.ascii_letters + string.digits, 16))
        cipher_tool=AES.new(key, AES.MODE_CFB,iv)

        split_file_path_list=split_file_path(file_path_list)
        for file_name in split_file_path_list:
            if len(file_name.split('.'))>1:
                file_path=file_path_list[split_file_path_list.index(file_name)]
                f=open(file_path,'rb')
                f_msg = f.read()

                x = len(f_msg) % 32
                if x != 0:
                    f_fixed = f_msg + '0' * (32 - x)
                else:
                    f_fixed = f_msg
                cipherText = cipher_tool.encrypt(f_fixed)
                f_new = open(file_path + cipher_name, 'wb+')
                f_new.write(cipherText)
                f.close()
                os.remove(file_path)

        key_path=self.exportKey(record_time, key, iv,save_path)
        return key_path

    def decipher_file(self,key_path,cipher_name='.cipher',*file_path_list):
        file_path_list = file_path_list[0]
        f=open(key_path,'r')
        key=f.readline().strip()
        iv=f.readline().strip()
        decipher_tool=AES.new(key,AES.MODE_CFB,iv)
        split_file_path_list = split_file_path(file_path_list)
        for file_name in split_file_path_list:
            if len(file_name.split('.'))>1:
                file_path=file_path_list[split_file_path_list.index(file_name)]
                f=open(file_path,'rb')
                f_msg = f.read()

                x = len(f_msg) % 32
                if x != 0:
                    f_fixed = f_msg + '0' * (32 - x)
                else:
                    f_fixed = f_msg
                decipherText = decipher_tool.decrypt(f_fixed)
                fix_file_path=file_path.replace(cipher_name,'')
                f_new = open(fix_file_path, 'wb+')
                f_new.write(decipherText)
                f.close()
                os.remove(file_path)
        pass
    def exportKey(self,record_time,key,iv,save_path):
        path=save_path+record_time+'.ini'
        f=open(path,'w+')
        f.write(key+'\n')
        f.write(iv)
        f.close()
        return path

