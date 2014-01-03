#!/usr/bin/env python2.7
# coding=utf-8

import os
import wx
import sys
import modify
from ObjectListView import ObjectListView, ColumnDefn
from channel_resconfig import ChannelResConfigParser
from channel_resconfig import UIConfigParser

class Results(object):
    """"""
    def __init__(
        self,
        channal_id,
        channal_alias,
        channal_custom
    ):
        """Constructor"""
        self.channal_id = channal_id
        self.channal_alias = channal_alias
        self.channal_custom = channal_custom


class ModifyPanel(wx.Panel):
    """"""
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        main_Sizer = wx.BoxSizer(wx.VERTICAL)

        #strinfo=u" 对apk渠道各个资源的配置写在channelconfig.xlsx,并且放到程序目录下"
        #self.infosta= wx.StaticText(self, -1, strinfo)

        #select a apk ui
        self.apk_Box = wx.StaticBox(self, -1, u"Apk")
        apkBoxSizer = wx.StaticBoxSizer(self.apk_Box, wx.HORIZONTAL)
        self.apksta = wx.StaticText(self, -1, u"apk包:  ")
        self.apkdiredit = wx.TextCtrl(self, -1, "")
        self.apkdirbtn = wx.Button(self, label=u"...")
        apkBoxSizer.Add(self.apksta, 0, wx.ALL|wx.ALIGN_TOP, 5)
        apkBoxSizer.Add(self.apkdiredit, 1, wx.ALL|wx.ALIGN_TOP, 5)
        apkBoxSizer.Add(self.apkdirbtn, 0, wx.ALL|wx.ALIGN_TOP, 5)

        #select a resource ui
        """
        self.res_Box = wx.StaticBox(self, -1, u"Resource")
        resBoxSizer = wx.StaticBoxSizer(self.res_Box, wx.HORIZONTAL)
        self.ressta = wx.StaticText(self, -1, u"资源目录:")
        self.resdiredit = wx.TextCtrl(self, -1, "")
        self.resdirbtn = wx.Button(self, label=u"...")
        resBoxSizer.Add(self.ressta, 0, wx.ALL|wx.ALIGN_TOP, 5)
        resBoxSizer.Add(self.resdiredit, 1, wx.ALL|wx.ALIGN_TOP, 5)
        resBoxSizer.Add(self.resdirbtn, 0, wx.ALL|wx.ALIGN_TOP, 5)
        """
        #set out put directory
        self.outPut_Box = wx.StaticBox(self, -1, u"Output")
        outPutBoxSizer = wx.StaticBoxSizer(self.outPut_Box, wx.HORIZONTAL)
        self.outPutsta = wx.StaticText(self, -1, u"输出目录:")
        self.outPutdiredit = wx.TextCtrl(self, -1, "")
        self.outPutdirbtn = wx.Button(self, label=u"...")
        outPutBoxSizer.Add(self.outPutsta, 0, wx.ALL|wx.ALIGN_TOP, 5)
        outPutBoxSizer.Add(self.outPutdiredit, 1, wx.ALL|wx.ALIGN_TOP, 5)
        outPutBoxSizer.Add(self.outPutdirbtn, 0, wx.ALL|wx.ALIGN_TOP, 5)

        #layout operate button
        #The list static box
        self.choiceList_Box = wx.StaticBox(self, -1, u"列表")
        self.choiceSel =wx.Choice(
            self, -1,choices=[u"全不选", u"反选", u"全选"]
        )
        self.choiceSel.SetSelection(0)
        self.keyStoreChoiceSel =wx.Choice(self, -1)
        choice_BoxSizer = wx.StaticBoxSizer(self.choiceList_Box, wx.HORIZONTAL)
        choice_BoxSizer.Add(self.choiceSel, 0, wx.ALL|wx.ALIGN_TOP, 5)
        choice_BoxSizer.Add(self.keyStoreChoiceSel, 0, wx.ALL|wx.ALIGN_TOP, 5)

        self.saveBtn = wx.Button(self, label=u"保存UI")
        self.GenBtn = wx.Button(self, label=u"生成")

        operate_Sizer = wx.BoxSizer(wx.HORIZONTAL)
        operate_Sizer.Add(choice_BoxSizer, 0, wx.ALIGN_LEFT|wx.EXPAND|wx.ALL, 5)
        operate_Sizer.Add(self.saveBtn, 0, wx.ALIGN_LEFT|wx.EXPAND|wx.ALL, 5)
        operate_Sizer.Add(self.GenBtn,0, wx.ALIGN_LEFT|wx.EXPAND|wx.ALL, 5)

        #add listctrl
        self.resultsOlv = ObjectListView(
            self,
            style = wx.LC_REPORT|wx.SUNKEN_BORDER
        )
        self.InitColumns()

        self.progress = wx.Gauge(self, -1)
        self.progress.SetRange(100)

        #main_Sizer.Add(self.infosta, 0, wx.EXPAND|wx.ALL, 5)
        main_Sizer.Add(apkBoxSizer, 0, wx.EXPAND|wx.ALL, 5)
        #main_Sizer.Add(resBoxSizer, 0, wx.EXPAND|wx.ALL, 5)
        main_Sizer.Add(outPutBoxSizer, 0, wx.EXPAND|wx.ALL, 5)
        main_Sizer.Add(self.resultsOlv, 1, wx.EXPAND|wx.ALL, 5)
        main_Sizer.Add(self.progress, 0, wx.EXPAND|wx.ALL, 5)
        main_Sizer.Add(operate_Sizer, 0, wx.EXPAND|wx.ALL, 5)
        self.SetSizer(main_Sizer)

        self.apkdirbtn.Bind(wx.EVT_BUTTON, self.onSelApkButton)
        #self.resdirbtn.Bind(wx.EVT_BUTTON, self.onSelResButton)
        self.outPutdirbtn.Bind(wx.EVT_BUTTON, self.onSelOutDirButton)
        self.choiceSel.Bind(wx.EVT_CHOICE, self.OnSelChoice)
        self.saveBtn.Bind(wx.EVT_BUTTON, self.onSaveUIButton)
        self.GenBtn.Bind(wx.EVT_BUTTON, self.onGenButton)

        #Set choice change event.
        self.choicesDict = {}
        self.choicesDict[u"全不选"] = self.ListCheckNotSel
        self.choicesDict[u"反选"] = self.ListCheckInverSel
        self.choicesDict[u"全选"] = self.ListCheckSelAll

        self.progress.SetValue(0)
        self.loadChannelCofigToList()
    #=======================Init End=====================================#

    def loadChannelCofigToList(self):
        """ Load Channel config then show to UI listCtrl"""

        UIConfigParser.getInstance().Read()
        ChannelResConfigParser.getInstance().Read()
        self.test_data = []
        configData = ChannelResConfigParser.getInstance().getConfigData()
        for (key, value) in configData.items():
            if key == "keystore":
                continue
            self.test_data.append(Results(str(key),"",""))
         #Set value to list.
        self.resultsOlv.SetObjects(self.test_data)
        objects = self.resultsOlv.GetObjects()
         #Refresh UI.
        self.resultsOlv.RefreshObjects(objects)
        if configData.has_key("keystore"):
            for (key, value) in configData["keystore"].items():
                self.keyStoreChoiceSel.Append(key)

        self.keyStoreChoiceSel.SetSelection(0)
        self.apkdiredit.SetValue(UIConfigParser.getInstance().getApkPath())
        self.outPutdiredit.SetValue(UIConfigParser.getInstance().getOutPutPath())

    def InitColumns(self):
        """Init list colums."""

        self.resultsOlv.SetColumns([
            ColumnDefn(u"渠道", "left", 150, "channal_id"),
            #ColumnDefn(u"渠道信息", "left", 160, "channal_alias"),
            #ColumnDefn(u"渠道特制", "left", 320, "channal_custom")
        ])
        self.resultsOlv.CreateCheckStateColumn()

    def onSelApkButton(self, event):
        file_wildcard = "source file(*.apk)|*.apk"
        dialog = wx.FileDialog(self,
                            "Get a apk file",
                            #os.getcwd(),
                            style = wx.FD_OPEN | wx.FD_CHANGE_DIR,
                            wildcard = file_wildcard)
        if dialog.ShowModal() != wx.ID_OK:
            return
        self.apkdiredit.SetValue(dialog.GetPath())
        pass

    def onSelResButton(self, event):
        dialog = wx.DirDialog(
            None,
            u"选择资源目录:",
            style = wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON
        )
        if dialog.ShowModal() == wx.ID_OK:
            self.resdiredit.SetValue(dialog.GetPath())

    def onSelOutDirButton(self, event):
        dialog = wx.DirDialog(
            None,
            u"选择输出目录:",
            style = wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON
        )
        if dialog.ShowModal() == wx.ID_OK:
            self.outPutdiredit.SetValue(dialog.GetPath())
        pass

    def onSaveUIButton(self, event):
        self.saveUiInfo()

    def saveUiInfo(self):
        UIConfigParser.getInstance().setApkPath(self.apkdiredit.GetValue())
        UIConfigParser.getInstance().setOutPutPath(self.outPutdiredit.GetValue())
        UIConfigParser.getInstance().Write()

    def onGenButton(self, event):
        apkFile = self.apkdiredit.GetValue()
        if apkFile.strip() == "":
            self.messageBox(u"未选择APK")
            return
        if self.fileNoExist(apkFile):
            return
        """
        resdir = self.resdiredit.GetValue()
        if resdir.strip() == "":
            self.messageBox(u"未选择资源目录")
            return
        if self.fileNoExist(resdir):
            return
        """
        outPutdir = self.outPutdiredit.GetValue()
        if outPutdir.strip() == "":
            self.messageBox(u"未选择输出目录")
            return
        if self.fileNoExist(outPutdir):
            return

        iSel=self.keyStoreChoiceSel.GetSelection()
        keyStore=self.keyStoreChoiceSel.GetString(iSel)
        if keyStore.strip() == "":
            self.messageBox(u"keyStore为空")
            return
        if self.fileNoExist("%s/%s" % (sys.path[0], keyStore)):
            return

        #If the channel be selected,it's value is 1.
        #otherwise it's value is 0.
        selChanneldict = {}
        objects = self.resultsOlv.GetObjects()
        for obj in objects:
            if self.resultsOlv.GetCheckState(obj, 0):
                selChanneldict[self.resultsOlv.GetStringValueAt(obj, 1)] = 0

        #No select channel.
        if len(selChanneldict) <= 0:
            self.messageBox(u"未选择渠道")
            return

        self.saveUiInfo()
        #Call parse
        modify.callParse(selChanneldict, apkFile, outPutdir, keyStore, self.progress)
        dlg = wx.MessageDialog(None, u"渠道处理完成", u"", wx.wx.OK)
        result = dlg.ShowModal()
        dlg.Destroy()
        self.progress.SetValue(0)

    def fileNoExist(self,filename):
        if os.path.exists(filename):
            return False
        dlg = wx.MessageDialog(
            None,u"%s 不存在" %(filename), u"错误", wx.OK|wx.ICON_ERROR
        )
        result = dlg.ShowModal()
        dlg.Destroy()
        return True

    def messageBox(self,errorMsg):
        dlg = wx.MessageDialog(None,errorMsg, u"错误",wx.OK|wx.ICON_ERROR)
        result = dlg.ShowModal()
        dlg.Destroy()

    #========================choice event====================#
    def OnSelChoice(self, event):
        """Choice change event"""

        iSel=self.choiceSel.GetSelection()
        selString=self.choiceSel.GetString(iSel)
        self.choicesDict[selString]()

    def ListCheckSelAll(self):
        """Select all channals"""

        objects = self.resultsOlv.GetObjects()
        for obj in objects:
            self.resultsOlv.SetCheckState(obj, True)
        self.resultsOlv.RefreshObjects(objects)

    def ListCheckInverSel(self):
        """Inverse selection"""

        objects = self.resultsOlv.GetObjects()
        for obj in objects:
            self.resultsOlv.SetCheckState(
                obj, not self.resultsOlv.GetCheckState(obj)
            )
        self.resultsOlv.RefreshObjects(objects)

    def ListCheckNotSel(self):
        """No select channals """

        objects = self.resultsOlv.GetObjects()
        for obj in objects:
            self.resultsOlv.SetCheckState(obj, False)
        self.resultsOlv.RefreshObjects(objects)


class ModifyFrame(wx.Frame):
    """"""
    def __init__(self):
        """Constructor"""
        title = "ModifyApk--FishingJoy"
        wx.Frame.__init__(self, parent=None, title=title, size=(800, 550))
        self.CenterOnScreen()
        panel = ModifyPanel(self)
"""
if __name__ == '__main__':
    app = wx.App(False)
    frame = ModifyFrame()
    frame.Show()
    app.MainLoop()
"""