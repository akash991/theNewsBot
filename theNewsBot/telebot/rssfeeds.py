import requests
from bs4 import BeautifulSoup

def collect_feeds_theHindu(rss_json):
    """
    Extract news feed from theHindu
    """
    the_hindu_rss_feeds_url = "https://www.thehindu.com/rssfeeds/"

    rss_json["theHindu"] = {}
    response = requests.get(url=the_hindu_rss_feeds_url)
    soup = BeautifulSoup(response.text, features="lxml")
    sublevel2 = soup.body.find('ul', attrs={'class':'sublevel2'})

    keys = []
    temp = rss_json["theHindu"]
    for child in sublevel2.findAll():
        if child.name == "ul":
            rss_json["theHindu"][keys[-1]] = {}
            temp = rss_json["theHindu"][keys[-1]]
        elif child.name == "li":
            keys.append(child.a.get('href').split("/")[-3].replace("-", "_").lower())
            temp[keys[-1]] = child.a.get('href')

def collect_feeds_theET(rss_json):
    """
    Extract news feed from theEconomicTimes
    """
    the_et_base_url = "https://economictimes.indiatimes.com"
    the_et_rss_feed_url = "https://economictimes.indiatimes.com/rss.cms"
    
    rss_json["theET"] = {}
    response = requests.get(url=the_et_rss_feed_url)
    soup = BeautifulSoup(response.text, features="lxml")
    rssSubHead = soup.body.findAll('div', attrs={'class':'rssSubHead'})

    for rss in rssSubHead:
        if rss.a.text.lower() == "news":
            ul = rss.find_next_sibling('ul')
            for li in ul.findAll("li"):
                url = "{}{}".format(the_et_base_url, li.a.get("href"))
                feed = li.a.get("href").split("/")[2].replace("-", "_")
                rss_json["theET"][feed] = url

def collect_feeds():
    """
    Method to parse the html response
    Collect all the feeds along with their name and url
    """
    rss_json = {}
    collect_feeds_theHindu(rss_json)
    collect_feeds_theET(rss_json)
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
                temp = list(v.keys())
                dictionary[k] = temp
                iterate_json(data[k], dictionary)
            else:
                dictionary[k] = v
    else:
        return data
