# scrapy-images360
### 目标
>抓取360图片http://image.so.com/index.html 
>熟悉pipeline 以及 ImagesPipeline用法

### 网站分析
* 往下拖动网页，到底后新的30张图片会自动加载，url无变化，打开开发工具确认，每次刷新均产生ajax请求
* 防爬策略基本没有

### 抓取结果
* ImagePipeline功能正常，根据每个item['url']自动下载图片并命名、放入指定目录。
* MysqlPipeline功能正常（需要提前在mysql中创建需要的库、表）。
* MongoPipeline功能正常（不需要提前创建库、表）。

结果展示：

<img align="center" src="https://github.com/Bigbenen/scrapy-images360/blob/master/aa.png" width=50%  >

<img src="https://github.com/Bigbenen/scrapy-images360/blob/master/a.jpg" width=50% >
