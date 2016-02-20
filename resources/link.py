# -*- coding: utf-8 -*-
import json
import re
import datetime
from flask_restful import Resource, reqparse, fields
from pymongo import MongoClient
from bson.objectid import ObjectId
from common.util import get_data_list, xstr

client = MongoClient('localhost', 27017)
db = client['board']
links = db['felinks']

post_parser = reqparse.RequestParser()
post_parser.add_argument('url', type=str, help='The link\'s url is null', required=True)
post_parser.add_argument('title', type=unicode, help='The link\'s title is null')
post_parser.add_argument('description', type=unicode, help='The link\'s title is null')

get_parser = reqparse.RequestParser()
get_parser.add_argument('limit', type=int, required=True)
get_parser.add_argument('after', type=str)
get_parser.add_argument('before',type=str)



class Link(Resource):
    def get(self, **kwargs):
        try:
            args = get_parser.parse_args()
            limit=args['limit'] + 1
            after=args['after']
            before=args['before']
            pattern='^[0-9a-fA-F]{24}$'
            query={}
            nav={'after':False, 'before':False}

            if re.match(pattern, xstr(after)):
                query["$lt"] = ObjectId(after)
                nav["before"] = True
                

            if re.match(pattern, xstr(before)):
                query["$gt"] = ObjectId(before)
                nav["after"] = True
            else:
                if "$lt" not in query:
                     query["$lt"] = ObjectId()

            # 获取数据, 从数据库读取的是cursor
            if "$lt" in query: 
                cursor = links.find( {'_id' : query }).limit(limit).sort([("_id",-1)]);
                data_list = get_data_list(cursor)
                if len(data_list) == limit:
                    nav["after"] = True
                    del data_list[-1]
            else:
                cursor = links.find( {'_id' : query }).limit(limit).sort([("_id",1)]);
                data_list = get_data_list(cursor)
                data_list = data_list[::-1]
                if len(data_list) == limit:
                    nav["before"] = True
                    del data_list[0]

            if data_list:
                before_id = data_list[0]['id'] if nav["before"] else None
                after_id =  data_list[-1]['id'] if nav["after"] else None
            else:
                before_id = None
                after_id = None
            
            res_data = {'data': data_list, 'before':before_id, 'after':after_id }
            return res_data
        except:
            return {'error': 'Not found'}, 404

    def post(self):
        try:       
            args = post_parser.parse_args()
            date = datetime.datetime.utcnow()
            _id = links.insert({'url': args.url, 'author': '', 'date': date, 'title': args.title, 'description': args.description});
            res_data = {'id':str(_id), 'url':args.url, 'title': args.title, 'description': args.description}
            return res_data
        except:
            return {'error': 'Not found'}, 404
