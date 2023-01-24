# ---------------------------------------------------------------------------------------------------------------------------------------------
# Code written by: Ronald Andrew Ganotisi (TR-PH-INTRN)
# Last Update: 01/25/23 12:58 AM
# ---------------------------------------------------------------------------------------------------------------------------------------------

import undetected_chromedriver as uc
import time
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
from csv import writer
from random import randint
from selenium.webdriver.common.by import By

def nextPage():
    global page_num
    print(f"Done on page {page_num}. Moving on to next page after a delay to prevent website from blocking the scraper.")
    page_num += 1
    time.sleep(randint(10,20))
    driver.get(f"https://scamdoc.com/?page={page_num}")

def is_captcha_solvable():
    while True:
        time.sleep(5)
        iframe = driver.find_element("xpath", '//iframe')
        driver.switch_to.frame(iframe)
        ggs = driver.find_element(By.TAG_NAME, "div")
        captcha_check = ggs.text
        if "Verify you are human" in captcha_check:
            print("\nCloudflare captcha detected, reloading webpage...")
            driver.switch_to.default_content()
            driver.refresh()
        else:
            driver.switch_to.default_content()
            break

def check_for_new():
    global new
    for content in contents:
            analysis_date = content.find("span", class_="type-label")
            temp = analysis_date.text.strip()
            cmp = temp.split(" ")
            if cmp[4] == input_date:
                new = True

def go_to_yesterday(current_date):
    print("No new links found. Switching to yesterday's date...\n")
    print("Going back to previous page to collect missed URLs... \n")
    days += 1
    new_date = datetime.now() - timedelta(days)
    current_date = new_date.strftime("%m/%d/%Y")
    page_num -= 1
    time.sleep(randint(10,20))
    driver.get(f"https://scamdoc.com/?page={page_num}")
    return current_date
    
def enter_link():
    global last_link
    last_link = input("\nCopy and paste the last URL (non-https and no spaces) to stop scraping there:")
    time.sleep(1)
    if "." in last_link:
        print(f"Scraper will halt when encountering: {last_link}")
        time.sleep(1)
    else:
        print("\nNo link constraint added. Proceeding...\n")

def check_for_link():
    global end
    if cmp2[0] == last_link:
        print("Detected the last URL. Closing the scraper...")
        driver.delete_all_cookies()
        time.sleep(1)
        print(f"Reached page {page_num} and collected {num} link(s)")
        driver.close()
        end = time.time() - start
        input("Press Enter to quit.")
        quit()

def main():
    global input_date, answer, new, num, contents, current_time, current_date, cmp, cmp2, title, analysis_date, page_num, driver, placebo, start, days
    days = 0
    start = time.time()
    answer = False
    new = False
    num = 0
    input_date = ""
    page_num = 1
    current_time = datetime.now()
    current_date = current_time.strftime("%m/%d/%Y")
    enter_link()
    options = uc.ChromeOptions()
    options.add_argument("--incognito")
    driver = uc.Chrome(use_subprocess=True)
    driver.get("https://scamdoc.com")
    with open("result.csv", "w") as f:
        writer_object = writer(f)
        writer_object.writerow(["First Analysis Date", "URL", "Trust Rating"])
        f.close()
    while answer == False:
        new = False
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "lxml")
        rtable = soup.find("table", class_="table reports-table text-left")
        if rtable is None:
            is_captcha_solvable()
            print("Captcha detected! \n")
            placebo = input("Press Enter if you have solved the captcha.")
            continue
        else:
            contents = rtable.find_all("td", class_="container pdr-unset")
            check_for_new()
            if new == False:
                go_to_yesterday(current_date)
                time.sleep(1)
                continue
            else:
                for content in contents:
                        title = content.find("span", class_="last-report-title")
                        analysis_date = content.find("span", class_="type-label")
                        temp = analysis_date.text.strip()
                        cmp = temp.split(" ")
                        if cmp[4] == current_date:
                            temp2 = title.text.strip()
                            cmp2 = temp2.split(" ")
                            check_for_link()
                            if int(cmp2[-2]) <= 30:
                                output = [input_date, cmp2[0], f"{cmp2[-2]}%"]
                                output2 = [input_date, f"https://{cmp2[0]}", f"{cmp2[-2]}%"]
                                num+=1
                                print("Found " + str(num) + " links")
                                with open("result.csv", "a", newline="") as f:
                                    writer_object = writer(f)
                                    writer_object.writerow(output)
                                    writer_object.writerow(output2)
                                    f.close()
            nextPage()

if __name__ == "__main__":
    main()