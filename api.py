#!/usr/bin/env python

# Micro event processor service through REST API.
#
# References:
# - http://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
# - http://www.w3.org/Protocols/HTTP/HTRESP.html
# 
# Testing:
# curl -i -H "Content-Type: application/json" -X POST -d '{"urls": []}' http://localhost:5002/api/v1/event

import csv
import datetime
import json
import logging
import sys
from flask import Flask, jsonify, request, make_response
from abp.filters import parse_filterlist
from subprocess import call

print("Instantiating application")
app = Flask(__name__)


@app.errorhandler(404)
def not_recognized(error):
    return make_response(jsonify({'error': 'Not recognized'}), 404)


@app.route('/api/v1/event', methods=['POST', 'GET'])
def receive_event():
    req_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    event = req = request.json
    params = ['urls']
    if event is None:
        return make_response(jsonify({'error': 'No input parameter sent'}), 400)

    for i in range(len(params)):
        if params[i] not in event:
            return make_response(jsonify({'error': params[i] + ' parameter not sent'}), 400)

    urls = req['urls']
    
    if not urls:
        return make_response(jsonify({'error': 'empty url list'}), 400)
    
    # removed due to possibilities of injects
    #file_name = req['file_name'] if req['file_name'] else 
    fragments_file_name = req_time + '_fragments.txt'
    list_file_name = req_time + '_list.txt'
    csv_file_name = req_time + '_list.csv'

    with open(fragments_file_name, 'w+') as fragments:
        fragments.write('[Adblock Plus 2.0]' + '\n')
        for url in urls:
            fragments.write('%include ' + url + '%\n')

    call(["flrender", fragments_file_name, list_file_name])


    with open(csv_file_name, "wb") as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(['<header_placeholder>'])
        csv_header = ['text', 'action', 'selector', 'options']

        with open(list_file_name) as list_file:
            list_iterator = parse_filterlist(list_file)
            for i in list_iterator:
                # skip non-Filters
                if not 'abp.filters.parser.Filter' in str(type(i)):
                    continue
                #text = i.text if i.text else ''
                #action = i.action if i.action else ''
                #selector = i.selector if i.selector else ''
                #options = i.options if i.options else ''
                try:
                    row = [i.text, i.action, json.dumps(i.selector), json.dumps(i.options)]
                    writer.writerow(row)
                except UnicodeEncodeError:
                    print 'broken row:'
                    print row
                    continue

    # replace header placeholder with actual header
    call(["sed", "-i", "s/<header_placeholder>/{}/g".format(';'.join(csv_header)), csv_file_name])
    #
    # 


    return make_response(jsonify({'success': 'download your file from http://'}), 200)

if __name__ == '__main__':
    log_handler = logging.StreamHandler(sys.stdout)
    log_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(log_handler)
    app.logger.setLevel(logging.DEBUG)
    app.run(host='0.0.0.0', port=5002, debug=False)