import re
import urllib.request
import os


class ShufaAlbum:
    def __init__(self, name, path, count):
        self.name = name
        self.path = path
        self.count = count

    name = ''
    path = ''
    count = 1


# 书法作品名，链接，页数
shufa_pages = {
    ShufaAlbum('王女节墓志', 'http://www.yac8.com/news/10749', 7),
}


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


def get_image(path, index, dir):
    request = urllib.request.urlopen(path)
    contents = request.read().decode('gbk')
    url_list = re.findall(r'http.+\.jpg', contents)
    for url in url_list:
        # 过滤引导图
        if url.__contains__('infoImg'):
            continue
        save_path = dir + '\\' + str(index) + '.jpg'
        print('downloading: ' + url)
        print('save to: ' + save_path)
        f = open(save_path, 'wb')
        request = urllib.request.urlopen(url)
        buf = request.read()
        f.write(buf)
        f.close()


# 创建本地保存文件夹，并下载保存图片
if __name__ == '__main__':
    for sf_album in shufa_pages:
        album_name = sf_album.name
        intro_path = sf_album.path
        max_count = sf_album.count

        mkdir(album_name)
        print('开始下载%s 1-%d页...' % (album_name, max_count))
        for i in range(1, max_count+1):
            if i == 1:
                url_path = str(intro_path + ".html")
            else:
                url_path = str(intro_path + "_" + str(i) + ".html")
            get_image(url_path, i, album_name)

