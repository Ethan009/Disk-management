#!/usr/bin/python
# coding:utf-8

from flask import Flask, render_template, request, json, make_response
import sys
import os
import pexpect
reload(sys)
sys.setdefaultencoding('utf-8')
app = Flask(__name__)

import datapc as da
# import Data as da

# data = {"sda":["22","22"],"sdc":[["22","11"],["22","333"]]}


@app.route("/", methods=['POST', 'GET'])
def hello():
    if request.method == "POST":
        yjfq = request.values.get('yjfq')  # 一键分区
        yufenqu = request.values.get('yufenqu')  # 预分区磁盘
        fengquhao = request.values.get('fengquhao')  # 分区号
        start = request.values.get('start')  # 开始
        end = request.values.get('end')  # 结束
        ygzcpm = request.values.get('ygzcpm')  # 预挂载磁盘
        wjjlj = request.values.get('wjjlj')  # 文件夹路径输入
        hidden = request.values.get('hidden')  # 文件类型选择
        xxx = request.values.get('xxx')  # 当前磁盘分区
         
         
        # 格式化文件类型
        if hidden and xxx:
            os.popen("mkfs.%s /dev/%s " % (hidden, xxx))
            #print("格式化成功")
        else:
            #print("格式化失败")
            pass
         
        # 一键分区
        #print(yjfq)
        if yjfq:
            child = pexpect.spawn("sudo fdisk /dev/%s" % (yjfq), timeout=3)
            child.sendline('n')
            child.sendline('\n')
            child.sendline('\n')
            child.sendline('\n')
            child.sendline('\n')
            child.sendline('w')
            print("Successful to Partition")
        else:
            #print("faild to Partition")
            pass
         
        # 手动分区
        if yufenqu and fengquhao and start and end:
            child = pexpect.spawn("sudo fdisk /dev/%s" % (yufenqu), timeout=3)
            child.sendline('n')
            child.sendline('p')
            child.sendline('%s' % (fengquhao))
            child.sendline('%s' % (start))
            child.sendline('%s' % (end))
            child.sendline('w')
            print("Successful to Partition")
        else:
            #print("faild to Partition")
            pass
         
        # 磁盘挂载
        if ygzcpm and wjjlj:
            os.system("mkdir %s" % (wjjlj))
            print("创建文件夹成功")
            os.system("mount /dev/%s %s" % (ygzcpm, wjjlj))
            print("挂载成功")
        else:
            pass

    data = da.datapc()
    print(data)
    data_key = data.keys()
    return render_template("index.html",
                           data_key=data_key,
                           data=data 
            )


if __name__ == "__main__":
    app.run(port=3333)

