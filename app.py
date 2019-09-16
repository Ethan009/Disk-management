#!/usr/bin/python
# coding:utf-8

from flask import Flask,render_template
import difflib
import re
import os
#import pexpect
import sys
import commands
import subprocess

# reload(sys)
# sys.setdefaultencoding('utf-8')

app = Flask(__name__)

def disk_view():
    diskmount = subprocess.getoutput("lsblk -lf ")
    return diskmount


def datapc():

    datapc = subprocess.getoutput("lsblk -lf ")
    # 正则表达式
    re_disk_device = r'(sd[a-z]{1,2}\b)'
    re_partition_no_fs = r'.*(sd\D{1,2}\d{1,2})'
    re_partition_fs_not_mount = r'.*(sd\D{1,2}\d{1,2}) (\S+).*[^/]'
    re_partition_fs_mounted = r'(sd\D{1,2}\d{1,2}) (\S+).* (/.*)'

    lst_line = datapc.split('\n')

    lstDisk = []
    dicDI = {}

    for line in lst_line:
        re_disk_device_result = re.match(re_disk_device, line)
        re_partition_no_fs_result = re.match(re_partition_no_fs, line)
        re_partition_fs_not_mount_result = re.match(re_partition_fs_not_mount, line)
        re_partition_fs_mounted_result = re.match(re_partition_fs_mounted, line)

        if re_disk_device_result:
            disk_device = str(re_disk_device_result.group())
            lstDisk.append(disk_device)
            dicDI[disk_device] = []
            continue
        else:
            if re_partition_fs_mounted_result:
                lstPartion = re_partition_fs_mounted_result.groups()
                lstPartion = list(lstPartion)
                lstPartion.append('0')
                if lstDisk:
                    dicDI[lstDisk[-1]].append(list(lstPartion))
                continue
            elif re_partition_fs_not_mount_result:
                lstPartion = re_partition_fs_not_mount_result.groups()
                lstPartion = list(lstPartion)
                lstPartion.append('')
                lstPartion.append('1')
                if lstDisk:
                    dicDI[lstDisk[-1]].append(list(lstPartion))
                continue
            elif re_partition_no_fs_result:
                lstPartion = re_partition_no_fs_result.groups()
                lstPartion = list(lstPartion)
                lstPartion.append('')
                lstPartion.append('')
                lstPartion.append('2')
                if lstDisk:
                    dicDI[lstDisk[-1]].append(list(lstPartion))
                continue
    # print(lstDisk)
    # pprint.pprint(dicDI)
        print (dicDI)
    return dicDI

def data_to_json():
    lis_data=[]
    dic_data={}
    Diskdata_pc = datapc()
    keys=Diskdata_pc.keys()
    values=Diskdata_pc.values()
    for key in keys():
        dic_data['disk']=key
        dic_data['options'] = []
        dic_child_data={}
        for value in values:
            dic_child_data['name']=value[0]
            dic_child_data['file_system']=value[1]
            dic_child_data['file_name']=value[2]
            dic_child_data['status']=value[3]
            dic_data['options'].append(dic_child_data)
        lis_data.append(dic_data)
    return lis_data

@app.route('/')
def hello_world():
    Diskdata=disk_view()
    Diskdata_pc=data_to_json()
    return render_template('index.html',Diskdata=Diskdata_pc)

dict_items=([('sba',[])])


if __name__ == '__main__':
    app.run()
