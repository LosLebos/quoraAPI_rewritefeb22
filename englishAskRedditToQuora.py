#written for python 3.8.10. not the windows store version

from cgitb import text
from selenium import webdriver
import json
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
import logging
from Reddit import reddit #this my own file
import datetime
import time

def navigateToPartners(driver):
    driver.get("https://www.quora.com/partners")


def quoraLogin(driver):
    driver.get("https://www.quora.com/partners")
    driver.set_window_size(1054, 808)
    #get the both input elements
    inputs = driver.find_elements_by_tag_name("input")
    inputs[0].send_keys("beneheeg@googlemail.com")
    inputs[1].send_keys("Tv13zs!tv13zs")
    time.sleep(1) # i have to 
    inputs[1].send_keys(Keys.ENTER)


def askTheQuestions(driver, strQuestion):
    wait = WebDriverWait(driver, 10)
    #this starts on the partner page:
    wait.until(ec.element_to_be_clickable((By.CLASS_NAME, "AskQuestionButton"))) #wait for one of the buttons, but the first one is often not in view
    time.sleep(1)
    driver.find_elements_by_class_name("AskQuestionButton")[1].click()
    
    wait.until(ec.presence_of_element_located((By.TAG_NAME, "textarea")))
    driver.find_element_by_tag_name("textarea").send_keys(strQuestion)
    submitButtons = driver.find_elements_by_tag_name("button")
    submitButtons[3].click()
    
    time.sleep(1) #this might be avoidable
    if "Was your question already asked?" in driver.page_source:
        logging.info ("already asked")
        status = 0
    elif "Double-check your question" in driver.page_source:
        #resumeButton = driver.find_element_by_xpath("//*[text() = 'Ask original question']")
        resumeButton = driver.find_element_by_xpath("//*[text() = 'Use suggestion']")
        resumeButton.click()
        logging.info("need to doublecheck")
        status = 2
    elif "Edit topics" in driver.page_source:
        logging.info("edit topics")
        status = 1
    else:
        logging.info("unknown box")
        status = 3
    
    if status == 2:
        time.sleep(1)
        if "Was your question already asked?" in driver.page_source:
            status = 4
    return status

    #after this already start over, the rest is not that important

def getRedditQuestions():
    objReddit = reddit()
    objReddit.getRedditAPI()
    currentTime = datetime.datetime.now()
    myTimedelta = datetime.timedelta(hours=24)
    questionLimit = 200
    timeLimit = currentTime-myTimedelta
    redditQuestions = objReddit.writeSubredditData('askReddit', questionLimit, timeLimit.timestamp() )
    return redditQuestions

#main flow
options = Options()
options.add_argument("--lang=en-US") #this does nothing
#ptions.add_argument('headless')
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.implicitly_wait(10)
quoraLogin(driver)
redditQuestions = getRedditQuestions()
alreadyAsked = 0
successes = 0
double_checks = 0
unknowns = 0
double_checks_then_alreadyAsked = 0
for question in redditQuestions:
    navigateToPartners(driver)
    status = askTheQuestions(driver, question)
    if status == 0:
        alreadyAsked += 1
    elif status == 1:
        successes += 1
    elif status == 2:
        double_checks += 1
    elif status == 3:
        unknowns += 1
    elif status == 4:
        double_checks_then_alreadyAsked += 1
logging.info("Nach dem durchlauf waren sortiert nach status: " + alreadyAsked + successes + double_checks + unknowns + double_checks_then_alreadyAsked)






