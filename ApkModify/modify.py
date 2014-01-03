#!/usr/bin/env python2.7
# coding=utf-8

import os
import sys
import re
import shutil
import commands
import wx

from channel_resconfig import ChannelResConfigParser

def modifyApk(apkFile, assetsPath, filterDict, keyStore):
    """Modify a apk's resouce.

    It deal with some things,as follows:
        1.Remove old signer.
        2.Remove old resource.
        3.add new resouce.
        4.add signer

    Returns:
        Sucessful is return True, otherwise return False
    """
    bModify = True
    #Remove signer
    listcmd =  "aapt list %s" % (apkFile)
    listcmd = listcmd.encode("gb2312")
    output = os.popen(listcmd).read()
    for filename in output.split('\n'):
        if filename.find("META-INF") == 0:
            rmcmd = "aapt remove %s %s" % (apkFile, filename)
            rmcmd = rmcmd.replace('\\', '/')
            rmcmd = re.sub(r'/+', '/', rmcmd)
            bReturn = os.system(rmcmd)

    #Modify apk resource.
    for root, dirs, files in os.walk(assetsPath):
        for name in files:
            if filterDict.has_key(name):
                continue
            fullFileName = os.path.join(root, name)
            resfile = fullFileName[len(assetsPath)+1: ]
            rmcmd = u"aapt remove %s %s" % (apkFile, resfile)
            rmcmd = rmcmd.replace('\\', '/')
            rmcmd = re.sub(r'/+', '/', rmcmd)
            rmcmd = rmcmd.encode("gb2312")
            bReturn =os.system(rmcmd)

            addcmd = u"aapt add %s %s" % (apkFile, resfile)
            addcmd = addcmd.replace('\\', '/')
            addcmd = re.sub(r'/+', '/', addcmd)
            addcmd = addcmd.encode("gb2312")
            bReturn = os.system(addcmd)
            print "add %s" % (resfile)
            if bReturn != 0:
                print u"add error-->%s" % (resfile)
                bModify = False
                break

    #Add signer.
    if bModify:
        channelDataDict=ChannelResConfigParser.getInstance().getConfigData()
        if (channelDataDict.has_key("keystore") and
            channelDataDict["keystore"].has_key(keyStore)
        ):
            if channelDataDict["keystore"][keyStore].has_key("key.store.password"):
                storepassword = channelDataDict["keystore"][keyStore]["key.store.password"]
            if channelDataDict["keystore"][keyStore].has_key("key.alias.password"):
                aliaspassword = channelDataDict["keystore"][keyStore]["key.alias.password"]
            if channelDataDict["keystore"][keyStore].has_key("key.alias"):
                keyalias = channelDataDict["keystore"][keyStore]["key.alias"]
            if aliaspassword=="":
                aliaspassword=storepassword
            if keyalias=="":
                keyalias=keyStore
            #jarsigner命令格式：-verbose输出详细信息 -storepass 密钥密码
            #-keystore 密钥库位置 要签名的文件 文件别名
            #jarsigner -verbose -keystore punchbox.keystore -storepass w3297825w
            #-keypass w3297825w apk android123.keystore
            apkFile = apkFile.replace('\\', '/')
            jarsingnCmd = ("jarsigner -verbose -keystore %s -storepass %s \
                -keypass %s %s  %s" %(keyStore, storepassword, aliaspassword,
                apkFile, keyalias)
            )

            bReturn = os.system(jarsingnCmd)
            #output = os.popen(jarsingnCmd).read()
            #print output
            if bReturn != 0:
                print u"jarsigner error:%s" % (apkFile)
                bModify = False

    return bModify

