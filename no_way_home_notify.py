from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from twilio.rest import Client
from fake_useragent import UserAgent
from time import sleep
import time
import logging
import random

logging.basicConfig(level=logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s')

# Start options
chrome_options = Options()              
chrome_options.add_argument("--headless")
# End options

PATH = "C:\Program Files (x86)\chromedriver.exe"
s=Service(PATH) 

# Remove options argument to actually see the webpage:
# , options=chrome_options
browser = webdriver.Chrome(service=s)
url='https://www.fandango.com/spider-man-no-way-home-2021-225415/movie-overview?date=2021-12-16'
xpath = r"//div[@id='viewing-toggle-wrapper']//div//div[1]//div[2]//div[1]//ol[1]//li[1]//span[1]"

account_sid = "AC6eb628c2d75172c8c03743c834d85e7e"
auth_token = "951d03c37a67f16bb417551afba494b3"
client = Client(account_sid, auth_token)

logging.info('Program started')
logging.info('Getting page...')

is_on_sale = False

while is_on_sale == False:
    browser.get(url)
    logging.info('Page opened')
    try:
        browser.find_element(By.XPATH, xpath)
        logging.info("Tickets still not on sale :(")
        logging.info("Checking again in about 60 seconds...")
        time.sleep(60)
        logging.info("Getting page again...")
    except:
        logging.info('Tickets on sale')
        is_on_sale = True
        message = client.messages.create(  
                              messaging_service_sid='MG5ef41aa4d217ff5e134aad3cecce95a2', 
                              body='https://www.fandango.com/spider-man-no-way-home-2021-225415/movie-overview',      
                              to='+19083926951' 
                          )
        call = client.calls.create(
                        twiml='<Response><Say>Hi, Akindu. No Way Home tickets are out!</Say></Response>',
                        to='+19083926951',
                        from_='+14158892932'
                    )
        print(message.sid)
        print(call.sid)
        browser.quit()
        break
