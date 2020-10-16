import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import random

class start:
    def __init__(self, username, password):
        self.main_session = requests.Session()
        self.email_address = username
        self.password = password
        self.time = datetime.now().timestamp()
        self.profile_url = 'https://www.instagram.com/accounts/edit/'
        self.headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
        'referer': "https://www.instagram.com/accounts/login/"
        }

    def login(self):
        first_login_url = 'https://www.instagram.com/accounts/login/'
        second_login_url = 'https://www.instagram.com/accounts/login/ajax/'
        r = self.main_session.get(first_login_url,headers=self.headers)
        headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
        "x-requested-with": "XMLHttpRequest",
        'referer': "https://www.instagram.com/accounts/login/",
        "x-csrftoken":self.main_session.cookies['csrftoken']
        }
        auth = {
        'username': self.email_address,
        'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{self.time}:{self.password}',
        'queryParams': {},
        'optIntoOneTap': 'false'
        }
        r = self.main_session.post(second_login_url, data=auth, headers=headers)
        return r.text

    def follow(self, url):
        r = self.main_session.get(url)
        user_id = re.findall(r"\"owner\":{\"id\":\"(.*?)\"",r.text)[0]
        follow_url = f'https://www.instagram.com/web/friendships/{user_id}/follow/'
        headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
        'X-CSRFToken': self.main_session.cookies['csrftoken']
        }
        r = self.main_session.post(follow_url,headers=headers)
        return r.text

    def follow_all(self, url):
        self.get_suggested_list(url)
        for i in self.username_urls_list:
            print('Grabing: ' + i)
            r = self.main_session.get(i)
            time.sleep(random.randrange(5,20))
            user_id = re.findall(r"\"owner\":{\"id\":\"(.*?)\"",r.text)[0]
            follow_url = f'https://www.instagram.com/web/friendships/{user_id}/follow/'
            headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
            'X-CSRFToken': self.main_session.cookies['csrftoken']
            }
            self.main_session.post(follow_url,headers=headers)

    def like_images(self, url):
        headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
        'X-CSRFToken': self.main_session.cookies['csrftoken']
        }
        r = self.main_session.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        image_id = []
        for i in soup.find_all('script'):
            if '__typename' in str(i) and 'GraphImage' in str(i):
                image_id = re.findall(r"\"GraphImage\",\"id\":\"(.*?)\"",r.text)
                print('Total Images: ' + str(len(image_id)))
        if len(image_id) > 5:
            count = random.randrange(4, len(image_id))
            print(f'Choosing {count}.')
            for i in range(0, count):
                time.sleep(random.randrange(1,3))
                self.main_session.post(f'https://www.instagram.com/web/likes/{image_id[i]}/like/',headers=headers)
        else:
            for i in image_id:
                time.sleep(random.randrange(1,3))
                self.main_session.post(f'https://www.instagram.com/web/likes/{i}/like/',headers=headers)

    def follow_and_like(self, url):
        self.get_suggested_list(url)
        for i in self.username_urls_list:
            print('Grabing: ' + i)
            r = self.main_session.get(i)
            time.sleep(random.randrange(5,20))
            user_id = re.findall(r"\"owner\":{\"id\":\"(.*?)\"",r.text)[0]
            follow_url = f'https://www.instagram.com/web/friendships/{user_id}/follow/'
            headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
            'X-CSRFToken': self.main_session.cookies['csrftoken']
            }
            self.main_session.post(follow_url,headers=headers)
            self.like_images(i)

    def get_suggested_list(self, url):
        r = self.main_session.get(url)
        user_id = re.findall(r"\"owner\":{\"id\":\"(.*?)\"",r.text)[0]
        soup = BeautifulSoup(r.text, 'lxml')
        for i in soup.find_all('script'):
            if 'Consumer.js' in str(i):
                bounce_url = i.get('src')
        r = self.main_session.get('https://www.instagram.com' + bounce_url)
        for i in r.text.split('__d'):
            if 'include_suggested_users' in i:
                suggested_links_function = i
        graphql_variable = re.findall(r"s=\"(.*?)\"",suggested_links_function)[0]
        suggest_links_url = 'https://www.instagram.com/graphql/query/?query_hash=' + graphql_variable + '&variables={"user_id":"' + user_id + '","include_chaining":true,"include_reel":true,"include_suggested_users":false,"include_logged_out_extras":false,"include_highlight_reels":true,"include_live_status":true}'
        r = self.main_session.get(suggest_links_url)
        suggest_json = r.json()
        self.username_urls_list = []
        for i in suggest_json['data']['user']['edge_chaining']['edges']:
            self.username_urls_list.append('https://www.instagram.com/' + i['node']['username'] + '/')
