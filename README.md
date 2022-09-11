# Pixiv - Web crawler❤

> 由SN-Grotesque开发并维护

> 主要采用Cookie对Pixiv网站进行爬取。<br>
> 不涉及任何登录操作，只要你拥有自己的Cookie，那么你就可以使用此程序。<br>
> 如果你不知道Cookie如何获取，请仔细<a href="#Cookie_Help">阅读文档</a>。

> 本Pixiv代码库采用requests网络请求库<br>
> 如果你的计算机中未安装此库请仔细<a href="#Cookie_Help">阅读文档</a>。

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
