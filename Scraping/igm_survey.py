#Scrape the money illusion website
import bs4
import requests
import time
import json
import re
#found in robots.txt
DELAY = 3

# gets a collection of urls from the sitemap
def urls():
    sitemap_urls = ['https://kentclarkcenter.org/survey-sitemap.xml']
    urls = []
    for sitemap_url in sitemap_urls:
        response  = requests.get(sitemap_url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'
        })
        print(response)
        soup = bs4.BeautifulSoup(response.content, 'xml')
        urls.extend([url.text for url in soup.find_all('loc')])
    return urls

def get_urls():
    file = open("my_dataset/utility/igm_survey.txt", "w", buffering=1)
    for u in urls():
        if "jpg" not in u:
            file.write(u)
            file.write("\n")
    file.close()

def download_html():
    file = open("my_dataset/utility/igm_survey.txt", "r")
    urls = file.readlines()
    file.close()
    for u in urls:
        u = u.strip()
        page = requests.get(u, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'})
        html_data = page.text
        #Each url ends in a /
        file = open("my_dataset/html/IGM/" + u.split("/")[-2] + ".html", "w", buffering=1)
        file.write(html_data)
        file.close()
        #Delay crawling
        time.sleep(DELAY)

def process_html():
    file = open("my_dataset/utility/igm_survey.txt", "r")
    urls = file.readlines()
    file.close()
    eval_file = open("my_dataset/eval_data/igm_survey.json", "w", buffering=1)
    json_array = []
    for u in urls:
        u = u.strip()
        print(u)
        file = open("my_dataset/html/IGM/" + u.split("/")[-2] + ".html", "r")
        html_data = file.read()
        file.close()
        #Parse the html
        soup = bs4.BeautifulSoup(html_data, 'html.parser')
        #grab all questions
        survey = soup.find("div", class_="poll_results_wrapper_default")
        # questions and results should always be the same length
        questions = survey.find_all("h4")
        questions = [q.get_text().strip() for q in questions]
        results = survey.find_all("script")
        survey_results = []
        # Grab data from first lines of script
        for result in results:
            unweighted = result.get_text()
            unweighted = next((line for line in unweighted.splitlines() if "pollVals" in line), None)
            unweighted_data = [int(float(match)) for match in re.findall(r",\s*([0-9.]+)", unweighted)][0:5]
            weighted = result.get_text()
            weighted = next((line for line in weighted.splitlines() if "weightedPV" in line), None)
            weighted_data = [int(float(match)) for match in re.findall(r",\s*([0-9.]+)", weighted)]
            survey_results.append((unweighted_data,weighted_data))
        # Convert to JSON
        for i in range(len(questions)):
            json_array.append({
                "question": questions[i],
                "unweighted": survey_results[i][0],
                "weighted": survey_results[i][1]
            })
    eval_file.write(json.dumps(json_array, indent=4))
    eval_file.close()