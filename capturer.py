import re
import urllib.request
import os

WEBSITE = "http://www.yac8.com"

# 书法作品名，链接，页数
class ShufaAlbum:
    def __init__(self, name, path, count):
        self.name = name
        self.path = path
        self.count = count

    name = ''
    path = ''
    count = 1


# 创建保存图片的文件夹
def mkdir(path):
    path = path.strip()
    #  判断路径是否存在
    #  存在    True
    #  不存在  Flase
    is_exists = os.path.exists(path)
    if not is_exists:
        print('新建了名字叫做', path, '的文件夹')
        #  创建目录操作函数
        os.makedirs(path)
        return True
    else:
        #  如果目录存在则不创建，并提示目录已经存在
        print('名为', path, '的文件夹已经创建成功')
        return False


def get_image(path, page_no, save_dir):
    page_no_in = page_no
    request = urllib.request.urlopen(path)
    contents = request.read().decode('gbk')
    url_list = re.findall(r'http.+?\.jpg', contents)
    src_file = re.findall(r'src=\".+?.jpg\"', contents)
    if src_file:
        for file in src_file:
            url_site = file[5:-1]
            url_site = url_site.replace('..', WEBSITE)
            url_list.append(url_site)
    for url in url_list:
        # 过滤引导图（带字母） ssdb3247788.jpg
        # 碑帖图 （纯数字） 134241.jpg
        if not re.findall(r'/[0-9]+.jpg', url):
            print('Filter ', url)
            continue
        save_path = save_dir + '\\' + str(page_no) + '.jpg'
        print('downloading: ' + url)
        print('save to: ' + save_path)
        f = open(save_path, 'wb')
        request = urllib.request.urlopen(url)
        buf = request.read()
        f.write(buf)
        f.close()
        page_no += 1
    return page_no - page_no_in


# 创建本地保存文件夹，并下载保存图片
def download_album(sf_album):
    album_name = sf_album.name
    intro_path = sf_album.path
    max_count = sf_album.count

    if intro_path.__contains__(".html"):
        intro_path = intro_path[0:-5]
    album_name = album_name.replace(':', '-')

    try:
        made = mkdir(album_name)
        if not made:
            files = os.listdir(album_name)
            if files.__len__() >= max_count:
                return
    except NotADirectoryError as e:
        print(e)
        return
    print('开始下载%s 1-%d页...' % (album_name, max_count))
    page_no = 1
    for i in range(1, max_count+1):
        if i == 1:
            url_path = str(intro_path + ".html")
        else:
            url_path = str(intro_path + "_" + str(i) + ".html")
        try:
            page_no += get_image(url_path, page_no, album_name)
        except urllib.error.HTTPError as e:
            print(e)
            break



