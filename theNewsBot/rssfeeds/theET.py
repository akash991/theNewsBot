import requests
from bs4 import BeautifulSoup

the_et_base_url = "https://economictimes.indiatimes.com"
the_et_rss_feed_url = "https://economictimes.indiatimes.com/rss.cms"

def collect_feeds():
    """
    """
    rss_json = {"theET": {"url":""}}
    response = requests.get(url=the_et_rss_feed_url)
    soup = BeautifulSoup(response.text, features="lxml")
    rssSubHead = soup.body.findAll('div', attrs={'class':'rssSubHead'})

    for rss in rssSubHead:
        if rss.a.text.lower() == "news":
            ul = rss.find_next_sibling('ul')
            for li in ul.findAll("li"):
                url = "{}{}".format(the_et_base_url, li.a.get("href"))
                feed = li.a.get("href").split("/")[2].replace("-", "_")
                rss_json["theET"][feed] = {"url":url}
            return rss_json

def fetch_items(url):
    """
    Fetch all the news articles using the url of a given feed
    """
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

def get_data(key):
    """
    Method to collect the data for a given key
    Key here refers to the rssfeed name
    
    Returns a list of strings, if there are suboptions
    or a list of dictionary, if it contains a url to the
    news articles.
    """
    data = None
    data = get_all_keys()
    data = data[key]
    if isinstance(data, str):
        data = fetch_items(url=data)
    return data

def get_all_keys():
    """
    Iterrate through the list of feeds and return
    all options and their suboptions (if any) as a dictionary.
    Used for creating the ConversationHandler for the bot.
    """
    json_response = collect_feeds()
    dictionary = {}
    iterate_json(json_response, dictionary)
    return dictionary

def iterate_json(data, dictionary):
    """
    Methof to travel through the json object
    recursively and return either a list of 
    suboptions or the url.
    """
    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, dict):
                if list(v.keys()) == ["url"]:
                    dictionary[k] = v["url"]
                else:
                    temp = list(v.keys())
                    temp.remove('url')
                    dictionary[k] = temp
                iterate_json(data[k], dictionary)
    else:
        return data
