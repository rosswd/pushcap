#!/usr/bin/env python
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
from dotenv import find_dotenv

# load ENVIRONMENT VARIABLES from .env
load_dotenv(find_dotenv())
username = os.environ.get("B593_USER")
password = os.environ.get("B593_PASS")
ip_address = os.environ.get("B593_IP_ADDRESS")
pushover_token = os.environ.get("PUSHOVER_TOKEN")
pushover_user = os.environ.get("PUSHOVER_USER")
pushover_title = os.environ.get("PUSHOVER_TITLE")
url = "http://" + ip_address + "/"

# create instance using chromedriver
driver = webdriver.Chrome("/usr/local/bin/chromedriver")

# send get request to your local router using chromedriver
driver.get(url)

# log in to local router
user = driver.find_element_by_id("txt_Username")
user.clear()
user.send_keys(username)
passwd = driver.find_element_by_id("txt_Password")
passwd.clear()
passwd.send_keys(password)
passwd.send_keys(Keys.RETURN)
driver.implicitly_wait(3)

# retrieve 'data usage' string from DOM
usage = driver.find_element_by_id("idAllVolume").text

# format message which will be sent to pushover.net
usage_string = "You have now used %s of your monthly Data" % (usage)

# quit the chromedriver instance
driver.quit()

# data to send to pushover.net
payload = {
  "token": pushover_token,
  "user": pushover_user,
  "message": usage_string,
  "title": pushover_title
}

# send POST request to pushover.net
r = requests.post('https://api.pushover.net:443/1/messages.json', data=payload)

# check if request was received by pushover.net
if (r.status_code == 200):
    print(usage_string)
else:
    print("request to pushover.net was NOT successful")

