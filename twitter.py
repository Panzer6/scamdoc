import undetected_chromedriver as uc
import time
from bs4 import BeautifulSoup
from datetime import datetime
import re
from csv import writer

driver = uc.Chrome()
driver.get("https://twitter.com/search?q=%23phishing%20-(from%3AillegalFawn%20OR%20from%3AKesaGataMe0%20OR%20from%3Aozuma5119%20OR%20from%3Aromonlyht%20OR%20from%3Aecarlesi%20OR%20from%3Adubstard%20OR%20from%3ASecureReload%20OR%20from%3Apingineer_jp%20OR%20from%3AMalwarePatrol%20OR%20from%3Adnstwist%20OR%20from%3AAP_Zenmashi%20OR%20from%3ASlvlombar%20OR%20from%3AUltrascan419)%20(domain%20OR%20hxxp%20OR%20http%20OR%20.%20OR%20%2F%20OR%20.xyz%20OR%20.co%20OR%20.com%20OR%20.ch%20OR%20.fr%20OR%20%F0%9F%94%97%20OR%20%22new%20today%22%20OR%20%22new%20websites%22)%20%20until%3A2023-01-12%20since%3A2023-01-11&src=typed_query")
page_source = driver.page_source
website = BeautifulSoup(page_source, "lxml")
contents = website.find_all("div", class_="css-1dbjc4n r-j5o65s r-qklmqi r-1adg3ll r-1ny4l3l")
for content in contents:
    texts = content.find_all("span", class_="css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0")
    final_txt = ""
    for text in texts:
        final_txt += text
    print(final_txt)