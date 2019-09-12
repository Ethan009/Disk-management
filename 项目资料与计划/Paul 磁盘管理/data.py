#!/usr/bin/python
# coding:utf-8

import commands
class Data():
    
    def Disk_Mount(self):
        diskmount = commands.getoutput("sudo lsblk -lf ")
        return diskmount
    
if __name__ == "__main__":
    #print(Data().Disk_Mount())
    pass

