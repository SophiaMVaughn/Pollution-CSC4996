
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

results_file = open("myUrlList.txt", "r").readlines()

url_list = []

for line in results_file:
    url_list.append(line.strip())

unique_urls = []
url_list.sort()

for url in url_list:
    if not bin_search(unique_urls, url):
        unique_urls.append(url)

unique_urls_file = open('myUniqueUrlList.txt', 'a')

for url in unique_urls:
    unique_urls_file.write(url+"\n")

