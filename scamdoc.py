import requests
import time
import urllib.parse
from bs4 import BeautifulSoup
import re
from datetime import datetime

check1 = 0
check2 = 1
sa_key = '34a83c31a6124e4793b0f8a44b2aa825' # paste here
sa_api = 'https://api.scrapingant.com/v2/general'
current_time = datetime.now()
current_date = current_time.strftime("%m/%d/%Y")
num = 0

new = False

def wait():
    print("Waiting 10 seconds to avoid being blocked by the website....")
    time.sleep(10)
    

def check_for_new():
    global new
    for content in contents:
            analysis_date = content.find("span", class_="type-label")
            temp = analysis_date.text.strip()
            cmp = temp.split(" ")
            if cmp[4] == current_date:
                new = True


if __name__ == "__main__":
    open("result.txt", "w").close()
    while check1 != check2:
        newlinks=0
        qParams = {'url': f"https://scamdoc.com/?page={pagenum}", 'x-api-key': sa_key}
        reqUrl = f'{sa_api}?{urllib.parse.urlencode(qParams)}'
        r = requests.get(reqUrl)
        check1+=1
        soup = BeautifulSoup(r.content, 'html.parser')
        rtable = soup.find("table", class_="table reports-table text-left")
        contents = rtable.find_all("td", class_="container pdr-unset")
        check_for_new()
        if new == True:
            for content in contents:
                title = content.find("span", class_="last-report-title")
                analysis_date = content.find("span", class_="type-label")
                temp = analysis_date.text.strip()
                cmp = temp.split(" ")
                if cmp[4] == current_date:
                    check2 = check1 + 1
                    temp2 = title.text.strip()
                    cmp2 = temp2.split(" ")
                    if int(cmp2[-2]) <= 30:
                        num+=1
                        print("Found " + str(num))
                        with open("result.txt", "a") as f:
                            f.write(cmp2[0])
                            f.write("\n")
                            f.write("https://" + cmp2[0])
                            f.write("\n")
                            f.close()
        elif new == False:
            print("No new links detected. Total of " + str(num) +" links found. Closing...")
            exit()
        new = False
        print("Finished page " + str(pagenum))
        pagenum+=1
        wait()