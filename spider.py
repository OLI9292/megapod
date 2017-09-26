import sys
import os
import threading
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common import action_chains, keys
import selenium.webdriver.support.ui as ui
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import glob
import shutil
import time
import errno

# READ URLS FROM CSV

csv_url = 'search_results/' + sys.argv[1]
download_url = 'backlinks/' + sys.argv[1].split('.csv')[0]

if os.path.isfile(csv_url) == False:
  sys.exit(csv_url + ' not found')

campaign = pd.read_csv(csv_url, header=0, low_memory=False).fillna('')
urls = list(campaign['url'])

if len(urls) == 0:
  sys.exit('no urls found in ' + csv_url)

try:
  os.makedirs(download_url)
except OSError as e:
  if e.errno != errno.EEXIST:
    raise


# DONT INCLUDE PREVIOUSLY CRAWLED

ALL = pd.read_csv('search_results/ALL.csv', header=0, low_memory=False).fillna('')
ALL_URLS = list(ALL['url'])

urls = [x for x in urls if x not in ALL_URLS]

for u in urls:
  ALL = ALL.append({ 'url': u }, ignore_index=True)

ALL.to_csv('search_results/ALL.csv', index=False)


# SPIDER

def find_backlinks_for_(url):
  driver.get('https://ahrefs.com/site-explorer')
  wait.until(lambda driver: driver.find_element_by_id('se_index_target').is_displayed())
  driver.find_element_by_id('se_index_target').send_keys(url)
  driver.find_element_by_id('se_index_start_analysing').click()

  WebDriverWait(driver, 60).until(
    lambda driver: driver.find_element_by_xpath('//h5[@id="numberOfRefPages"]//a').is_displayed() or 
    driver.find_element_by_xpath('//div[@id="TopBacklinksStatsContainer"]//h5//div[@class="no-data-chart"]'))

  if check_exists_by_xpath('//div[@id="TopBacklinksStatsContainer"]//h5//div[@class="no-data-chart"]'):
    print('no data chart')
    run_urls()
    return

  wait.until(lambda driver: driver.find_element_by_xpath('//h5[@id="numberOfRefPages"]//a').is_displayed())
  backlinks_count = driver.find_element_by_xpath('//h5[@id="numberOfRefPages"]//a').text
  
  if has_links(backlinks_count):
    download_backlinks(url)
  else:
    run_urls()


def download_backlinks(url):
    driver.find_element_by_xpath('//h5[@id="numberOfRefPages"]//a').click()
    wait.until(lambda driver: driver.find_element_by_id('export_button').is_displayed())
    driver.find_element_by_id('export_button').click()
    wait.until(lambda driver: driver.find_element_by_id('start_full_export').is_displayed())

    if driver.find_element_by_id('start_full_export').is_enabled() == False:
      add_to_text_file_(url)
      driver.execute_script('window.history.go(-2)')
      time.sleep(1)
      run_urls()
      return

    driver.find_element_by_id('start_full_export').click()
    wait.until(lambda driver: driver.find_element_by_id('start_export_button').is_displayed())
    driver.find_element_by_id('start_export_button').click()
    run_urls()  


# SETUP

driver = None
wait = None

def setup_driver():
    global driver
    global wait
    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.folderList', 2)
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv/xls')
    profile.set_preference('browser.download.dir', os.path.join(os.getcwd(), download_url))
    driver = webdriver.Firefox(profile)
    wait = ui.WebDriverWait(driver, 200)
    driver.set_window_size(2100, 1000)

def login():
    driver.get('http://www.ahrefs.com')
    driver.find_element_by_link_text('Sign in').click()
    driver.find_element_by_id('emailLogin').click()
    action = action_chains.ActionChains(driver)
    action.send_keys('oliverplunkett2015@u.northwestern.edu')
    action.perform()
    action.send_keys(keys.Keys.ENTER)
    action2 = action_chains.ActionChains(driver)
    action2.send_keys(keys.Keys.TAB)
    action2.perform()
    action2.send_keys(keys.Keys.ENTER)
    action3 = action_chains.ActionChains(driver)
    action3.send_keys('buWUomD98zFUNj')
    action3.perform()
    action3.send_keys(keys.Keys.ENTER).send_keys(Keys.ENTER)
    elem2 = driver.find_element_by_name('password')
    elem2.send_keys(Keys.ENTER)
    time.sleep(3)

# HELPERS

def add_to_text_file_(url):
  with open('needs_manual_dwnld.txt', 'a') as myfile:
    myfile.write(url+"\n")   

def check_exists_by_xpath(xpath):
  try:
    driver.find_element_by_xpath(xpath)
  except NoSuchElementException:
    return False
  return True

def has_links(backlinks_count):
  if backlinks_count == '': 
    return False
  return ('K' in backlinks_count) or ('M' in backlinks_count) or (int(backlinks_count) > 30) 


# EXECUTION

def run_urls():
  if len(urls) > 1:
    url = urls.pop(0)
    print('Running ' + url)
    find_backlinks_for_(url)
  else:
    print("\n* * * DONE * * *\n")

def execute():
  global urls
  setup_driver()
  login()
  run_urls()

execute()
