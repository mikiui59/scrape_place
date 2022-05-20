import selenium
from selenium import webdriver
import pathlib
import time
import argparse
import pandas as pd
import random
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager as CM
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as ExpectedConditions
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

def css_and_click(code, fail_message = "Css not found"):
    while True:
        try:
            x = wait.until(ExpectedConditions.presence_of_element_located((By.CSS_SELECTOR, code)))
            x.click()
            break
        except:
            print(fail_message + ": " + code + "\nretrying...")
            time.sleep(1)

def main(query):
    options=webdriver.ChromeOptions()
    options.add_argument('–lang=en-us')
    driver = webdriver.Chrome(options=options,executable_path='/home/mike/.wdm/drivers/chromedriver/linux64/97.0.4692.71/chromedriver')#CM().install())
    wait = WebDriverWait(driver, 60)

    q0=query
    q=q0.replace(' ','+')
    driver.get(f'https://google.com/search?q={q}')
    time.sleep(2)
    q=driver.find_element_by_class_name('tiS4rf.Q2MMlc').get_attribute('href')
    time.sleep(2)
    driver.get(q)
    time.sleep(3)
    driver.find_elements_by_class_name('VfPpkd-vQzf8d')[3].click()
    time.sleep(5)

    driver.get('https://www.google.com/preferences#languages')
    time.sleep(5)
    driver.find_elements_by_css_selector('div#langten')[0].click()
    time.sleep(5)
    driver.find_element_by_css_selector('div.goog-inline-block.jfk-button.jfk-button-action').click()
    time.sleep(2)

    obj = driver.switch_to.alert
    time.sleep(2)
    obj.accept()
    time.sleep(2)

    columns=['Name','Rate','Review Count','Adress','Phone']
    df=[]

    q=q0.replace(' ','+')
    driver.get(f'https://google.com/search?q={q}')
    time.sleep(2)
    q=driver.find_element_by_class_name('tiS4rf.Q2MMlc').get_attribute('href')
    time.sleep(2)
    driver.get(q)
    time.sleep(3)

    end=len(driver.find_elements_by_css_selector('td'))-2

    for i in range(0,end-1):
        l=driver.find_elements_by_css_selector('div.cXedhc.uQ4NLd')

        for i in range(0,len(l)):
            l0=l[i].text.split('\n')
            if len(l0)>=4 and not 'No review' in l[i].text:
                rate=float(l0[1])
                rc=l0[2].split(')')[0].split('(')[-1]
                if 'K' in rc:
                    rc=float(rc[:-1])*1e3
                elif 'M' in rc:
                    rc=float(rc[:-1])*1e6

                try:
                    if '+' in l0[4]:
                        phone=l0[4].split('·')[-1].replace(' ','')
                    else:
                        phone=None
                    if not '+' in l0[3]:
                        df.append([l0[0],rate,int(rc),l0[3],phone])
                except:
                    pass
            else:
                pass

        driver.find_element_by_css_selector('a#pnnext').click()
        time.sleep(8)
    driver.quit()

    df=pd.DataFrame(df,columns=columns)
    df.to_csv('place.csv')
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-q","--query",
                        help='search query example(Giftshops in USA)',
                        required=True)
    args = parser.parse_args()
    main(str(args.query))