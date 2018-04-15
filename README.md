# ncwu_crawler  
### 功能  
爬取华北水利水电大学的[通知页面](http://www5.ncwu.edu.cn/channels/5.html)，可指定开始页面和结束页面。  
### 爬取格式:  
1. 若通知文章无附件，则直接将通知正文保存为文本文件，文件名为 [部门][标题][创建时间]。  
![无附件例子](https://s1.ax1x.com/2018/04/15/CeA0mD.png)  
2. 若通知文章带有附件，则创建一个文件夹，放置通知正文和所有附件。  
![有附件例子](https://s1.ax1x.com/2018/04/15/CekzWt.png)  
### 依赖   
[requests](http://docs.python-requests.org/en/master/)  
[bs4](https://www.crummy.com/software/BeautifulSoup/)  
### 测试平台  
ubuntu 16.04  


