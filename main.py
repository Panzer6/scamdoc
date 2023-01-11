# ---------------------------------------------------------------------------------------------------------------------------------------------
# Code written by: Ronald Andrew Ganotisi (TR-PH-INTRN)
# Last Update: 01/10/23 5:42PM
# ---------------------------------------------------------------------------------------------------------------------------------------------

import undetected_chromedriver as uc
import time
from bs4 import BeautifulSoup
from datetime import datetime
import re
from csv import writer

answer = False
new = False
num = 0
input_date = ""

def inCaptcha():
    global bypass
    bypass = input("Enter Y if you have solved the captcha. Enter N to cancel. \n")

def nextPage():
    global nPage
    nPage = input("Done Scraping. Press enter if you have moved on to next page. \n Or input Q to quit. \n")

def check_for_new():
    global new
    for content in contents:
            analysis_date = content.find("span", class_="type-label")
            temp = analysis_date.text.strip()
            cmp = temp.split(" ")
            if cmp[4] == input_date:
                new = True

def enter_date():
    while True:
        global input_date
        input_date = input("Enter desired analysis date in the form of MM/DD/YYYY (no spaces) below: \n")
        temp1 = input_date.split("/")
        if int(temp1[2]) > 2023:
            print("Unfortunately, we don't support links in the future. \n")
            time.sleep(1)
            continue
        else:
            break

def enter_new_date():
    while True:
        prompt1 = input("No new links found. Enter a new date? (y/n)\n")
        if prompt1.lower() == "y":
            enter_date()
            break
        else:
            if prompt1.lower() == "n":
                driver.delete_all_cookies()
                time.sleep(1)
                driver.close()
                quit()
            else:
                print("Input not recognized, try again.")
                continue

def enter_link():
    global last_link
    print("\n Copy and paste the last URL (non-https and no spaces) to stop scraping there.")
    last_link = input("Or leave blank to only have a constraint on the date: ")
    time.sleep(1)
    if "." in last_link:
        print(f"Scraper will halt when encountering: {last_link}")
        time.sleep(1)
    else:
        print("No link constraint added. Proceeding...")
        time.sleep(1)

def check_for_link():
    if cmp2[0] == last_link:
        print("Detected the last URL. Closing the scraper...")
        driver.delete_all_cookies()
        time.sleep(1)
        driver.close()
        quit()
    
current_time = datetime.now()
current_date = current_time.strftime("%m/%d/%Y")
enter_date()
enter_link()
driver = uc.Chrome()
driver.get("https://scamdoc.com")
inCaptcha()
open("result.csv", "w").close()
while answer == False:
    if bypass.lower() == "y":
        new = False
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "lxml")
        rtable = soup.find("table", class_="table reports-table text-left")
        contents = rtable.find_all("td", class_="container pdr-unset")
        check_for_new()
        if new == False:
            enter_new_date()
            time.sleep(1)
            continue
        else:
            for content in contents:
                    title = content.find("span", class_="last-report-title")
                    analysis_date = content.find("span", class_="type-label")
                    temp = analysis_date.text.strip()
                    cmp = temp.split(" ")
                    if cmp[4] == input_date:
                        temp2 = title.text.strip()
                        cmp2 = temp2.split(" ")
                        check_for_link()
                        if int(cmp2[-2]) <= 30:
                            output = [cmp2[0], f"{cmp2[-2]}%"]
                            output2 = [f"https://{cmp2[0]}", f"{cmp2[-2]}%"]
                            num+=1
                            print("Found " + str(num) + " links")
                            with open("result.csv", "a", newline="") as f:
                                writer_object = writer(f)
                                writer_object.writerow(output)
                                writer_object.writerow(output2)
                                f.close()
        nextPage()
        if nPage.lower() == "q":
            print("Closing the program...")
            driver.delete_all_cookies()
            time.sleep(1)
            driver.close()
            quit()
    else:
        if bypass.lower() == "n":
            answer = True
            print("Closing...")
            exit()
        else:
            print("Input not recognized, try again.")
            inCaptcha()