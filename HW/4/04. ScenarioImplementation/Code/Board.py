import datetime
import time
import threading
from random import randrange
import paho.mqtt.client as mqtt
import logging
import asyncio
from aiocoap import *

logging.basicConfig(level=logging.INFO)
coap_message = None
verification_message = ""
actuator_message = -1
stop_thread = False


async def client():
	global verification_message, actuator_message, coap_message
	if coap_message is not None:
		context = await Context.create_client_context()
		payload = coap_message.encode("utf8")
		request = Message(code=3, payload=payload, uri="coap://127.0.0.1/other/block")
		response = await context.request(request).response
		verification_message = response.payload.decode("utf8")
		coap_message = None


def coap():
	asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
	asyncio.run(client())


def on_message(client, userdata, message):
	global verification_message, actuator_message
	verification_message = str(message.payload.decode("utf-8"))
	if len(str(message.payload.decode("utf-8"))) < 3:
		if int(message.payload.decode("utf-8")) != actuator_message and actuator_message == -1:
			actuator_message = int(message.payload.decode("utf-8"))
		else:
			actuator_message = -1


def door_sensor(id, password, room):
	global protocol, coap_message
	if protocol == "MQTT":
		door_client = mqtt.Client("Door_Sensor")
		door_client.connect("localhost", port=1883)
		door_client.publish("VERIFICATION_REQ", str(id) + '?' + str(password) + '?' + str(room) + '?' + "enter", 0)
		door_client.loop_start()
		door_client.subscribe("VERIFICATION_RES")
		door_client.on_message = on_message
		time.sleep(2)
		door_client.loop_stop()
		if verification_message == "valid":
			return True
		else:
			return False
	else:
		coap_message = "door" + '?' + str(id) + '?' + str(password) + '?' + str(room)
		time.sleep(2)
		if verification_message == "valid":
			return True
		else:
			return False


def light_sensor():
	global protocol, id, password, room, coap_message
	if protocol == "MQTT":
		light_client = mqtt.Client("Light_Sensor")
		light_client.connect("localhost", port=1883)
		while True:
			rand_number = random_light()
			light_client.publish("LIGHT", str(id) + '?' + str(password) + '?' + str(room) + '?' + str(rand_number), 0)
			time.sleep(5)
			if stop_thread:
				break
	else:
		while True:
			rand_number = random_light()
			coap_message = "light" + '?' + str(id) + '?' + str(password) + '?' + str(room) + '?' + str(rand_number)
			if stop_thread:
				break


def random_light():
	hour = datetime.datetime.now().hour
	if 8 <= hour <= 16:
		return randrange(66, 100)
	elif 20 <= hour or hour <= 4:
		return randrange(0, 33)
	else:
		return randrange(33, 66)


def actuator():
	global protocol
	if protocol == "MQTT":
		while True:
			door_client = mqtt.Client("Actuator")
			door_client.connect("localhost", port=1883)
			door_client.loop_start()
			door_client.subscribe("ACTUATOR")
			door_client.on_message = on_message
			time.sleep(2)
			door_client.loop_stop()
			if actuator_message != -1:
				print("Setting light to " + str(actuator_message))
			if stop_thread:
				break
	else:
		pass


id = input("Please Enter your Username:")
password = input("Please Enter your Password:")
room = input("Please Enter The Room Number:")
protocol = input("Please Enter Either MQTT or COAP:")
if protocol == "COAP":
	coap_thread = threading.Thread(target=coap)
	coap_thread.start()
if door_sensor(id, password, room):
	print("Welcome To Room " + str(room))
	sensor_thread = threading.Thread(target=light_sensor)
	sensor_thread.start()
	actuator_thread = threading.Thread(target=actuator)
	actuator_thread.start()
	while True:
		if input('Type "exit" to Exit The Room:') == "exit":
			stop_thread = True
			break
else:
	print("Entry Not Authorized")
