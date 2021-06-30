import requests
from bs4 import BeautifulSoup

the_hindu_base_url = "https://www.thehindu.com/"
the_hindu_rss_feeds_url = "https://www.thehindu.com/rssfeeds/"

def collect_feeds():
    feeds = []
    rss_json = {}
    response = requests.get(url=the_hindu_rss_feeds_url)
    soup = BeautifulSoup(response.text, features="lxml")
    sublevel2 = soup.body.find('ul', attrs={'class':'sublevel2'})

    for child in sublevel2.findAll("li"):
        url = child.a.get('href')
        feed_pos = url.split(the_hindu_base_url)[1].split("/feeder/default.rss")[0]
        if not feed_pos.startswith("news"):
            feed_pos = "news/" + feed_pos
        if "national" in feed_pos and not feed_pos.endswith("national"):
            feed_pos = feed_pos.replace("national", "states")
        feeds.append([feed_pos.lower(), url])
    
    for entry in feeds:
        feed, addr = entry[0], entry[1]
        temp = rss_json
        for i in feed.split("/"):
            i = i.replace("-", "_")
            if i in temp.keys():
                pass
            else:
                temp[i] = {"url":addr}
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

def get_data(key):
    data = None
    data = get_all_keys()
    data = data[key]
    if len(data) == 1:
        data = fetch_items(url=data[0])
    return data

def get_all_keys():
    json_response = collect_feeds()
    dictionary = {}
    iterate_json(json_response, dictionary)
    return dictionary

def iterate_json(data, dictionary):
    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, dict):
                elem = list(v.keys())
                elem.remove('url')
                if len(elem) == 0:
                    elem.append(v["url"])
                dictionary[k] = elem
                iterate_json(data[k], dictionary)
    else:
        return data
