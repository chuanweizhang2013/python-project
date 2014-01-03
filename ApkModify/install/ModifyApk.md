				ModifyApk--apk资源修改工具

使用这个工具注意点：

1.需要安装JDK1.6并且配置环境，在cmd输入jarsigner如果出现jarsigner帮助，表示配置成功就可以使用本工具

2.渠道资源配置可以参考ChannelResConfig.yaml

(1)其中资源目录 "../../../Resource/FinalResources 1 iPad iPhone"

参数之间用空格分割

第一个参数表示资源的位置

第二个参数表示是否展开资源

第三个及之后的参数表示过滤文件及文件夹

(2)

Resource_android 表示配置android的资源

Resource_java 表示配置java的资源

OutPut_name 表示输出名字,如果没有则使用渠道名字


=============下面是python安装环境==========

1.此工具使用python编写，安装软件如下：

以下是环境的安装步骤，目录下已经包含安装的包，当然你也可以网上下载

①安装 Python2.7   
 有分为32位版本,和64位版本	[www.python.org/download](www.python.org/download "python")

②安装 UI界面库 wxPython : [http://www.wxpython.org/](http://www.wxpython.org/ "wxPython")

③安装 编辑器 Ulipad 		 [https://code.google.com/p/ulipad/](https://code.google.com/p/ulipad/ "Ulipad")

在安装这个之前要先安装 Comtypes :
 [http://sourceforge.net/projects/comtypes/files/comtypes/0.6.2/](http://sourceforge.net/projects/comtypes/files/comtypes/0.6.2/ "comtypes")
	
	备注：
		在用python安装comtypes时，可能会报如此的错误：
		from distutils.core import setup, Command, DistutilsOptionError 
		ImportError: cannot import name DistutilsOptionError
		碰到这样的错误 ，我们可以简单的更改一下comtypes目录下的setup.py文件的第42行
		将from distutils.core import setup, Command, DistutilsOptionError 
		改为from distutils.core import setup, Command 
		from distutils.errors import DistutilsOptionError

这里个人推荐个编辑器 PyScripter 个人感觉比较好用 [https://code.google.com/p/pyscripter/](https://code.google.com/p/pyscripter/ "pyscripter")



④ 安装ObjectListView-1.2--modify   

这个注意，必须安装本地的jectListView-1.2--modify包

 python setup.py install

 [https://pypi.python.org/pypi/ObjectListView](https://pypi.python.org/pypi/ObjectListView "ObjectListView")

这个ObjectListView是网上开源的ListCtrl的扩展，这个我个人对他进行了小部分的修改，所以必须安装我修改过的这个才可以使用，上面这个链接是没修改过的


⑤安装 pyyaml

[http://pyyaml.org/](http://pyyaml.org/ "pyyaml")

python setup.py install

如果上面的命令安装失败,那么使用下面这个方法

python setup.py --without-libyaml install