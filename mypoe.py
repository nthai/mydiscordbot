#!/usr/bin/env python3

import urllib.parse
import urllib.error
import urllib.request
import json
import re
from bs4 import BeautifulSoup

SEARCH_URL = 'http://pathofexile.gamepedia.com/api.php?action=opensearch&search={0}'
ITEM_PANEL_URL = 'https://pathofexile.gamepedia.com/api.php?action=askargs&conditions=Has%20name::{0}&printouts=Has%20infobox%20HTML&format=json'

class NoItemFoundException(Exception):
    pass

class NetworkError(Exception):
    pass

def search_item(item_name : str):
    query_url = SEARCH_URL.format(urllib.parse.quote(item_name))
    query_req = urllib.request.Request(query_url, headers={'User-Agent' : 'PoeWiki'})
    try:
        response = urllib.request.urlopen(query_req).read().decode('utf-8')
    except urllib.error.HTTPError as err:
        print('Error code: {0}'.format(err.code))
        raise NetworkError
    except urllib.error.URLError as err:
        print('Error code: {0}'.format(err.reason))
        raise NetworkError
    
    json_data = json.loads(response)

    if len(json_data[1]) == 0 or len(json_data[3]) == 0:
        raise NoItemFoundException
    else:
        if len(json_data[1]) > 10:
            name_list = json_data[1][0:10]
            link_list = json_data[3][0:10]
        else:
            name_list = json_data[1]
            link_list = json_data[3]
        return name_list, link_list

def get_item_panel(item : str):
    print('getting item panel...')
    try:
        item_name, item_link = search_item(item)
    except NetworkError:
        print('Network Error.')
        raise NetworkError
    except NoItemFoundException:
        print('No item found exception.')
        raise NoItemFoundException
    print('item found!')
    query_url = ITEM_PANEL_URL.format(urllib.parse.quote(item_name[0]))
    query_req = urllib.request.Request(query_url, headers={'User-Agent' : 'PoeWiki'})
    try:
        response = urllib.request.urlopen(query_req).read().decode('utf-8')
    except urllib.error.HTTPError as err:
        print('Error code: {0}'.format(err.code))
        raise NetworkError
    except urllib.error.URLError as err:
        print('Error code: {0}'.format(err.reason))
        raise NetworkError
    
    print('json data retrieved!')
    json_data = json.loads(response)
    results = []
    
    for key, item in json_data['query']['results'].items():
        print('processing ' + str(key) + '...')
        soup = BeautifulSoup(item['printouts']['Has infobox HTML'][0], 'html.parser')
        results.append((key, soup.get_text().encode('utf-8')))
    
    if len(results) > 10:
        results = results[0:10]

    return results


def main():
    results = get_item_panel('Atziri\'s Disfavour')
    print(results[0][1])

if __name__ == '__main__':
    main()