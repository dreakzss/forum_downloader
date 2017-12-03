import xlwt
import scrapy
import urllib.request
from bs4 import BeautifulSoup
import time

# comments:一页的comments数
# comments_list:数据存放处
# 二元数组 len[[]] 数组长度相比 len[] 会加 + 1


class Spider(object):

    def __init__(self):
        self.url = "http://www.miui.com/thread-11018798-1-1.html"
        self.saved = 'fd2.xls'


class MySpider(scrapy.Spider):
    name = 'forum_spider'

    start_time = time.time()

    # 创建excel并填充列名
    wb = xlwt.Workbook()
    sh = wb.add_sheet('A Test Sheet')
    sh.write(0, 0, '页码')
    sh.write(0, 1, '评论')

    # 初始comment列表
    comments_list = []

    max_num = ''
    grabbed_pages = 0

    total = 0
    spider = Spider()

    @staticmethod
    def get_first_url(self):
        return self.spider.url

    @staticmethod
    def get_saved(self):
        return self.spider.saved

    def start_requests(self):

        first_url = self.get_first_url(self)

        page = urllib.request.urlopen(first_url)
        html = page.read().decode('utf-8')
        soup = BeautifulSoup(html, "html.parser")
        last_page = soup.select('.last')
        self.max_num = str(last_page[0].getText())[4:]

        print('max_num: ' + self.max_num)

        base_url = str(first_url)[:-8]
        bash_url = str(first_url)[-7:]

        for num in range(1, 7):  # int(max_num) + 1

            url = base_url + str(num) + bash_url
            yield scrapy.Request(url=url, callback=self.parse, meta={'current_page': num})

    def parse(self, response):
        comments = BeautifulSoup(response.text, 'lxml').select('.t_f')
        num = len(comments)
        i = 0

        while i < num:
            a = comments[i].getText()
            b = str(response.meta['current_page'])
            item = []
            item.append(int(b))
            item.append(a)
            self.comments_list.append(item)
            i = i + 1

        # 抓取完一页内容，grabbed_pages + 1
        self.grabbed_pages = self.grabbed_pages + 1
        if self.grabbed_pages == 6:
            self.write()

    # 如果grabbed_pages累加之和等于最大页数，写入excel
    def write(self):
        print('write2Excel')

        print('len: ' + str(len(self.comments_list)))

        # 第一行是列名，所以 i + 1
        for i in range((len(self.comments_list))):
            for j in range(len(self.comments_list[i])):
                self.sh.write(i + 1, j, self.comments_list[i][j])
                #print('comment: ' + self.comments_list[i][1])

        self.wb.save(self.get_saved(self))
        print("--- 用时 ---" + str(time.time() - self.start_time)[:4] + '秒')

