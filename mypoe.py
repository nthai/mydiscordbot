#!/usr/bin/env python3

import urllib.parse
import urllib.error
import urllib.request
import json

SEARCH_URL = 'http://pathofexile.gamepedia.com/api.php?action=opensearch&search={0}'
ITEM_PANEL_URL = 'https://pathofexile.gamepedia.com/api.php?action=askargs&conditions=Has%%20name::{0}&printouts=Has%%20infobox%%20HTML&format=json'

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
    # TODO
    try:
        item_name, item_link = search_item(item)
    except NetworkError:
        print('Network Error.')
        return None
    except NoItemFoundException:
        print('No item found exception.')
        return None
    query_url = ITEM_PANEL_URL.format(urllib.parse.quote(item_name[0]))
    print(query_url)


def main():
    print(search_item('vessel'))

if __name__ == '__main__':
    main()