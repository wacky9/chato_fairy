#Scrape the money illusion website
import bs4
import requests


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

