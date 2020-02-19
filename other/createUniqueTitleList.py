
def bin_search(list, key) -> bool:

    min = 0
    max = len(list)-1

    while min <= max:
        mid = int((min + max) / 2)
        if key == list[mid]:
            return True
        elif key < list[mid]:
            max = mid - 1
        elif key > list[mid]:
            min = mid + 1
    return False

titles_file = open("article-titles.txt", "r").readlines()

title_list = []

for line in titles_file:
    title_list.append(line.strip())

unique_titles = []
title_list.sort()

for url in title_list:
    if not bin_search(unique_titles, url):
        unique_titles.append(url)

unique_titles_file = open('uniqueArticleTitleList.txt', 'a')

for url in unique_titles:
    unique_titles_file.write(url+"\n")

