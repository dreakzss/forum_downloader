import re
import xlwt
from timeit import timeit
import scrapy
import urllib.request
from bs4 import BeautifulSoup
from scrapy.http import Request
from forum_downloader.items import ForumDownloaderItem

#

class MySpider(scrapy.Spider):
    name = 'forum_spider'

    wb = xlwt.Workbook()
    sh = wb.add_sheet('A Test Sheet')

    comments_list = []
    max_num =''
    grab_pages = 0

    def get_first_url(self):
        first_url = "http://www.miui.com/thread-11018798-1-1.html"
        return first_url

    def get_saved(self):

        file = 'fd1.xls'

        return file

    def start_requests(self):

        first_url = self.get_first_url()

        page = urllib.request.urlopen(first_url)
        html = page.read().decode('utf-8')
        soup = BeautifulSoup(html, "html.parser")
        last_page = soup.select('.last')
        self.max_num = str(last_page[0].getText())[4:]

        print('max_num: ' + self.max_num)

        base_url = str(first_url)[:-8]
        bash_url = str(first_url)[-7:]

        #print('base_Url: ' + base_url) #First_Url: http://www.miui.com/thread-11397653-
        #print('bash_Url: ' + bash_url)

        #for num in range(1, int(max_num) + 1):
        for num in range(1, 7):

            url = base_url + str(num) + bash_url
            yield scrapy.Request(url=url, callback=self.parse)
            # print('url: ' + url)


    def parse(self, response):
        #print(response.text)
        comments = BeautifulSoup(response.text, 'lxml').select('.t_f')
        num = len(comments)
        i = 0
        while (i < num):
            a = comments[i].getText()
            print(a)
            self.comments_list.append(a)
            i = i + 1
        self.grab_pages = self.grab_pages + 1
        self.write()


    def write(self):
        print('write2')
        #while (self.grab_pages == int(self.max_num)):
        if self.grab_pages == 6:

            for k in range(len(self.comments_list)):
                self.sh.write(k, 0, self.comments_list[k])
            self.wb.save(self.get_saved())


    #comments:一页的comments数
    #comments_list:数据存放处
