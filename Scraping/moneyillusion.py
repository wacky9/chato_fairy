#Scrape the money illusion website
import bs4
import requests
import time

#found in robots.txt
DELAY = 10

# gets a collection of urls from the sitemap
def urls():
    sitemap_urls = ['https://www.themoneyillusion.com/wp-sitemap-posts-post-1.xml','https://www.themoneyillusion.com/wp-sitemap-posts-post-2.xml','https://www.themoneyillusion.com/wp-sitemap-posts-post-3.xml']
    urls = []
    for sitemap_url in sitemap_urls:
        response  = requests.get(sitemap_url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = bs4.BeautifulSoup(response.content, 'xml')
        urls.extend([url.text for url in soup.find_all('loc')])
    return urls

def get_urls():
    file = open("my_dataset/utility/moneyillusion_urls.txt", "w", buffering=1)
    for u in urls():
        file.write(u)
        file.write("\n")
    file.close()

def download_html():
    file = open("my_dataset/utility/moneyillusion_urls.txt", "r")
    urls = file.readlines()
    file.close()
    for u in urls:
        u = u.strip()
        page = requests.get(u, headers={'User-Agent': 'Mozilla/5.0'})
        html_data = page.text
        #Each url ends in a /
        file = open("my_dataset/html/MI/" + u.split("/")[-2] + ".html", "w", buffering=1)
        file.write(html_data)
        file.close()
        #Delay crawling
        time.sleep(DELAY)

def process_html():
    file = open("my_dataset/utility/moneyillusion_urls.txt", "r")
    urls = file.readlines()
    file.close()
    for u in urls:
        u = u.strip()
        file = open("my_dataset/html/MI/" + u.split("/")[-2] + ".html", "r")
        html_data = file.read()
        file.close()
        #Parse the html
        soup = bs4.BeautifulSoup(html_data, 'html.parser')
        file = open("my_dataset/data/" + u.split("/")[-2] + ".txt", "w", buffering=1)
        paragraph_list = soup.find("div",class_="post").find_all("p")
        for paragraph in paragraph_list:
            # Saves only basic <p> tags
            if len(paragraph.attrs) == 0:
                file.write(paragraph.get_text())
                file.write("\n")
        file.close()

process_html()