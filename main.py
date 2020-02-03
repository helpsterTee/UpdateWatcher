from database import Database
from bs4 import BeautifulSoup
import yaml
import requests
import time, datetime

# debug
#from pprint import pprint

class UpdateWatcher:
    db = False
    config = False

    def __init__(self):
        self.db = Database()

    # send a notification message
    def notify(self, name, description):
        if self.config['notification_service']['type'] == "gotify":
            url = self.config['notification_service']['url']
            payload = {'title': "Update for ["+name+"]", 'message': description}

            response = requests.post(url, data=payload)

            if response.status_code != 200:
                print("! Error pushing message: "+response.reason)

    # main run loop
    def loop(self):
        # print execution time
        print(str(datetime.datetime.now()))

        # check sites against DB
        for site in self.config['sites']:
            # get entry, this can be either the content or False
            siteres = self.db.getEntryContent(site['name'], site['url'])

            # get the current version of the app site
            r = requests.get(site['url'])
            soup = BeautifulSoup(r.content, 'html.parser')

            print("Parsing app: "+site['name']+" at "+site['url']+". Getting content...")

            # select the content
            content = False
            if 'selector' in site.keys():
                content = soup.select_one(site['selector'])

            if content is False:
                print("-- Error selecting CSS")
            else:
                # this is a new application to watch
                if siteres == False:
                    print("-- this is a new app!")

                    # insert into db
                    insid = self.db.insertEntry("insert", site['name'], site['url'], content.get_text())
                    print("-- created new entry with id "+str(insid))

                    # call notification service
                    print("-- calling notification service to make sure you'll get updates!")
                    notify_text = 'Update available'
                    if 'notification_selector' in site.keys():
                        notify_text = soup.select_one(site['notification_selector']).get_text()
                    self.notify(site['name'], notify_text)
                # we already know this app
                else:
                    # the existing content is the same as online
                    if content.get_text() == siteres:
                        print("-- no new version available, skipping")
                    # the content differs. we assume this is a new version
                    else:
                        insid = self.db.insertEntry("update", site['name'], site['url'], content.get_text())
                        print("-- update available for id "+str(insid))

                        notify_text = 'Update available'
                        if 'notification_selector' in site.keys():
                            notify_text = soup.select_one(site['notification_selector']).get_text()
                        self.notify(site['name'], notify_text)
        print()

    def run(self):
        # init the db
        self.db.initDB()

        # load the config
        with open('config.yml', 'r') as stream:
            self.config = yaml.safe_load(stream)

        while True:
            self.loop()
            time.sleep(int(self.config["update_interval"]))

if __name__ == "__main__":
    app = UpdateWatcher()
    app.run()
