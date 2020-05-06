# WeChat
微信公众号文章爬虫
----------------------------------
###基本配件

ProxyPool

[CookiePool](https://github.com/dongrunhua/wechat_cookie_pool)
----------------------------------
###输入excel格式
| 字段    | 说明|
|  :------: |  :------: |
| 关键词 |公众号或者关键词|
| top  | 如果字段一为公众号，top值为0。如果是关键词，top值>=1，表示此类关键词搜索的结果列表前top个 |
----------------------------------
###主要思路
配置好ProxyPool、CookiePool，将待爬的公众号或者公众号关键词写入到excel中，将excel地址赋值给settings里面的FilePath变量。先启动url，它会根据excel中的关键词爬取到公众号的列表文章接口，在启动gongzhonghao，它会爬取文章列表接口得到每篇文章的链接。
