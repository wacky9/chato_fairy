import bs4
import requests

DIR_HEAD = '/app/data/'

def pull():
    URL = "https://www.themoneyillusion.com/trade-war-children-its-just-a-tweet-away/"
    #Need user agent to avoid 403 Forbidden error
    page = requests.get(URL, headers={'User-Agent': 'Mozilla/5.0'})
    html_data = page.text
    file = open(DIR_HEAD + "test.html", "w", buffering=1)
    file.write(html_data)
    file.close()

def manipulate():
    file = open(DIR_HEAD + "test.html", "r")
    html_data = file.read()
    soup = bs4.BeautifulSoup(html_data, 'html.parser')
    file = open(DIR_HEAD + "test_file.txt", "w", buffering=1)
    paragraph_list = soup.find("div",class_="post").find_all("p")
    for paragraph in paragraph_list:
        # Saves only basic <p> tags
        if len(paragraph.attrs) == 0:
            file.write(paragraph.get_text())
            file.write("\n")
    file.close()

#pull()
manipulate()