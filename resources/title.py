# -*- coding:utf-8 -*-
import datetime
from flask import make_response
from flask_restful import Resource, reqparse, fields, marshal_with
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps
from common.util import get_data_list
import json
import requests
from lxml.html import fromstring

parser = reqparse.RequestParser()
parser.add_argument('url', type=str, required=True)

class Title(Resource):
    def get(self, **kwargs):
        args = parser.parse_args()
        url = args.url
        try:
            url_request = requests.get(url)
            tree = fromstring(url_request.content)
            title = tree.find(".//title")
            if title is not None:
                title = title.text
            else:
                title = ''
            description = tree.find(".//meta[@name='description']")
            if description is not None:
                print description.get('content')
                description = description.get('content')
            else: 
                description = ''

            link = {'link': {'url':url, 'title':title, 'description':description}}
            data = json.dumps(link, ensure_ascii=False)
            response = make_response(data)
            response.headers['content-type'] = 'application/json; charset=utf-8'
            return response
        except:
            return {'error': 'Not found'}, 404

    def post(self):
        return {'hello':'123'}
        
        
