# -*- coding:utf-8 -*-
from bson.objectid import ObjectId
from datetime import datetime
import time

def get_data_list(cursor):
    data_list = []
    for document in cursor:
        item = {}
        for arr in document:
            value=document[arr]
            if isinstance(value, ObjectId):
                if arr == '_id':
                    item['id'] = str(value)
                else:
                    item[arr] = str(value)
            elif isinstance(value, datetime):
                item[arr] = int(time.mktime(value.timetuple()))
            else:
                item[arr]=document[arr]
        data_list.append(item);            
            
    return data_list

def xstr(s):
    if s is None:
        return ''
    return str(s)
