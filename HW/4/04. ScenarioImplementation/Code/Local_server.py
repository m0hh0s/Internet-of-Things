import threading
import jwt
import paho.mqtt.client as mqtt
import pymongo
from flask import *
import time
import requests
import asyncio
import aiocoap.resource as resource
import aiocoap

server = Flask("Local")
api_key = "very strong one"
office_name = "mashhad office"
coap_message = ""


class BlockResource(resource.Resource):
    def __init__(self):
        super().__init__()

    async def render_put(self, request):
        msg = request.payload.decode("utf8")
        message = msg.split('?')
        type = message[0]
        id = message[1]
        password = message[2]
        room = message[3]
        if type == "light":
            sensor_value = message[4]
            light_control([id, password, room, sensor_value])
        else:
            verify([id, password, room])
        time.sleep(2)
        return aiocoap.Message(payload=f'{coap_message}'.encode("utf8"))


async def coap_server():
    # Resource tree creation
    root = resource.Site()
    root.add_resource(['other', 'block'], BlockResource())
    await aiocoap.Context.create_server_context(bind=("127.0.0.1", None), site=root)
    # Run forever
    await asyncio.get_running_loop().create_future()


def verify(message):
    global coap_message
    if protocol == "MQTT":
        message = message.split('?')
    id = message[0]
    password = message[1]
    room = message[2]
    with pymongo.MongoClient("mongodb://localhost:27017/") as my_client:
        db = my_client["Local_server"]
        col = db["users"]
        query_result = col.find({"id": id, "password": password, "room": room})
        if protocol == "MQTT":
            client2 = mqtt.Client("LocalServer")
            client2.connect("localhost", port=1883)
            if query_result.__sizeof__() > 0:
                client2.publish("VERIFICATION_RES", "valid", 0)
            else:
                client2.publish("VERIFICATION_RES", "invalid", 0)
        else:
            if query_result.__sizeof__() > 0:
                coap_message = "valid"
            else:
                coap_message = "invalid"


def light_control(message):
    global coap_message
    if protocol == "MQTT":
        message = message.split('?')
    id = message[0]
    password = message[1]
    room = message[2]
    sensor_value = int(message[3])
    data = {"id": id,
            "password": password,
            "office": office_name,
            "room": room}
    resp = requests.post("http://localhost:5000/api/light", headers={"api-key": api_key}, json=data)
    user_light = int(resp.text)
    actuator_light = user_light - sensor_value
    if actuator_light < 0:
        actuator_light = 0
    if protocol == "MQTT":
        client3 = mqtt.Client("LocalServer")
        client3.connect("localhost", port=1883)
        client3.publish("ACTUATOR", actuator_light, 0)
    else:
        coap_message = actuator_light


def on_message(client, userdata, message):
    topic = str(message.topic)
    message = str(message.payload.decode("utf-8"))
    if topic == "VERIFICATION_REQ":
        verify(message)
    else:
        light_control(message)


def MQTT():
    while True:
        client = mqtt.Client("LocalServer")
        client.connect("localhost", port=1883)
        client.loop_start()
        client.subscribe("LIGHT")
        client.subscribe("VERIFICATION_REQ")
        client.on_message = on_message
        time.sleep(5)
        client.loop_stop()


def COAP():
    asyncio.run(coap_server())


def API_server():
    server.run(port=3000)


@server.route("/api/admin/login", methods=["POST"])
def admin_login():
    request_json = request.get_json()
    username = request_json["username"]
    password = request_json["password"]
    with pymongo.MongoClient("mongodb://localhost:27017/") as my_client:
        db = my_client["Local_server"]
        col = db["admins"]
        query_result = col.find({"user": username, "password": password})
        if query_result.__sizeof__() > 0:
            return Response(status=201, headers={'Cookie': {"access-level": "admin"}}, mimetype="application/json")
    return Response(status=401, mimetype="application/json")


@server.route("/api/admin/register", methods=["POST"])
def admin_register():
    request_json = request.get_json()
    username = request_json["username"]
    password = request_json["password"]
    with pymongo.MongoClient("mongodb://localhost:27017/") as my_client:
        db = my_client["Local_server"]
        col = db["admins"]
        col.insert_one({"user": username, "password": password})
    return Response(status=201, mimetype="application/json")


@server.route("/api/admin/user/register", methods=["POST"])
def user_register():
    request_json = request.get_json()
    id = request_json["id"]
    password = request_json["password"]
    room = request_json["room"]
    if request.cookies.get("access-level") == "admin":
        with pymongo.MongoClient("mongodb://localhost:27017/") as my_client:
            db = my_client["Local_server"]
            col = db["users"]
            col.insert_one({"id": id, "password": password, "room": room})
        return Response(status=201, mimetype="application/json")
    return Response(status=401, mimetype="application/json")


@server.route("/api/admin/activities", methods=["GET"])
def user_activity():
    pass


@server.route("/api/user/login", methods=["POST"])
def user_login():
    request_json = request.get_json()
    id = request_json["id"]
    password = request_json["password"]
    with pymongo.MongoClient("mongodb://localhost:27017/") as my_client:
        db = my_client["Local_server"]
        col = db["users"]
        query_result = col.find({"id": id, "password": password})
        if query_result.__sizeof__() > 0:
            return Response(status=201, headers={'Cookie': {"access-level": "user"}}, mimetype="application/json")
    return Response(status=401, mimetype="application/json")


@server.route("/api/user/<userid>", methods=["POST"])
def user_settings(userid):
    request_json = request.get_json()
    id = userid
    light = request_json["lights"]
    data = {"id": id,
            "light": light,
            "office": office_name}
    if request.cookies.get("access-level") == "user":
        resp = requests.post("http://localhost:5000/api/light/change", json=data)
        if resp.status_code == 200:
            return Response(status=201, mimetype="application/json")
        return Response(status=404, mimetype="application/json")
    return Response(status=401, mimetype="application/json")


protocol = input("Please Enter Either MQTT or COAP:")
if protocol == "MQTT":
    mqtt_thread = threading.Thread(target=MQTT)
    mqtt_thread.start()
    api_thread = threading.Thread(target=API_server)
    api_thread.start()
else:
    coap_thread = threading.Thread(target=COAP)
    coap_thread.start()
