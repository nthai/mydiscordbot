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

def get_json(query_url : str):
    query_req = urllib.request.Request(query_url, headers={'User-Agent' : 'PoeWiki'})
    try:
        response = urllib.request.urlopen(query_req).read().decode('utf-8').replace('&ndash;', '--')
    except urllib.error.HTTPError as err:
        print('Error code: {0}'.format(err.code))
        raise NetworkError
    except urllib.error.URLError as err:
        print('Error code: {0}'.format(err.reason))
        raise NetworkError
    
    return json.loads(response)

def search_item(item_name : str):
    query_url = SEARCH_URL.format(urllib.parse.quote(item_name))
    json_data = get_json(query_url)

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

def recursive_soup(item):
    for x in item.contents:
        pass

def get_item_info(item : str):
    query_url = ITEM_PANEL_URL.format(urllib.parse.quote(item))
    json_data = get_json(query_url)
    results = []
    
    if not json_data['query']['results']:
        raise NoItemFoundException

    for key, item in json_data['query']['results'].items():
        soup = BeautifulSoup(item['printouts']['Has infobox HTML'][0], 'html.parser')

        for cl in soup.find_all('em', {'class' : 'tc -value'}):
        	cl.replace_with(cl.text)

        for cl in soup.find_all('em', {'class' : 'tc -default'}):
        	cl.replace_with(cl.text)

        text = None
        text_list = []

        for child in soup.descendants:
        	name = getattr(child, 'name', None)
        	if name is not None:
        		if text is not None:
        			text_list.append(text)
        			text = None
        	else:
        		if text is None:
        			text = child
        		else:
        			text = text + child
        if text is not None:
        	text_list.append(text)

        results.append((key, text_list))
    
    if len(results) > 10:
        results = results[0:10]

    return results

def main():
    # results = get_item_info('Atziri\'s Disfavour')
    results = get_item_info('Vessel of Vinktar')
    for result in results:
    	print(result[0])
    	for text in result[1]:
    		print(text)
    	print('\n')

if __name__ == '__main__':
    main()