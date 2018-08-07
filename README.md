## [notice.py](https://github.com/mozjiang/ncwu_crawler/blob/master/notice.py)  
### 功能  
爬取华北水利水电大学的[通知页面](http://www5.ncwu.edu.cn/channels/5.html)，可指定开始页面和结束页面。  
### 爬取格式:  
1. 若通知文章无附件，则直接将通知正文保存为文本文件，文件名为 [部门][标题][创建时间]。  
![无附件例子](https://s1.ax1x.com/2018/04/15/CeA0mD.png)  
2. 若通知文章带有附件，则创建一个文件夹，放置通知正文的文本文件和所有附件。  
文件夹:        
![有附件例子_文件夹](https://s1.ax1x.com/2018/04/16/CeEgUJ.png)  
内容:  
![有附件例子_](https://s1.ax1x.com/2018/04/15/CekzWt.png)  
### 依赖   
python3  
[requests](http://docs.python-requests.org/en/master/)  
[beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/)  
[lxml](http://lxml.de/)
### 使用方法  
1. clone 此仓库到本地   
2. 打开命令行， cd 到仓库目录 ncwu_crawler    
3. pip 安装依赖  `pip install -r requirements`  
4. 输入 python notice.py 运行  
### 测试平台  
ubuntu 16.04  
Windows 8,10  


