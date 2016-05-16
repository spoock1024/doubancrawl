# -*- coding: utf-8 -*-
import queue
import random

import requests
import time
from bs4 import BeautifulSoup

from activity import Activity
from db import DBHelper
from gevent import monkey;monkey.patch_all()
import gevent
__author__ = 'Aaron'

def random_header():
    headers = [
        {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0'}]
    index = random.randint(0,2)
    return headers[index]
activities = []
class Douban():
    def __init__(self,url):
        all_event_urls = self.get_all_urls_by_date(url)
        print("url提取完毕")
        self.get_events_info(all_event_urls)

    def get_all_urls_by_date(self, url):
        total_page = self.get_total_page(url)
        page_urls = self.get_date_urls(url,total_page)
        all_event_urls = []
        for url in page_urls:
            all_event_urls.extend(self.get_events_url(url))
        urls = "\r\n".join(all_event_urls)
        f = open("urls.txt","w")
        f.write(urls)
        f.close()
        return all_event_urls


    def get_total_page(self,url):
        response = requests.get(url,headers=random_header())
        html  =response.text
        htmlsoup = BeautifulSoup(html,"html5lib")
        total_page = 0
        last_page = htmlsoup.find("span",class_="next")
        if last_page:
            total_page_element = last_page.find_previous_sibling("a")
            total_page = total_page_element.text
            return int(total_page)
        else:
            return 0



    # get all page urls
    def get_date_urls(self,url,total):
        urls = []
        if total == 0:
            urls.append(url)
        else:
            urls = [url+"?start="+str(i*10) for i in range(total)]
        return urls
    # get evetn url by page url
    def get_events_url(self,pageurl):
        response = requests.get(pageurl,headers=random_header())
        html = response.text
        htmlsoup = BeautifulSoup(html,"html5lib")
        event_tags = htmlsoup.find_all("a",itemprop='url')
        event_urls = [event_tag["href"] for event_tag in event_tags]
        time.sleep(5)
        return event_urls

    # get the event info by event url
    def get_events_info(self,event_urls):
        num = len(event_urls)//5
        for i in range(num):
            gevent.joinall([
                gevent.spawn(self.get_event_info(event_urls.pop() if event_urls else None)),
                gevent.spawn(self.get_event_info(event_urls.pop() if event_urls else None)),
                gevent.spawn(self.get_event_info(event_urls.pop() if event_urls else None)),
                gevent.spawn(self.get_event_info(event_urls.pop() if event_urls else None)),
                gevent.spawn(self.get_event_info(event_urls.pop() if event_urls else None)),
            ])

    # parse the html,get the activity info
    def get_event_info(self,event_url):
        if event_url:
            time.sleep(random.randint(0,5))
            response = requests.get(event_url,headers=random_header())
            status_code = response.status_code
            if status_code == 200:
                event_html = response.text
                eventsoup = BeautifulSoup(event_html,"html5lib")
                eventid = 0
                try:
                    eventid = int(event_url[event_url[:-1].rfind("/")+1:-1])
                except:
                    print(event_url)
                try:
                    activity = Activity(eventsoup, eventid)
                except Exception as e:
                    f = open('error_url.txt', 'a')
                    f.write(event_url + "\r\n")
                    f.close()
                dbhelper = DBHelper()
                dbhelper.store_data(activity)
                print(event_url,"数据插入完毕")
            else:
                f = open('error_url.txt','a')
                f.write(event_url+"\r\n")
                f.close()




def auto_complete_zero(half_baked_time):
    complete_time = ""
    if half_baked_time <10:
        complete_time = "0"+str(half_baked_time)
    else:
        complete_time = str(half_baked_time)
    return complete_time


def generate_events_url_by_time():
    urls = []
    url_template = "https://www.douban.com/location/wuhan/events/{year}{month}{day}-all"
    for year in range(2008,2009):
        for month in range(1,13):
            for day in range(1,32):
                url = url_template.format(year=year,month=auto_complete_zero(month),day=auto_complete_zero(day))
                if query_activity(url):
                    urls.append(url)
    return urls

def query_activity(url):
    time.sleep(random.randint(0,3))
    response = requests.get(url,headers=random_header())
    html = response.text
    htmlsoup = BeautifulSoup(html,"html5lib")
    activity_events = htmlsoup.find_all("span",itemprop="summary")
    if len(activity_events)==0:
        return False
    else:
        return True


if __name__ == "__main__":
    start = time.clock()
    urls = generate_events_url_by_time()
    f = open("urls.txt","w")
    url_str = "\n".join(urls)
    f.write(url_str)
    f.close()
    for url in urls:
        print(url)
        douban = Douban(url)
    end_time = time.clock()
    print("TIme used:",str(end_time-start))
    print("Done")
