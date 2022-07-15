import threading
import time
import pymongo
from flask import *


server = Flask("Central")


@server.route("/api/office/register", methods=["POST"])
def register_office():
	office_name = request.get_json()["name"]
	with pymongo.MongoClient("mongodb://localhost:27017/") as my_client:
		db = my_client["Central_server"]
		col = db["office"]
		data = {"id": col.count_documents({}), "name": office_name}
		col.insert_one(data)
	return Response("status: True", status=201, mimetype="application/json")


@server.route("/api/light", methods=["POST"])
def light_settings():
	if request.headers.get("api-key") == "very strong one":
		request_json = request.get_json()
		print(request_json)
		id = request_json["id"]
		password = request_json["password"]
		office = request_json["office"]
		room = request_json["room"]
		with pymongo.MongoClient("mongodb://localhost:27017/") as my_client:
			db = my_client["Central_server"]
			col = db["users"]
			query_result = col.find_one({"id": id, "password": password, "room": room, "office": office})
			if query_result is not None:
				return str(query_result["light"])
			return Response(status=404)
	return Response(status=401)


@server.route("/api/light/change", methods=["POST"])
def light_change():
	request_json = request.get_json()
	id = request_json["id"]
	light = request_json["light"]
	office = request_json["office"]
	my_query = {"id": id, "office": office}
	new_values = {"$set": {"light": light}}
	with pymongo.MongoClient("mongodb://localhost:27017/") as my_client:
		db = my_client["Central_server"]
		col = db["users"]
		col.update_one(my_query, new_values)
	return Response(status=200)


def run_server():
	server.run()


api_thread = threading.Thread(target=run_server)
api_thread.start()
while True:
	time.sleep(20)
