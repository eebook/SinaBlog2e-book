# jianshu2e-book

## 简介
爬取[简书](http://www.jianshu.com)上的文章，制作成Epub格式的电子书（同时生成html格式文件）  
</br>
例如，将[王垠](http://www.jianshu.com/users/b1dd2b2c87a8/latest_articles)在简书上的所有文章爬取下来制作电子书：

网页版：   

![hanhanhtml](http://7xi5vu.com1.z0.glb.clouddn.com/2016-02-02-SinaBloghanhanhtml.png?imageView/2/w/619/q/90)

## 开发环境
Mac 			10.11   
Python 			2.7.11    
BeautifulSoup 	4    
目前完成度不高，bug还比较多，Win，Linux平台下还没有测试过，有可能存在问题。

## 使用说明 
1. 将博客地址放入项目文件夹目录的ReadList.txt中，例如：  
![readlist](http://7xi5vu.com1.z0.glb.clouddn.com/2016-02-02-SinaBlogReadList.png?imageView/2/w/619/q/90)
需要说明的一点是：目前只支持ID形式的博客地址，例如http://blog.sina.com.cn/u/1191258123。新浪微博支持多种形式的地址，如：http://blog.sina.com.cn/1191258123, http://blog.sina.com.cn/twocold, 以及http://blog.sina.com.cn/u/1191258123. 目前只支持一种，后面会改进。

2. 执行：  
```shell
$ python SinaBlog2e-book.py
```

稍等片刻，html和Epub格式的电子书会生成在「生成的电子书」文件夹中。

## 依赖
 * [Beautiful Soup 4](http://www.crummy.com/software/BeautifulSoup/)(已经放在项目目录中，不需要下载)
 * [lxml](http://lxml.de/)     
  
 ```shell
$ pip install lxml
```  

## 项目说明
**该项目只是[ZhihuHelp](https://github.com/YaoZeyuan/ZhihuHelp)的新浪博客版本，目前大量用到[ZhihuHelp](https://github.com/YaoZeyuan/ZhihuHelp)项目的代码，再次表示感谢。也请大家多多支持该项目作者[姚泽源](https://github.com/YaoZeyuan)同学。**

## TODO list  
本着「过早优化是万恶之源」的原则（好吧，就是代码写得烂），目前这个项目还算能用，但是问题也比较多，写个TODO list: 

0. 支持多种形式的新浪博客地址 
1. 效率问题，程序还需要优化（爬韩寒博客，一共316篇博文，用了36分钟）  
2. 页面的样式还需要改进（如：封面，简介，标题，博主logo等）  
3. 博文评论的数量  
4. 博文更新时间    
5. 图形界面
6. 程序接口  
7. 分卷制作电子书， 多个博主的文章放在同一本书中
8. ....

## License
[MIT](http://opensource.org/licenses/MIT)