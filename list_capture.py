import re
import urllib.request
import os
from lxml import etree
from bs4 import BeautifulSoup
from capturer import ShufaAlbum
import capturer

WEBSITE = "http://www.yac8.com"
LIST_PATH = "http://www.yac8.com/news/?list_topic-32.html"
LIST_PAGES = 7
TEST_ALBUM = "http://www.yac8.com/news/13456.html"
album_no = 0

# import HTMLParser
# class ShufaHTMLParser(HTMLParser):
#     def __init__(self):
#         HTMLParser.__init__(self)


def get_album_page_count(album_path):
    page_request = urllib.request.urlopen(album_path)
    page_contents = page_request.read().decode('gbk')

    page_scroll = re.findall(r'rel=\"nofollow\">.+?<', page_contents)
    max_page = 1
    for scroll in page_scroll:
        page_no = re.findall(r'[0-9]+', scroll)
        if page_no and (int(page_no[0]) > max_page):
                max_page = int(page_no[0])

    return max_page


def get_list(path):
    request = urllib.request.urlopen(path)
    contents = request.read().decode('gbk')
    # hp = ShufaHTMLParser()
    # hp.feed(contents)
    # hp.getresult()
    # print(hp)

    # hp = etree.HTMLParser
    # html = etree.parse('list_contents.txt', hp)
    # html = etree.fromstring(contents)
    # html = etree.fromstring(contents)
    # result = etree.tostring(html, pretty_print=True)

    soup = BeautifulSoup(contents, from_encoding='gbk')
    box = soup.find_all('div', class_='pageBox')
    global album_no
    albums = []
    for page in box:
        page_box = str(page.contents)
        album_list = re.findall(r'<div class=\"img\">.+?</div>', page_box)

        for album in album_list:
            print("Album: ", album)
            title = re.findall(r'title=\".+?\"', album)
            link = re.findall(r'../news/[0-9]+.html', album)
            if not link or (len(link) == 0):
                continue
            if not title or (len(title) == 0):
                continue
            link = WEBSITE + link[0][2:]
            title = title[0][7:-1]
            count = get_album_page_count(link)
            print('Album[%d]: %s(%s)[%d]' % (album_no, title, link, count))
            album_no += 1
            albums.append(ShufaAlbum(title, link, count))

    return albums


# main function
if __name__ == '__main__':
    intro_path = LIST_PATH

    if intro_path.__contains__(".html"):
        intro_path = intro_path[0:-5]

    for i in range(1, LIST_PAGES+1):
        if i == 1:
            url_path = str(intro_path + ".html")
        else:
            url_path = str(intro_path + "_" + str(i) + ".html")

        print("Get Albums from Page ", i)
        try:
            current_albums = get_list(url_path)
        except urllib.error.HTTPError as e:
            print(e)
            break

        for current_album in current_albums:
            capturer.download_album(current_album)

