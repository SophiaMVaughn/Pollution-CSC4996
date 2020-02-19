from bs4 import BeautifulSoup as soup
import requests

url_list = open("myUrlList.txt", "r").readlines()
title_list = open("article-titles.txt", "r").readlines()
body_list = open("eventsBodyList.txt", "a+")

index_list = []
index = 0

for title in title_list:
    if title[0] == "1" and title[1] == " " and title[2] == "-":
        index_list.append(index)
    index = index + 1

for index in index_list:
    page = requests.get(url_list[index])
    soup_page = soup(page.content, 'html.parser')
    body = soup_page.find_all("p")

    body_list.write("\n-DOCSTART-\n")

    for line in body:
        formated_line = line.get_text().replace("\n", " ")
        body_list.write(formated_line)
