# encoding=utf-8
'''
Created on 5/30/2017

@author: Sen Li
'''
import codecs
import random

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
    join_date = profileheader.find(
        'span', {'class': 'ProfileHeaderCard-joinDateText', 'dir': 'ltr'})['title']
    return name, tweet_count, following, follower, favorite, list_count, location, join_date

def get_status_information(user_name, status_id, proxies=None):
    '''Return text, time, reply, retweet, favorite'''
    url = 'https://twitter.com/'+user_name+'/status/'+status_id
    agent = random.choice(Agent)
    headers = {
        'User-Agent':agent
    }
    html = 0
    if proxies is not None:
        html = BeautifulSoup(requests.get(url, headers=headers, proxies=proxies).text, 'html5lib')
    else:
        html = BeautifulSoup(requests.get(url, headers=headers).text, 'html5lib')
    text = html.find('div', {'class':'js-tweet-text-container'}).find('p', {'class':'js-tweet-text'}).text
    time = html.find('div', {'class':'js-tweet-details-fixer'}).find('span', {'class':'metadata'}).text.strip()
    tweet_action = html.find('div', {'class':'ProfileTweet-actionCountList'})
    reply = tweet_action.find('span', {'class':'ProfileTweet-action--reply'}).find('span', {'class':'ProfileTweet-actionCount'})['data-tweet-stat-count']
    retweet = tweet_action.find('span', {'class':'ProfileTweet-action--retweet'}).find('span', {'class':'ProfileTweet-actionCount'})['data-tweet-stat-count']
    favorite = tweet_action.find('span', {'class':'ProfileTweet-action--favorite'}).find('span', {'class':'ProfileTweet-actionCount'})['data-tweet-stat-count']
    return text, time, reply, retweet, favorite


def test():
    user_id = '25073877'
    print(get_information(user_id, 1,Proxies))
    name = 'realDonaldTrump'
    print(get_information(name,0,Proxies))
    status = '870234811616677889'
    print(get_status_information(name, status,Proxies))


if __name__ == '__main__':
    test()
