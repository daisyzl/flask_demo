# -*- coding:utf-8 -*-  
'''
function：
http://www.pythondoc.com/Flask-RESTful/quickstart.html
'''
from flask import Flask, request
from flask_restful import Resource, Api, fields, marshal_with

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


todos = {}


class TodoSimple(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}, 201, {'Etag': 'some-opaque-string'}
#  先执行put，再执行get
# Set the response code to 201 and return custom headers


# 格式化返回的数据格式
resource_fields = {
    'task':   fields.String,
    'uri':    fields.Url('todo_ep'),
    'todo_id': fields.String,
}


class TodoDao(object):
    def __init__(self, todo_id, task):
        self.todo_id = todo_id
        self.task = task

        # This field will not be sent in the response
        self.status = 'active'


class Todo(Resource):
    @marshal_with(resource_fields)
    def get(self):
        return TodoDao(todo_id='my_todo', task='Remember the milk')
'''
{
task: "Remember the milk",
uri: "/todo/hahaha",
todo_id: "my_todo"
}
'''
api.add_resource(HelloWorld, '/')
api.add_resource(TodoSimple, '/<string:todo_id>')
api.add_resource(Todo,
    '/todo/hahaha', endpoint='todo_ep')


if __name__ == '__main__':
    app.run(debug=True)