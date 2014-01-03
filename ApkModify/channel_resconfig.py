#!/usr/bin/env python2.7
# coding=utf-8

import threading
import yaml
import sys

class ChannelResConfigParser(object):
    '''The class can parse channel resource config file of yaml '''

    def __init__(self):
        "disable the __init__ method"

    __configParse = None

    __lock = threading.Lock()

    @staticmethod
    def getInstance():
        # threading safe
        ChannelResConfigParser.__lock.acquire()

        if not ChannelResConfigParser.__configParse:
            ChannelResConfigParser.__configParse = \
                object.__new__(ChannelResConfigParser)
            object.__init__(ChannelResConfigParser.__configParse)
            ChannelResConfigParser.__configParse.projectConfigData = {}

        ChannelResConfigParser.__lock.release()
        return ChannelResConfigParser.__configParse

    def Read(self):
        '''Read ChannelResConfig.yaml file and save to a dictionary'''

        file = open("%s/ChannelResConfig.yaml" %(sys.path[0]),"r")
        if file:
            data = file.read()
            self.projectConfigData = yaml.load(data)
            file.close()
            yaml.dump(
                self.projectConfigData,
                default_flow_style=False,
                allow_unicode=True
            )
        else:
            print "The ChannelResConfig.yaml file is open failed"
            return False
        return True

    def getConfigData(self):
        '''Get thd config's dictionary datas'''

        return self.projectConfigData

    def getChannelData(self, channelId):

        if self.projectConfigData.has_key(channelId):
            return self.projectConfigData[channelId]
        return None



class UIConfigParser(object):
    '''The class can parse channel resource config file of yaml '''

    def __init__(self):
        "disable the __init__ method"

    __configParse = None

    __lock = threading.Lock()

    @staticmethod
    def getInstance():
        # threading safe
        UIConfigParser.__lock.acquire()

        if not UIConfigParser.__configParse:
            UIConfigParser.__configParse = object.__new__(UIConfigParser)
            object.__init__(UIConfigParser.__configParse)
            UIConfigParser.__configParse.projectConfigData = {}

        UIConfigParser.__lock.release()
        return UIConfigParser.__configParse

    def Read(self):
        '''Read UIConfig.yaml file and save to a dictionary'''

        file = open("%s/UIConfig.yaml" %(sys.path[0]),"r")
        if file:
            data = file.read()
            self.projectConfigData = yaml.load(data)
            file.close()
            yaml.dump(
                self.projectConfigData,
                default_flow_style=False,
                allow_unicode=True
            )
        else:
            print "The UIConfig.yaml file is open failed"
            return False
        return True

    def getApkPath(self):
        '''Get thd config's dictionary datas'''
        if self.projectConfigData.has_key("ApkPath"):
            return self.projectConfigData["ApkPath"]
        return ""

    def getOutPutPath(self):
        '''Get thd config's dictionary datas'''
        if self.projectConfigData.has_key("OutPutPath"):
            return self.projectConfigData["OutPutPath"]
        return ""

    def setApkPath(self,apkPath):
        self.projectConfigData["ApkPath"] = apkPath

    def setOutPutPath(self,outPutPath):
        self.projectConfigData["OutPutPath"] = outPutPath

    def Write(self):
        file = open("%s/UIConfig.yaml" %(sys.path[0]),"w")
        if file:
            try:
                yaml.dump(
                    self.projectConfigData,
                    file,
                    default_flow_style=False,
                    allow_unicode=True
                )
                file.flush()
                file.close()
                return True
            except Exception,error:
                print "ProjectCofigWrite-->%s" % (error)
        return False
