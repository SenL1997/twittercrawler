# encoding=utf-8
'''
Created on 5/30/2017

@author: Sen Li
'''
import codecs
import random
import datetime

import requests
from bs4 import BeautifulSoup

Proxies = {
    'http':'socks5://127.0.0.1:1080',
    'https':'socks5://127.0.0.1:1080'
}

Agent = [
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
    'Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11'
]

Month = {
    'Jan':'1',
    'Feb':'2',
    'Mar':'3',
    'Apr':'4',
    'May':'5',
    'Jun':'6',
    'Jul':'7',
    'Aug':'8',
    'Sep':'9',
    'Oct':'10',
    'Nov':'11',
    'Dec':'12'
}


def id2name(user_id, proxies=None):
    '''Convert user_id to user_name'''
    agent = random.choice(Agent)
    headers = {
        'User-Agent': agent
    }
    url = 'https://tweeterid.com/ajax.php'
    if proxies is not None:
        result = requests.post(url, {'input': user_id}, headers=headers, proxies=proxies)
        return result.text.split('@')[1]
    else:
        result = requests.post(url, {'input': user_id}, headers=headers)
        return result.text.split('@')[1]


def get_information(user_inf, flag=0, proxies=None):
    ''' flag = 0 (default): user_name flag = 1: user_id\n
        Return name, tweet_count, following, follower, favorite, list_count, location, join_date
    '''
    agent = random.choice(Agent)
    headers = {
        'User-Agent': agent
    }
    URL = 'https://twitter.com/'
    name = user_inf
    if flag == 1:
        name = id2name(user_inf,proxies)
    url = URL + name
    html = 0
    if proxies is not None:
        html = BeautifulSoup(requests.get(url, headers=headers, proxies=proxies).text, 'html5lib')
    else:
        html = BeautifulSoup(requests.get(url, headers=headers).text, 'html5lib')
    profileNav_list = html.find('ul', {'class': 'ProfileNav-list'})
    following = '0'
    follower = '0'
    favorite = '0'
    list_count = '0'
    try:
        tweet_count = profileNav_list.find('li', {'class':'ProfileNav-item--tweets'}).find('span', {'class': 'ProfileNav-value'})['data-count']
    except:
        pass
    try:
        following = profileNav_list.find('li', {'class':'ProfileNav-item--following'}).find('span', {'class': 'ProfileNav-value'})['data-count']
    except:
        pass
    try:
        follower = profileNav_list.find('li', {'class':'ProfileNav-item--followers'}).find('span', {'class': 'ProfileNav-value'})['data-count']
    except:
        pass
    try:
        list_count = profileNav_list.find('li', {'class':'ProfileNav-item--lists'}).find('span', {'class': 'ProfileNav-value'}).text
    except:
        pass
    try:
        favorite = profileNav_list.find('li', {'class':'ProfileNav-item--favorites'}).find('span', {'class': 'ProfileNav-value'})['data-count']
    except:
        pass
    

    profileheader = html.find('div', {'class': 'ProfileSidebar'}).find(
        'div', {'class': 'ProfileHeaderCard'})
    location = profileheader.find('span', {
        'class': 'ProfileHeaderCard-locationText', 'dir': 'ltr'}).text.split('<span')[0].strip()
    location = location.replace(u'💗', '')
    join_date = profileheader.find(
        'span', {'class': 'ProfileHeaderCard-joinDateText', 'dir': 'ltr'})['title']
    join_date = join_date.split('-')[1].split(' ')
    year = join_date[3]
    month = Month[join_date[2]]
    day = join_date[1]
    join_date = (year+'-'+month+'-'+day)

    return name, tweet_count, following, follower, favorite, list_count, location, join_date

def get_status_information(status_id, proxies=None):
    '''Return user_id, text, time, reply, retweet, favorite'''
    url = 'https://twitter.com/'+'realdonaldtrump'+'/status/'+status_id
    agent = random.choice(Agent)
    headers = {
        'User-Agent':agent
    }
    html = 0
    if proxies is not None:
        html = BeautifulSoup(requests.get(url, headers=headers, proxies=proxies).text, 'html5lib')
    else:
        html = BeautifulSoup(requests.get(url, headers=headers).text, 'html5lib')
    user_id = html.find('div', {'class':'permalink-tweet-container'}).find('div', {'class':'js-initial-focus'})['data-user-id']
    text = html.find('div', {'class':'js-tweet-text-container'}).find('p', {'class':'js-tweet-text'}).text
    time = html.find('div', {'class':'client-and-actions'}).find('span', {'class':'metadata'}).text.strip()
    year = time.split(' ')[5]
    month = Month[time.split(' ')[4]]
    day = time.split(' ')[3]
    f = time.split(' ')[1]
    hour = time.split(' ')[0].split(':')[0]
    minute = time.split(' ')[0].split(':')[1]
    if f == 'PM':
        hour = str(int(hour) + 12)
    time = year+'-'+month+'-'+day+' '+hour+':'+minute+':'+'00'
    tweet_action = html.find('div', {'class':'ProfileTweet-actionCountList'})
    reply = tweet_action.find('span', {'class':'ProfileTweet-action--reply'}).find('span', {'class':'ProfileTweet-actionCount'})['data-tweet-stat-count']
    retweet = tweet_action.find('span', {'class':'ProfileTweet-action--retweet'}).find('span', {'class':'ProfileTweet-actionCount'})['data-tweet-stat-count']
    favorite = tweet_action.find('span', {'class':'ProfileTweet-action--favorite'}).find('span', {'class':'ProfileTweet-actionCount'})['data-tweet-stat-count']
    return user_id, text, time, reply, retweet, favorite


def test():
    user_id = '25073877'
    print(get_information(user_id, 1,Proxies))
    name = 'realDonaldTrump'
    print(get_information(name,0,Proxies))
    status = '870234811616677889'
    print(get_status_information(name, status,Proxies))


if __name__ == '__main__':
    test()
