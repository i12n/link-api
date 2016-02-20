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
            # 为了解决 https 的问题使用 requests
            url_request = requests.get(url)
            # 处理utf gb2312 使用request.text ，但是 request.content 速度更快，参考 http://xiaorui.cc/2016/02/19/%E4%BB%A3%E7%A0%81%E5%88%86%E6%9E%90python-requests%E5%BA%93%E4%B8%AD%E6%96%87%E7%BC%96%E7%A0%81%E9%97%AE%E9%A2%98/
            tree = fromstring(url_request.text)
            title = tree.find(".//title")
            if title is not None:
                title = title.text
            else:
                title = ''
            description = tree.find(".//meta[@name='description']")
            if description is not None:
                description = description.get('content')
            else: 
                description = ''


            link = {'link': {'url':url, 'title':title, 'description':description}}
            return link
        except:
            return {'error': 'Not found'}, 404

