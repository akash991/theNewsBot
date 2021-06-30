import json
import requests
from bs4 import BeautifulSoup

the_hindu_base_url = "https://www.thehindu.com/"
the_hindu_rss_feeds_url = "https://www.thehindu.com/rssfeeds/"
json_file_path = "../data/theHindu.json"

def collect_feeds():
    feeds = []
    rss_json = {}
    response = requests.get(url=the_hindu_rss_feeds_url)
    soup = BeautifulSoup(response.text, features="html")
    sublevel2 = soup.body.find('ul', attrs={'class':'sublevel2'})

    for child in sublevel2.findAll("li"):
        url = child.a.get('href')
        feed_pos = url.split(the_hindu_base_url)[1].split("/feeder/default.rss")[0]
        if not feed_pos.startswith("news"):
            feed_pos = "news/" + feed_pos
        if "national" in feed_pos and not feed_pos.endswith("national"):
            feed_pos = feed_pos.replace("national", "states")
        feeds.append([feed_pos, url])
    
    for entry in feeds:
        feed, addr = entry[0], entry[1]
        temp = rss_json
        for i in feed.split("/"):
            i = i.replace("-", "_")
            if i in temp.keys():
                pass
            else:
                temp[i] = {"url":addr, "article":[]}
            temp = temp[i]
    return rss_json

def fetch_items(url):
    data = []
    soup = BeautifulSoup(markup=requests.get(url).text, features="xml")
    for i in soup.find_all("item"):
        temp = {}
        temp["title"] = i.title.text
        temp["link"] = i.link.text
        temp["published_on"] = i.pubDate.text
        temp["description"] = i.description.text.strip("\r\n ")
        data.append(temp)
    return data

def collect_articles(data):
    for _, v in data.items():
        if _ == "article":
            data["article"] = fetch_items(data["url"])
        if isinstance(v, dict):
             data[_] = collect_articles(v)
    return data

if __name__ == "__main__":
    feeds = collect_feeds()
    data = collect_articles(data=feeds)
    with open(json_file_path, "w") as file:
        json.dump(data, file)
