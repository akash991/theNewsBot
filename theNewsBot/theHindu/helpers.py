import json
from theHindu import load_data

the_hindu_dot_json = "../data/theHindu.json"

def get_data(key):
    data = None
    data = get_all_keys()
    data = data[key]
    if len(data) == 1:
        data = load_data.fetch_items(url=data[0])
    return data

def get_all_keys():
    data = None
    json_response = None
    with open(the_hindu_dot_json) as file:
        json_response = json.load(file)
    json_response = json_response
    dictionary = {}
    iterate_json(json_response, dictionary)
    return dictionary

def iterate_json(data, dictionary):
    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, dict):
                elem = list(v.keys())
                elem.remove('url')
                elem.remove('article')
                if len(elem) == 0:
                    elem.append(v["url"])
                dictionary[k] = elem
                iterate_json(data[k], dictionary)
    else:
        return data
