import urllib.request
from bs4 import BeautifulSoup
import time

first_url = "http://www.miui.com/thread-11018798-5-1.html"
#start_time = time

def get(first_url):

    start_time = time.time()

    page = urllib.request.urlopen(first_url)
    html = page.read().decode('utf-8')

    soup = BeautifulSoup(html, "html.parser")
    table_list = soup.select('.plhin')

    item_list = []

    for table in table_list:
        item = []
        floor = get_floor(table)
        author = get_author(table)
        phone_type = get_phone_type(table)
        miui_type = get_miui_type(table)
        title = get_title(table)

        comment_list = get_comment(table)  # get_comment返回一个数组，如果有quote长度为2
        quote = ''
        if len(comment_list) > 1:
            comment = comment_list[0]
            quote = comment_list[1]
        else:
            comment = comment_list[0]

        item.append(floor)
        item.append(author)
        item.append(phone_type)
        item.append(miui_type)
        item.append(title)
        item.append(comment)
        item.append(quote)

        # print(str(len(item)))

        for j in item:  # 遍历item中的各元素
            print('item: ' + str(j))

        item_list.append(item)
        print("--- seconds ---" % (time.time() - start_time))


        # print('item: ' + str(j) + ' len: ' + str(len(j)))


# 抓取楼层
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


def get_author(table):
    author = table.find('a', {'class': 'xw1'}).getText()

    return author


def get_phone_type(table):
    # contents[1],[3],[5],[7],[9]为空
    dl_list = table.find('dl', {'class': 'pil cl'})
    phone_type = dl_list.contents[5].getText()

    return phone_type


def get_miui_type(table):
    # contents[1],[3],[5],[7],[9]为空
    dl_list = table.find('dl', {'class': 'pil cl'})
    miui_type = dl_list.contents[11].getText()

    return miui_type


def get_title(table):
    div_list = table.find('div', {'class': 'pi'})
    title = div_list.find_next_sibling().find_next_sibling().getText()

    return title


# get_comment返回一个数组，如果有quote长度为2
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

    comment_list = []
    comment_list.append(comment)
    if quote:
        comment_list.append(quote)

    return comment_list


get(first_url)