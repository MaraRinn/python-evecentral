"""
Very small module to cache EVE Central prices results locally in memory

Also does a lookup of item_name so you don't need to know pesky item IDs
"""
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import requests
import collections

EVE_CENTRAL_QUERY="http://api.eve-central.com/api/marketstat"
FUZZWORKS_QUERY="https://www.fuzzwork.co.uk/api/typeid.php?typename={item}"
JITA_REGION_ID='10000002'

__all__ = ("market_stats",)

PRICES = {}
ITEMIDS = {}

def _price_request(item_id, region):
    shitxml = requests.get(EVE_CENTRAL_QUERY, params={'typeid':item_id, 'regionlimit':region})
    rootshit = ET.fromstring(shitxml.text)
    item = rootshit[0][0]
    price = {
            "region": region,
            "maxbuy": float(item.find('buy').find('max').text),
            "minsell": float(item.find('sell').find('min').text),
            "cached_at": datetime.utcnow()
    }
    return price

def _get_item_stats(item_id, region):
    if item_id in PRICES:
        item = PRICES[item_id]
        if item['cached_at'] + timedelta(hours=1) < datetime.utcnow():
            return item
    item = _price_request(item_id, region)
    PRICES[item_id] = item
    return item

def _get_item_id(item_name):
    if item_name not in ITEMIDS:
        resp = requests.get(FUZZWORKS_QUERY.format(item=item_name))
        if resp.status_code != 200:
            raise RuntimeError("An error occurred with the item type resolver")
        elif resp.json()['typeName'] == 'bad item':
            raise ValueError("The item name '%s' is not known to the item type resolver" % item_name)
        else:
            item_id = resp.json()['typeID']
        ITEMIDS[item_name] = item_id
    else:
        item_id = ITEMIDS[item_name]
    return item_id

def market_stats(item_name, region=JITA_REGION_ID):
    if isinstance(item_name, collections.Sequence) and not isinstance(item_name, (str, unicode)):
        item_stats = {}
        for item in item_name:
            item_id = _get_item_id(item)
            this_stats = _get_item_stats(item_id, region)
            item_stats[item_id] = this_stats
    else:
        item_id = _get_item_id(item_name)
        item_stats = _get_item_stats(item_id, region)
    return item_stats
