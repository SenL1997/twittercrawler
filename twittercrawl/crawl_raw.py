# encoding=utf-8
'''
Created on 5/30/2017

@author: Sen Li
'''
import codecs
import random
import sys

import requests
from bs4 import BeautifulSoup

sys.getdefaultencoding()
f = codecs.open('t.txt', 'w', encoding='utf-8')

ids = [
    1390077032,
    25073877,
    822215673812119553,
    2827613550,
    166862944,
    781651968729161728,
    793105171,
    399811923,
    464779261,
    764555761179656192,
    16526776,
    2654478201,
    869415374957101056,
    1490340577,
    1350460646,
    3437553407
]

Agent = [
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
    'Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11'
]

Month = {
    'Mar': 3,
    'Aug': 8
}


def id2name(user_id):
    '''Convert user_id to user_name'''
    agent = random.choice(Agent)
    headers = {
        'User-Agent': agent
    }
    url = 'https://tweeterid.com/ajax.php'
    result = requests.post(url, {'input': user_id}, headers=headers)
    return result.text.split('@')[1]


def get_information(user_id):
    '''Return name, tweet_count, following, follower, favorite, list_count, location, join_date'''
    agent = random.choice(Agent)
    headers = {
        'User-Agent': agent
    }
    URL = 'https://twitter.com/'
    name = id2name(user_id)
    url = URL + name
    html = BeautifulSoup(requests.get(url, headers=headers).text, 'html5lib')
    profileNav_list = html.find(
        'ul', {'class': 'ProfileNav-list'}).find_all('li', {'class': 'ProfileNav-item'})
    tweet_count = profileNav_list[0].find(
        'span', {'class': 'ProfileNav-value'})['data-count']
    following = profileNav_list[1].find(
        'span', {'class': 'ProfileNav-value'})['data-count']
    follower = profileNav_list[2].find(
        'span', {'class': 'ProfileNav-value'})['data-count']
    list_count = '0'
    favorite = profileNav_list[3].find('span', {'class': 'ProfileNav-value'})
    if favorite.text != 'More ':
        favorite = favorite['data-count']
        list_count = profileNav_list[4].find(
            'span', {'class': 'ProfileNav-value'}).text
        if list_count == 'More ':
            list_count = '0'
    else:
        favorite = '0'
    profileheader = html.find('div', {'class': 'ProfileSidebar'}).find(
        'div', {'class': 'ProfileHeaderCard'})
    location = profileheader.find('span', {
        'class': 'ProfileHeaderCard-locationText', 'dir': 'ltr'}).text.split('<span')[0].strip()
    f.write(location + '\r\n')
    join_date = profileheader.find(
        'span', {'class': 'ProfileHeaderCard-joinDateText', 'dir': 'ltr'})['title']
    return name, tweet_count, following, follower, favorite, list_count, location, join_date


def main():
    for i in ids:
        print(get_information(i))


if __name__ == '__main__':
    main()
