# -*- coding: utf-8 -*-
import random
import re

import requests
from bs4 import BeautifulSoup

__author__ = 'Aaron'

def random_header():
    headers = [
        {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0'}]
    index = random.randint(0,2)
    return headers[index]

class Organization():

    def __init__(self,url):
        self.url = url
        self.type = self.get_type(url)
        self.organizationid = self.get_organizationid(url)
        response = requests.get(url,headers=random_header())
        html = response.text
        htmlsoup = BeautifulSoup(html,"html5lib")
        self.followers = 0
        self.attendnum = 0
        self.wishnum = 0
        self.ownednum = 0
        self.groupsnum = 0
        self.groupsnames = ""
        if self.type == "site":
            self.ownednum = self.get_site_owned(htmlsoup)
            self.followers = self.get_follower(htmlsoup)

        else:
            self.attendnum,self.wishnum,self.ownednum = self.get_people_info(htmlsoup)
            self.groupsnum, self.groupsnames = self.get_people_group(htmlsoup)

        # print("type:"+self.type)
        # print("ownednum:"+str(self.ownednum))
        # print("followers:"+str(self.followers))
        # print("attendnum:"+str(self.attendnum))
        # print("wishnum:"+str(self.wishnum))
        # print("groupsnum:"+str(self.groupsnum))
        # print("groupsnames:"+str(self.groupsnames))

    # get the organization_type bu url,maybe site or person
    def get_type(self,url):
        if url.find("site") !=-1:
            return "site"
        else:
            return "people"

    def get_organizationid(self,url):
        match = re.search("\d+",url)
        if match:
            return int(match.group())
        else:
            return 0

    def get_site_owned(self,htmlsoup):
        # get the url  which can get all the events
        events = htmlsoup.find(href=re.compile("widget/events"))
        events_url = ""
        if events:
            events_url = events["href"]
            response = requests.get(events_url,headers=random_header())
            html = response.text
            eventsoup = BeautifulSoup(html,"html5lib")
            site_owned_element = eventsoup.find("span",class_="count")
            owned = 0
            if site_owned_element:
                element_str = site_owned_element.text
                owned = int(element_str[2:-2])
            return owned
        else:
            return 0

    def get_follower(self,htmlsoup):
        followers = htmlsoup.find(href=re.compile("followers"))
        nums = 0
        if followers:
            nums = int(followers.text)
        return nums

    def get_people_info(self,htmlsoup):
        attendnum = self.__get_infonum(htmlsoup,"attend")
        wishnum = self.__get_infonum(htmlsoup,"wish")
        ownednum = self.__get_infonum(htmlsoup,"owned")
        return attendnum,wishnum,ownednum

    def __get_infonum(self,htmlsoup,type):
        url_pattern = ""
        if type == "attend":
            url_pattern = "^events/attend"
        elif type == "wish":
            url_pattern = "^events/wish"
        elif type == "owned":
            url_pattern = "^events/owned"
        attend_urls = htmlsoup.find_all(href=re.compile(url_pattern))
        sum = 0
        for url_element in attend_urls:
            text = url_element.text
            sum += int(text[3:])
        return sum
    def get_people_group(self,htmlsoup):
        groupsnum = self.__get_group_num(htmlsoup)
        groupsnames = self.__get_group_names(htmlsoup)
        return groupsnum,groupsnames

    def __get_group_num(self,htmlsoup):
        group_element = htmlsoup.find(href="groups")
        group_num = 0
        if group_element:
            group_str = group_element.text
            group_num = int(group_str[2:])
        return group_num

    def __get_group_names(self,htmlsoup):
        names = []
        name_elements =  htmlsoup.find_all("a",class_="name")
        for element in name_elements:
            names.append(element.text)
        return ",".join(names)

class Activity_involved_person(object):
    def __init__(self,participate_url,wisher_url):
        self.parse_participate(participate_url)
        self.parse_wisher(wisher_url)

    def parse_participate(self,participate_url):
        response = requests.get(participate_url,headers=random_header())
        html = response.text
        htmlsoup = BeautifulSoup(html,"html5lib")
        title_soup = htmlsoup.find("h3")
        self.participate_total = self.get_total_members(title_soup)
        self.participate_cities = self.get_rate(htmlsoup)

    def parse_wisher(self,wisher_url):
        response = requests.get(wisher_url,headers=random_header())
        html = response.text
        htmlsoup = BeautifulSoup(html,"html5lib")
        title_soup = htmlsoup.find("h3")
        self.wisher_total = self.get_total_members(title_soup)
        self.wisher_cities = self.get_rate(htmlsoup)

    def get_total_members(self,title_soup):
        title = title_soup.text
        match = re.search("\d+",title)
        total = 0
        if match:
            total = int(match.group())
        return total

    def get_rate(self,participate_html_soup):
        cities = {}
        cities_elements= participate_html_soup.find_all("span",class_="pl")
        for city_element in cities_elements:
            city = city_element.text[1:-1]
            if city in cities:
                cities[city] += 1
            else:
                cities[city] = 1
        return cities

class Activity():
    def __init__(self, html_soup, event_id):
        self.html_soup = html_soup
        self.event_id = event_id
        self.title = Activity.remove_blank(self.get_title())
        self.time = Activity.remove_blank(self.get_time())
        self.location = Activity.remove_blank(self.get_location())
        self.cost = Activity.remove_blank(self.get_cost())
        self.type = Activity.remove_blank(self.get_type())
        self.organization_name = Activity.remove_special_char(self.get_organization_name())
        self.organization_url = Activity.remove_blank(self.get_organization_url())
        self.info = Activity.remove_blank(self.get_related_info())
        self.involved_person = self.get_involved_person()
        self.organization = self.get_organization()

    def get_title(self):
        return self.html_soup.find("h1").text

    def get_time(self):
        return  self.html_soup.find("li", class_="calendar-str-item ").text

    def get_location(self):
        return self.html_soup.find("div", itemprop='location').text

    def get_cost(self):
        return self.html_soup.find("div", itemprop="location").find_next_sibling().text

    def get_type(self):
        return self.html_soup.find("a", itemprop="eventType").text

    def get_organization_name(self):
        return self.html_soup.find("a", itemprop="name").text

    def get_organization_url(self):
        return self.html_soup.find("a", itemprop="name")["href"]

    def get_organization(self):
        return Organization(self.organization_url)

    def get_related_info(self):
        return self.html_soup.find_all("div", class_="wr")[-1].text

    def get_involved_person(self):
        participate_url =  self.html_soup.find(href=re.compile("participant"))["href"]
        wisher_url  =self.html_soup.find(href=re.compile("wisher"))["href"]
        return  Activity_involved_person(participate_url,wisher_url)


    @staticmethod
    def remove_blank(text):
        return text.strip().replace("\n","").replace(" ","").replace(u"\xa0","")

    @staticmethod
    def remove_special_char(text):
        text = text.strip().replace("\n", "").replace(" ", "").replace(u"\xa0", "")
        cleanString = re.sub('\W+', '', text)
        return cleanString


