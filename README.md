# wechat_program
个人练习小程序入门项目, 通过 scrapy 爬取豆果美食热门数据, 使用 flask 搭建后端, 最后搭建一个简单的小程序

### 项目效果
![image](https://github.com/yhs111/wechat_program/blob/master/images/img_1.png)
![image](https://github.com/yhs111/wechat_program/blob/master/images/img_2.png)
![image](https://github.com/yhs111/wechat_program/blob/master/images/img_3.png)

### 开始
下载第三方库和微信开发者工具, 在这之前必须要安装 mongoDB(http://mirrors.aliyun.com/mongodb/yum/redhat/8/mongodb-org/4.2/x86_64/RPMS/)

(1) 下载 python 第三方库
```bash
python requirements.txt
```
(2) 下载微信开发者工具(https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html)

### 启动
(1) 切换到 flask/douguo/ 目录下, 启动 scrapy, 爬取数据, 在这之前要启动 mongodb 服务
```bash
python start_spider.py
或
scrapy crawl toutiao
```

(2) 切换到 flask 目录下, 执行 start.py 文件
```bash
python start.py
```
(3) 最后打开微信开发者工具选择导入项目

