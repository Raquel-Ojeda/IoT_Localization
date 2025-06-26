
import json
import psycopg2
import paho.mqtt.client as mqtt

# PostgreSQL connection
conn = psycopg2.connect(
    dbname="factory_tracking",
    user="postgres",
    password="Caterpillar",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to TTN MQTT broker successfully!")
        client.subscribe("v3/localization-thd@ttn/devices/+/up")
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        device_id = payload["end_device_ids"]["device_id"]
        fields = payload["uplink_message"]["decoded_payload"]

        lat = fields.get("latitude")
        lon = fields.get("longitude")
        battery = fields.get("battery")
        satellites = fields.get("satellites")

        print(f"Data from {device_id}: {lat}, {lon}, {battery}%, {satellites} satellites")

        cursor.execute(
            "INSERT INTO device_location (device_name, latitude, longitude, battery_percentage, satellites) VALUES (%s, %s, %s, %s, %s)",
            (device_id, lat, lon, battery, satellites)
        )
        conn.commit()


    except Exception as e:
        print("Error processing message:", e)

# MQTT Client
client = mqtt.Client()
client.username_pw_set("localization-thd@ttn", "NNSXS.HZN7UYSCS5XXQUI7U64A7VNWZAEQNEIUBMSM7BQ.THBQC3B2HCCWCO7VUJS2TZ5WOZXYWNOZ6QEXQRPNOUPOJAP7X2YA")
client.on_connect = on_connect
client.on_message = on_message

# Connect and run loop
client.connect("eu1.cloud.thethings.network", 1883, 60)
client.loop_forever()


