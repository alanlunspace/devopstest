#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from flask import Flask, request, json
import pprint as pp
import requests

app = Flask(__name__)

@app.route("/")
def root():
  print("OK")
  return 'OK'

@app.route('/test', methods=['POST'])
def test():
  if request.headers['Content-Type'] == 'application/json':
    pp.pprint(request.json)
    if 'ref' in request.json:
      if request.json['ref'] == 'refs/heads/master':
        json_str = json.dumps(request.json)
        commit_hash = request.json['commits'][0]['id']
        commit_message = request.json['commits'][0]['message']

        headers = {'Content-type': 'application/json',}
        data = f"{{ 'text': '[master] Latest committed {commit_hash}: {commit_message}' }}"
        slack_url = 'https://hooks.slack.com/services/xxxxxxxxx/xxxxxxxxx/xxxxxxxxxxxxxxxxxxxxxxxx'
        response = requests.post(slack_url, headers=headers, data=data)

        pp.pprint(response.text)
        return json_str
  return "POST"

if __name__ == "__main__":
  app.run(debug=True)
