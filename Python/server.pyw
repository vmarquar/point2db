# !/usr/bin/python
# -*- coding: utf-8 -*-
import os,time

def checkDir (mypath,filename="new_point.txt"):
    onlyfiles = [f for f in os.listdir(mypath) if (os.path.isfile(os.path.join(mypath, f)) and f == filename)]
    #print "Found match with keyword:{0}<->{1}".format(onlyfiles,filename)
    return onlyfiles

def touch(path):
    with open(path, 'a'):
        os.utime(path, None)


mypath = "N:/Start_Script"
filename="new_point.txt"

while True:
    onlyfiles = checkDir(mypath,filename)
    for configfile in onlyfiles:
        try:
            print "starting script..."
            try:
                try:
                    os.remove(os.path.join(mypath,'Added_point_successfully_delete_me.txt'))
                except:
                    print "File already deleted..."

                os.system("C:\GIS\Python_Tools\point2db\Python\main.py")
                print "successfully added point. Deleting config.file now..."
                touch(os.path.join(mypath,'Added_point_successfully_delete_me.txt'))
                os.remove(os.path.join(mypath,configfile))

            except:
                raise
        except:
            pass





    print "waiting for configfile..."
    time.sleep(30)
    pass
