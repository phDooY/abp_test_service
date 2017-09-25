ABP filters/fragments URLs to CSV converter 
===========

Install requirements::

    $ sudo pip install -r requirements.txt

Usage::

    $ # fire up API service on localhost
    $ python api.py

    $ # call POST request to localhost passing json with
    $ # array of URLs or single URL in following format: 
    $ # {"urls": ["<url1>", "<url2>"]}
    $ curl -i -H "Content-Type: application/json" -X POST -d '{"urls": ["https://raw.githubusercontent.com/easylist/easylistgermany/master/easylistgermany/easylistgermany_adservers.txt"]}' http://localhost:5002/api/v1/event
