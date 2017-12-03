import xlwt
import scrapy
import urllib.request
from bs4 import BeautifulSoup
import time
import os

# comments:一页的comments数
# comments_list:数据存放处
# 二元数组 len[[]] 数组长度相比 len[] 会加 + 1


class Spider(object):

    def __init__(self):
        self.url = "http://www.miui.com/thread-11018798-1-1.html"


class MySpider(scrapy.Spider):
    name = 'forum_spider'

    # 于初始该类 开始计时
    start_time = time.time()

    # 创建excel并填充列名
    wb = xlwt.Workbook()
    sh = wb.add_sheet('A Test Sheet')

    # 初始table_list列表
    table_list = []

    # 初始化进度条和最大页数
    max_num = ''
    grabbed_pages = 0

    def start_requests(self):

        first_url = self.get_first_url()

        page = urllib.request.urlopen(first_url)
        html = page.read().decode('utf-8')
        soup = BeautifulSoup(html, "html.parser")
        last_page = soup.select('.last')
        self.max_num = str(last_page[0].getText())[4:]

        base_url = str(first_url)[:-8]
        bash_url = str(first_url)[-7:]

        for num in range(1, 7):  # int(max_num) + 1

            url = base_url + str(num) + bash_url
            yield scrapy.Request(url=url, callback=self.parse, meta={'current_page': num})

    def parse(self, response):

        soup = BeautifulSoup(response.text, "html.parser")
        table_list = soup.select('.plhin')

        filename = self.get_filename(soup)  # 抓取文件名

        for table in table_list:
            item = []
            page = response.meta['current_page']
            floor = self.get_floor(table)
            issue_time = self.get_issue_time(table)
            author = self.get_author(table)
            phone_type = self.get_phone_type(table)
            miui_type = self.get_miui_type(table)
            title = self.get_title(table)

            comment_list = self.get_comment(table)  # get_comment返回一个数组，如果有quote长度为2
            quote = ''
            if len(comment_list) > 1:
                comment = comment_list[0]
                quote = comment_list[1]
            else:
                comment = comment_list[0]

            item.append(page)
            item.append(floor)
            item.append(issue_time)
            item.append(author)
            item.append(phone_type)
            item.append(miui_type)
            item.append(title)
            item.append(comment)
            item.append(quote)

            self.table_list.append(item)

            for j in item:  # 遍历item中的各元素
                print('item: ' + str(j))

        # 抓取完一页内容，grabbed_pages + 1
        self.grabbed_pages = self.grabbed_pages + 1

        # 显示进度条
        print('--- Progress --- : ' + str(self.grabbed_pages) + '/' + str(self.max_num))

        # 判断进度，如果为100%，则写入文件
        if self.grabbed_pages == 6:
            self.write_2_excel(filename)

    # 如果grabbed_pages累加之和等于最大页数，写入excel
    def write_2_excel(self, filename):

        # 初始列名
        self.init_excel()

        # 第一行是列名，所以 i + 1
        for i in range((len(self.table_list))):
            for j in range(len(self.table_list[i])):
                self.sh.write(i + 1, j, self.table_list[i][j])
                # print('comment: ' + self.comments_list[i][1])

        # 结束计时，并计算总用时
        self.sh.write(1, 9, str(time.time() - self.start_time)[:4] + '秒')

        # 保存文件
        save_path = '/Users/haoranwang/Desktop/miui_forum'
        complete_name = os.path.join(save_path, filename)
        self.wb.save(complete_name)
        print("--- 用时 ---" + str(time.time() - self.start_time)[:4] + '秒')

    def init_excel(self):
        self.sh.write(0, 0, '页码')
        self.sh.write(0, 1, '楼层')
        self.sh.write(0, 2, '发布时间')
        self.sh.write(0, 3, '作者')
        self.sh.write(0, 4, '手机型号')
        self.sh.write(0, 5, 'MIUI')
        self.sh.write(0, 6, '称号')
        self.sh.write(0, 7, '评论')
        self.sh.write(0, 8, '引用')
        self.sh.write(0, 9, '用时')

    @staticmethod
    def get_first_url():
        return Spider().url

    @staticmethod
    def get_filename(soup):
        bm_div = soup.find('div', {'class': 'bm cl'})
        filename = bm_div.contents[1].contents[-2].getText()
        return filename + '.xls'

    # 抓取楼层
    @staticmethod
    def get_floor(table):

        floor_1 = table.find('a', {'class': 'floors_1'})
        floor_2 = table.find('a', {'class': 'floors_2'})
        floor_3 = table.find('a', {'class': 'floors_3'})
        floor_4 = table.find('a', {'class': 'floors_4'})
        floor_normal = table.find('a', {'class': 'floors_normal'})
        if floor_1:
            return 1
        elif floor_2:
            return 2
        elif floor_3:
            return 3
        elif floor_4:
            return 4
        else:
            # print('floor: ' + floor_normal.contents[1].getText())
            floor = int(floor_normal.contents[1].getText())
        return floor

    @staticmethod
    def get_issue_time(table):
        pi_div = table.find('div', {'class': 'pti'})
        z_div = pi_div.find('div', {'class': 'z'})
        issue_time = z_div.contents[1].getText()
        return issue_time

    @staticmethod
    def get_author(table):

        author = table.find('a', {'class': 'xw1'}).getText()

        return author

    @staticmethod
    def get_phone_type(table):

        # contents[1],[3],[5],[7],[9]为空
        dl_list = table.find('dl', {'class': 'pil cl'})
        phone_type = dl_list.contents[5].getText()

        return phone_type

    @staticmethod
    def get_miui_type(table):

        # contents[1],[3],[5],[7],[9]为空
        dl_list = table.find('dl', {'class': 'pil cl'})
        miui_type = dl_list.contents[11].getText()

        return miui_type

    @staticmethod
    def get_title(table):

        div_list = table.find('div', {'class': 'pi'})
        title = div_list.find_next_sibling().find_next_sibling().getText()

        return title

    # get_comment返回一个数组，如果有quote长度为2
    @staticmethod
    def get_comment(table):

        td = table.find('td', {'class': 't_f'})

        # 清除掉<br/>
        for e1 in td.findAll('br'):
            e1.extract()

        # 判断有无quote，有则拼接好添加至item最后，并从comment中删除
        quote = ''
        for quote_div in td.findAll('div', {'class': 'quote'}):

            if quote_div:
                quote = '( ' + quote_div.blockquote.contents[0].getText() + ' ) ' + quote_div.blockquote.contents[1]
                quote_div.extract()
                # print(quote)

        comment = td.getText()
        # print(comment)

        comment_list = list([])
        comment_list.append(comment)
        if quote:
            comment_list.append(quote)

        return comment_list
