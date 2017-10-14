# !/usr/bin/python
# -*- coding: utf-8 -*-

import bs4
import requests

def get_html(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        # 网站使用的是gbk编码
        r.encoding = 'gbk'
        return r.text
    except:
        return 'Error'

def get_content(url):
    html = get_html(url)
    soup = bs4.BeautifulSoup(html, 'lxml')

    # 找到电影排行榜的ul列表
    movies_list = soup.find('ul', class_='picList clearfix')
    movies = movies_list.find_all('li')

    for top in movies:
        # 找到图片链接
        img_url = top.find('img')['src']
        name = top.find('span', class_='sTit').a.text

        # 处理没有上映时间的电影
        try:
            time = top.find('span', class_='sIntro').text
        except:
            time = '暂无上映时间'

        # 使用bs4库迭代出’pActor‘的所有子孙节点，即每一位演员
        # 解决名字分割的问题
        actors = top.find('p', class_='pActor')
        actor=''
        for act in actors.contents:
            actor = actor + act.string + ' '
        # 找到电影简介
        intro = top.find('p', class_='pTxt pIntroShow').text
        print('名片: %s\t%s\n%s\n%s\n\n' % (name, time, actor, intro))

        # 图片
        with open('./movie_images/' + name + '.png', 'wb+') as f:
            # 从url中以二进制格式下载图片数据
            # 注意处理图片的链接
            f.write(requests.get('http:' + img_url).content)

def main():
    url = 'http://dianying.2345.com/top/'
    get_content(url)

if __name__ == '__main__':
    main()