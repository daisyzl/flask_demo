# -*- coding:utf-8 -*-  
'''
function：
'''
from flask import Flask, jsonify
from flask_restful import Api, reqparse, fields, Resource, marshal

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('dates', required=True)
parser.add_argument('bing_url', required=True)
parser.add_argument('qiniu_url', required=True)
# parser.add_argument('user_nickname')
parser.add_argument('image_name', required=True)

resource_full_fields = {
    'id': fields.Integer,
    'dates': fields.String,
    'bing_url': fields.String,
    'qiniu_url': fields.String,
    'image_name': fields.String
}


class Common:
    def returnTrueJson(self, data, msg="请求成功"):
        return jsonify({
            "status": 1,
            "data": data,
            "msg": msg
        })

    def returnFalseJson(self, data=None, msg="请求失败"):
        return jsonify({
            "status": 0,
            "data": data,
            "msg": msg
        })


class Hello(Resource):

    def get(self):
        return 'Hello Flask!'


class Bing_all(Resource):
    def get(self):
        # dates = Bing.query.filter_by()
        return Common.returnTrueJson(Common, marshal(Bing.query.all(), resource_full_fields))


class Bing_url(Resource):
    def get(self, dates):
        dates = Bing.query.filter_by(dates=dates).first()
        if (dates is None):
            abort(410, msg="找不到数据！", data=None, status=0)
        else:
            return Common.returnTrueJson(Common, marshal(dates, resource_full_fields))


api.add_resource(Hello, '/', '/hello')
api.add_resource(Bing_all, '/bing')
api.add_resource(Bing_url, '/bing/<string:dates>')


if __name__ == '__main__':
    app.run(debug=True)