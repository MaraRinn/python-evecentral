python-evecentral
=================

Super simple module that hits 2 external APIs. 

It uses `Fuzzworks <[https://www.fuzzwork.co.uk/tools/api-typename-to-typeid/>`_ to get 
the typeID from a typeName. 

It then pulls prices from the `EVE-Central API <http://eve-central.com/home/develop.html>`_
and caches them in memory

market_stats API
================

::

    import evecentral
    
    stats = evecentral.market_stats("Tritanium", 10000032)
    # stats['region'] is 10000032
    # stats['minbuy'] is the lowest buy price in the region
    # stats['maxsell'] is the highest sell price in the region
    
    stats = evecentral.market_stats(["Tritanium", "Pyroxeres"], [10000032, 10000033])
    # stats[34]['region'] is [10000032, 10000033]
    # stats[34]['minbuy'] is the lowest buy price for Tritanium (item 34) in the nominated regions

