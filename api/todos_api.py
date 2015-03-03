#!/usr/bin/env python3

import pymongo
import os
from flask import Flask, url_for, request, abort
from flask.views import MethodView
from tools import jsonify
from bson.objectid import ObjectId
from crossdomain import crossdomain

client = pymongo.MongoClient("mongodb://todos_admin:123456@ds049211.mongolab.com:49211/todos")
db = client.todos
entries = db.entries

app = Flask(__name__)

def remap_todo(todo):
    todo["id"] = todo["_id"]
    todo.pop("_id", None)
    return todo

class TodosAPI(MethodView):
    @crossdomain(origin = "*", methods = ["GET"])
    def get(self, todo_id):
        print ("get")
        if todo_id is None:
            tasks = list(entries.find())
            return jsonify({"todos": list(map(remap_todo, tasks))})
        else:
            todo_object_id = ObjectId(todo_id)
            todo = entries.find_one({"_id": todo_object_id})
            return jsonify(remap_todo(todo))
        
    @crossdomain(origin = "*", methods = ["POST"])
    def post(self):
        print ("post")
        if not request.json or not 'title' in request.json:
            abort(400)
        
        todo = {
            "title": request.json["title"],
            "isCompleted": request.json["isCompleted"] or False
        }
        
        result = entries.insert(todo)
        
        return jsonify({"result": result})
    
    @crossdomain(origin = "*", methods = ["DELETE"])
    def delete(self, todo_id):
        print ("delete")
        todo_object_id = ObjectId(todo_id)
        result = entries.remove({"_id": todo_object_id})
        if (result['ok'] == 1 and result['n'] > 0):
            return jsonify({"result": True})
        else:
            return jsonify({"result": False})
    
    @crossdomain(origin = "*", methods = ["PUT"])
    def put(self, todo_id):
        print ("put")
        if not request.json:
            abort(400)
        
        spec = {"_id": ObjectId(todo_id)}
        
        settings = {}
        
        if 'title' in request.json:
            settings["title"] = request.json["title"]
        
        if "isCompleted" in request.json:
            settings["isCompleted"] = request.json["isCompleted"]
            
        result = entries.update(spec, {"$set":settings})
        
        if result['ok'] and result['nModified'] and result['ok'] == 1 and result['nModified'] == 1:
            return jsonify({"result": True})
        else:
            return jsonify({"result": False})

todos_view = TodosAPI.as_view("todos_api")

def list_routes():
    import urllib
    output = []
    for rule in app.url_map.iter_rules():
        options = {}
        
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)
        
        methods = ",".join(rule.methods)
        with app.test_request_context():
            url = url_for(rule.endpoint, **options)
        
        line = urllib.parse.unquote("{:20s} {:40s} {}".format(rule.endpoint, methods, url))
        output.append(line)
    
    for line in sorted(output):
            print(line)

def register():
    endpoint = "/todos/api/v1.0"
    app.add_url_rule(endpoint + "/todos", defaults={"todo_id":None},
        view_func=todos_view, methods=["GET"])
        
    app.add_url_rule(endpoint + "/todos", view_func=todos_view, methods=["POST"])
    
    app.add_url_rule(endpoint + "/todos/<todo_id>", view_func=todos_view,
        methods=["GET", "PUT", "DELETE" ])
        
    #app.add_url_rule(endpoint + "/<path>", view_func=catchall, methods = ["OPTIONS"])
        
    list_routes()

def run():
    register()
    app.run(host="0.0.0.0", debug=True)


if __name__ == "__main__":
    run()