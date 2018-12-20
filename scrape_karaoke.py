import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
import selenium
from selenium import  webdriver
import csv


def get_user_data(user):
    tables = []
    num = 0
    # table= pd.read_html("https://clubdam.info/user/" + user)

    # print(table[0])

    url = "https://clubdam.info/user/" + user
    browser = webdriver.Chrome(
        executable_path="C:/Users/match/Miniconda3/Lib/site-packages/selenium/webdriver/chrome/chromedriver.exe")
    browser.implicitly_wait(6)

    browser.get(url)

    html = browser.page_source.encode("utf-8")

    soup = BeautifulSoup(html,"html.parser")

    browser.close()

    df = pd.read_html(html)
    print(df)
    """
    data = browser.find_elements_by_css_selector("tr")
    
    for tds in range(len(data)):
        if num == 18:
            print("reset")
            num = 0
        print(i.text)
        print("|")
        num += 1
    """

def main():
    users = []
    user = ""
    while user != "end":
        user = input("username?")
        users.append(user)
    for u in users:
        get_user_data(u)


if __name__ == "__main__":
    main()


