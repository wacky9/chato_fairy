#scrape VoxEu columns
#Scrape the money illusion website
import bs4
import requests
import time
import os
#found in robots.txt
DELAY = 3
# Index for the article name in the URL
ARTICLE_NAME_INDEX = -1
# gets a collection of urls from the sitemap
def urls():
    base_url = 'https://cepr.org/sitemap.xml?page='
    sitemap_urls = [base_url + str(i) for i in range(1, 51)]
    urls = []
    for sitemap_url in sitemap_urls:
        response  = requests.get(sitemap_url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = bs4.BeautifulSoup(response.content, 'xml')
        urls.extend([url.text for url in soup.find_all('loc')])
    return urls

def get_urls():
    file = open("my_dataset/utility/voxeu.txt", "w", buffering=1)
    for u in urls():
        #filter out non-column urls
        if u.startswith("https://cepr.org/voxeu/columns/"):
            file.write(u)
            file.write("\n")
    file.close()

def download_html():
    file = open("my_dataset/utility/voxeu.txt", "r")
    urls = file.readlines()
    file.close()
    for u in urls:
        u = u.strip()
        #filter out already downloaded articles
        if os.path.isfile("my_dataset/html/VOXEU/" + u.split("/")[ARTICLE_NAME_INDEX] + ".html"):
            continue
        try:
            page = requests.get(u, headers={'User-Agent': 'Mozilla/5.0'})
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {u}: {e}")
            break
        html_data = page.text
        file = open("my_dataset/html/VOXEU/" + u.split("/")[ARTICLE_NAME_INDEX] + ".html", "w", buffering=1)
        file.write(html_data)
        file.close()
        # Delay crawling
        time.sleep(DELAY)



def process_html():
    file = open("my_dataset/utility/voxeu.txt", "r")
    urls = file.readlines()
    file.close()
    for u in urls:
        u = u.strip()
        file = open("my_dataset/html/VOXEU/" + u.split("/")[ARTICLE_NAME_INDEX] + ".html", "r")
        html_data = file.read()
        file.close()
        #Parse the html
        soup = bs4.BeautifulSoup(html_data, 'html.parser')
        file = open("my_dataset/data/" + u.split("/")[ARTICLE_NAME_INDEX] + ".txt", "w", buffering=1)
        core = soup.find("div", class_="c-text-block__inner o-content-from-editor")
        if core is None:
            print(f"Skipping {u} due to missing content.")
            continue
        paragraph_list = core.find_all("p")
        for paragraph in paragraph_list:
            # Saves only basic <p> tags
            if len(paragraph.attrs) == 0:
                file.write(paragraph.get_text())
                file.write("\n")
        file.close()


download_html()