class CopyRes(object):
    def __init__(self):
        self.rootDir = ""
        self.filterDict = {}
        self.bspread = False
        self.dstDir = ""

    def _copyResource(self, rootDir):
        for name in os.listdir(rootDir):
            srcname = os.path.join(rootDir, name)
            if os.path.isdir(srcname):
                if self.filterDict.has_key(name):
                    continue
                self._copyResource(srcname)
            else:
                if self.filterDict.has_key(name):
                    continue

                dstname = ""
                if self.bspread:
                    dstname = os.path.join(self.dstDir, name)
                else:
                    dstname = "%s/%s" % (self.dstDir, srcname[len(self.rootDir)+1:])

                if os.path.exists(dstname):
                    os.remove(dstname)
                dirPath=os.path.dirname(dstname)

                if not os.path.exists(dirPath):
                    os.makedirs(dirPath)
                print "copy %s" % (name)
                shutil.copy2(srcname, dstname)

    def startCopy(self, srcDir, dstDir):
        self. __init__()

        self.dstDir = dstDir
        srcList = srcDir.split(" ")
        if len(srcList) >= 1:
            self.rootDir = srcList[0]
            #Make absolute path.
            resFullPath = self.rootDir
            if resFullPath.find(":") == -1:
                self.rootDir = u"%s/%s" % (sys.path[0], self.rootDir)

        if len(srcList) >= 2:
            self.bspread = srcList[1]
        if len(srcList) >= 3:
            for i in range(2, len(srcList), 1):
                self.filterDict[srcList[i]] = ""
        self._copyResource(self.rootDir)

def callParse(selChannelDict, apkFile, outPutdir, keyStore, progressCtrl):
    """Deal with select channel by configure.

       Args:
            selectChannels: The channels which you want to operate.
            apkFile: It's a empty apk package,not with resource.
            outPutdir: Out put dircetory.
            keyStore: A apk must sign by keyStore.
                      Use jarsigner tool.
            progressCtrl:The ctrl which show deal progress.

    """
    ErrorChannel={}
    index = 0
    channelDataDict=ChannelResConfigParser.getInstance().getConfigData()
    for (channel, cfgData) in channelDataDict.items():
        if not selChannelDict.has_key(channel):
            continue
        print "======%s=======" % (channel)
        tmpFolder = "%s/tmp" % (sys.path[0])
        if os.path.exists(tmpFolder):
                shutil.rmtree(tmpFolder)

        if not os.path.exists(tmpFolder):
            os.makedirs(tmpFolder)
        #Copy android resource to tmp folder's "assets" file directory.
        if cfgData.has_key("Resource_android"):
            for (key, filearg) in cfgData["Resource_android"].items():
                assetCopy = CopyRes()
                assetCopy.startCopy(filearg, "%s/assets" % (tmpFolder))

        #Copy java resource to tmp folder's "res" file directory.
        if cfgData.has_key(u"Resource_java"):
            for (key, filearg) in cfgData["Resource_java"].items():
                resCopy = CopyRes()
                resCopy.startCopy(filearg, "%s/res" % (tmpFolder))

        #Copy apk file to destination file
        apkFileName=os.path.basename(apkFile)
        if cfgData.has_key("OutPut_name"):
            apkFileName = "%s.apk" % (cfgData["OutPut_name"])
        dstApkfile =u"%s/%s" % (outPutdir, apkFileName)
        if os.path.exists(dstApkfile):
            os.remove(dstApkfile)
        if not os.path.exists(outPutdir):
            os.makedirs(outPutdir)

        #modify apk resource.
        shutil.copy2(apkFile, dstApkfile)
        prechDir=os.getcwd()
        shutil.copy2("%s/aapt.exe" % (sys.path[0]), "%s/aapt.exe" % (tmpFolder))
        shutil.copy2("%s/%s" % (sys.path[0], keyStore), "%s/%s" % (tmpFolder, keyStore))
        os.chdir(tmpFolder)
        #add file filter
        filterDict={}
        filterDict["aapt.exe"]=""
        filterDict[keyStore]=""
        bresult = modifyApk(dstApkfile, tmpFolder, filterDict, keyStore)
        os.chdir(prechDir)
        if not bresult:
            ErrorChannel[channel] = ""
            if os.path.exists(dstApkfile):
                os.remove(dstApkfile)
        if os.path.exists(tmpFolder):
            shutil.rmtree(tmpFolder)
        index = index+1
        pos = index*100/len(selChannelDict)
        if progressCtrl:
            progressCtrl.SetValue(pos)
    if len(ErrorChannel) > 0:
        print ("===================modify error channel================")
        for (key, value) in ErrorChannel.items():
            print key
    else:
        print ("   ~_~ sucessful ~_~   ")


