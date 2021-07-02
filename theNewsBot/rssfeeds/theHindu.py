import requests
from bs4 import BeautifulSoup

the_hindu_base_url = "https://www.thehindu.com/"
the_hindu_rss_feeds_url = "https://www.thehindu.com/rssfeeds/"

def collect_feeds():
    """
    Method to parse the html response
    Collect all the feeds along with their name and url
    """
    feeds = []
    rss_json = {}
    response = requests.get(url=the_hindu_rss_feeds_url)
    soup = BeautifulSoup(response.text, features="lxml")
    sublevel2 = soup.body.find('ul', attrs={'class':'sublevel2'})

    for child in sublevel2.findAll("li"):
        url = child.a.get('href')
        feed_pos = url.split(the_hindu_base_url)[1].split("/feeder/default.rss")[0].lower()
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
