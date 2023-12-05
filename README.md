# Pixiv - Web crawler❤

# 此版本的代码已不可用，请等待后续维护和修改。

> 由SN-Grotesque开发并维护

> 关于此代码的开发和维护：<br>
> 请你仔细<a href="#DM_Document">阅读文档</a>

> 主要采用Cookie对Pixiv网站进行爬取。<br>
> 不涉及任何登录操作，只要你拥有自己的Cookie，那么你就可以使用此程序。<br>
> 如果你不知道Cookie如何获取，请仔细<a href="#Cookie_Help">阅读文档</a>。

> 此Pixiv代码库使用Python3进行开发，如果你的电脑没有Python3。<br>
> 请访问此<a href="https://www.python.org/downloads">链接</a>进行下载并安装。<br>
> 请使用版本号大于等于<kbd>3.7.5</kbd>的Python程序。<br>
> 安装完毕之后请在你的计算机中设置环境变量以确保你可以正常使用Python。<br>
> 请仔细<a href="#Python_Help">阅读文档</a>。

> 本Pixiv库采用了部分Python第三方库。<br>
> 如果你的计算机中未安装这些库请仔细<a href="#Modules_Help">阅读文档</a>。

<span id="DM_Document">开发和维护文档</span>
```text
初始化类中的变量名有前缀
    DEFINED 表示此变量作为参数使用或初始定义
    RESULTS 表示此变量作为结果保存

在类方法中
    GetArtistInfo       作用是获取指定ID的关注列表所有用户的ID和名字
        传入一个参数，参数类型可以是str或int，最好是你自己的ID
        返回值          None
        结果保存至      self.RESULTS_ArtistInfo
    
    MultiThreadGetArtworks  作用是获取指定用户的所有作品链接
        传入一个参数，参数类型可以是str或int，为作者ID
        返回值              None
        结果保存至          self.RESULTS_ArtworkLinks
                            self.RESULTS_PictureLinks
    
    MultiThreadDownloadArtwork  作用是下载列表中的作品至指定目录
        传入三个参数
                                artworkUrl 类型为List[str]
                                folder     类型为str
                                zipToMp4   类型为bool（可选参数，默认为True）
        返回值                  None
        无结果
```

<span id="Cookie_Help">Cookie 帮助文档</span>
```text
1.  首先打开你的电脑浏览器(此处以Microsoft Edge为例)

2.  进入你的Pixiv主页，点击关注按钮查看关注的用户。
    此时你浏览器上方地址栏的地址应该是这样的
        https://www.pixiv.net/users/你的用户ID/following
    或这样的
        https://www.pixiv.net/users/你的用户ID/following?p=数字

3.  按压并释放你键盘上的F12功能键(它一般在键盘的第一排最后几个)
    或是按照下面的步骤来
        点击浏览器右上角的三个点 -> 更多工具 -> 开发人员工具
    如果窗口跳出来了之后没有中文(你看不懂英文的话)
        点击窗口右上角的设置图标 -> Language -> 中文简体

4.  关掉设置，返回开发人员工具主页面，点击菜单栏中的”网络“
    在”保留日志“与”禁用缓存“那一栏的下方找到下面这一栏内容
        全部 Fetch/XHR JS CSS img 媒体....
    然后勾选"Fetch/XHR"

5.  按住你键盘上的Ctrl键(它一般在键盘最左下角)，并按R键。
    松开所有按键，此时浏览器页面会刷新，并在”开发人员工具“的
    页面窗口中多出几条数据。

    找到名称前部为"following?offset=数字&limit=24"的那一条数据
    用鼠标左键点击它，查看内容。

6.  在跳出的侧边窗口中往下滑动鼠标滚轮，在请求标头找到cookie那一项
    鼠标右键点击它”复制值“

    再将它保存在某个文件中，这样你就拥有自己的Cookie数据了(不过请注意
    不要泄露给他人)
```

<span id="Python_Help">Python 帮助文档</span>

```text
通过链接安装完成Python之后，请按照以下的步骤设置环境变量。
此处使用Windows 10 21H2版本演示。

1.  鼠标右键点击桌面上的”此电脑 -> 属性“
    (如果”此电脑“为快捷方式，请按Win键(它一般在Ctrl键旁边)+I键打开设置，”系统 -> 关于“)，
    在窗口找到高级系统设置并点击。
    在新窗口找到”高级 -> 环境变量“，在系统变量那一栏，
    找到变量为”Path“的一行双击它，之后点击跳出的窗口中的空白行，
    在右侧”浏览“中定位到你Python的安装路径。

    完成之后点击确认，所有环节打开的窗口全部保存退出。

2.  按住键盘中的Win键，再按R键，松开按压。
    输入cmd之后按回车键，在命令行窗口输入python或python3。
    如果正确进入Python的交互页面就代表可以正常使用Python。
    如果不行，请仔细检查上面的每一个步骤。

3.  如果你需要更换Pip源，请阅读此链接：
        https://blog.csdn.net/weixin_42640909/article/details/112142215
```

<span id="Modules_Help">模块帮助文档</span>
```text
Requests库用作爬取指定URL的内容
cv2是一个图像处理库，用作jpg转MP4
    关于为什么不是转gif，原因如下
    在同帧率同时长的情况下，Gif比MP4更占用空间，并且表现也不如MP4

如果你需要安装此库请通过如下的指令进行安装
    python -m pip install requests opencv-python
```
