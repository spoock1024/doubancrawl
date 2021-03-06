# -*- coding: utf-8 -*-
import re
import traceback

__author__ = 'Aaron'
import mysql.connector

config = {
    "user":"whu",
    "password":"123456",
    "host":"127.0.0.1",
    "database":"douban",
    "raise_on_warnings":True,
}

class DBHelper():

    def __init__(self):
        pass


    def store_data(self,activity):
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        add_activity = ("INSERT INTO activity(eventid,title,activitytime,location,cost,info,activitytype,interestedpersonnum,interestedrate,participatepersonnum,participaterate,organizationname,organizationid,organizationurl,organizationtype,attendnum,wishnum,ownednum,groupsnum,groupsnames,followersnum) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        data = self.__get_data(activity)
        try:
            cursor.execute(add_activity,data)
        except mysql.connector.errors.DatabaseError as e:
            traceback.print_exc()
            with open("storedb_error.txt","a+") as file:
                file.write(str(activity.event_id))
                file.write("\n")

        cnx.commit()
        cursor.close()
        cnx.close()

    def __get_data(self,activity):
         involved_person = activity.involved_person
         organization = activity.organization
         activity_data = (activity.event_id, activity.title, activity.time, activity.location, activity.cost, activity.info,activity.type,
                     involved_person.participate_total, str(involved_person.participate_cities), involved_person.wisher_total,
                     str(involved_person.wisher_cities), activity.organization_name, organization.organizationid, organization.url, organization.type,
                    organization.attendnum, organization.wishnum, organization.ownednum, organization.groupsnum,
                    organization.groupsnames, organization.followers
                          )
         return activity_data

if __name__ == "__main__":
    name = '💄豌豆丫丫✨🎀'
    print(len(name))
    cleanString = re.sub('\W+', '', name)
    print(len(cleanString))




