# -*- coding:utf-8 -*-
from flask import Flask
from flask_restful import Api
from resources.link import Link
from resources.title import Title

app = Flask(__name__)

api = Api(app)
api.add_resource(Link, 
    '/',
    '/links/<string:id>', # /link/12345
    '/links', # /link
    endpoint='all'  # /link/all
    )

api.add_resource(Title, '/title')

if __name__ == '__main__':
    app.run(debug=True)

