ABP filters/fragments URLs to CSV converter 
===========

Current status: Work In Progress


Install requirements:

    $ sudo pip install -r requirements.txt

Usage:

    $ # fire up API service on localhost
    $ python api.py

    $ # call POST request to localhost passing json with
    $ # array of URLs or single URL in following format: 
    $ # {"urls": ["<url1>", "<url2>"]}
    $ curl -i -H "Content-Type: application/json" -X POST -d '{"urls": ["https://raw.githubusercontent.com/easylist/easylistgermany/master/easylistgermany/easylistgermany_adservers.txt"]}' http://localhost:5002/api/v1/event

This will create 3 files in the folder from where script is called: 
    <date>_<time>_fragments.txt - a file consisting of fragments of urls you passed in request
    <date>_<time>_list.txt - raw text ABP filters file
    <date>_<time>_list.csv - ABP filters in CSV format

API will return download link for CSV formatted filter file, usable for analytical processing (currently with only 4 fields: text, action, selector, options).


Further developments
===========

* Add method to parse Filter object, and detect fields, and apped them to CSV file on the go.
* Accept text filter files as well, not only URLs.
* Ideally there should be database fired up, where requests can be saved.
* On top of database there can be simple visualization/analytical tool.
