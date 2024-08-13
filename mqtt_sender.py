import paho.mqtt.client as mqtt
import keyboard

# Configuration
MQTT_BROKER = '192.168.0.101'  # Replace with your MQTT broker address
MQTT_PORT = 1883  # Default port for MQTT
MQTT_TOPIC_1 = "race/player1"
MQTT_TOPIC_2 = "race/player2"
MQTT_TOPIC_DATA ="race/data"
KEY_PLAYER_1 = 'space'  # The key to trigger the publish event
KEY_PLAYER_2 = '2'
KEY_BUZZ = 'b'
passw = 'telli2456'
user = 'lichtspiel'
print("---------------- MQTT SENDER ----------------")
# Callback when connecting to the MQTT broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        # Subscribe to the topic once connected
        client.subscribe(MQTT_TOPIC_1)
        client.subscribe(MQTT_TOPIC_2)
    else:
        print("Failed to connect, return code %d\n", rc)

# Callback for when a message is received
def on_message(client, userdata, msg):
    print(f"Received message: '{msg.payload.decode()}' on topic '{msg.topic}'")

# Create an MQTT client instance
client = mqtt.Client()

# Set the username and password
client.username_pw_set(user, passw)

# Assign the on_connect and on_message callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Start the MQTT client loop in a separate thread
client.loop_start()

# Callback function to handle key press
def on_key_press(event):
    print(event.name)
    print("-----")
    if event.name == KEY_PLAYER_1:
        message = "Player1 pressed the key!"
        client.publish(MQTT_TOPIC_1, message)
        print(f"Published message: '{message}' to topic: '{MQTT_TOPIC_1}'")
    elif event.name == KEY_PLAYER_2:
        message = "Player2 pressed the key!"
        client.publish(MQTT_TOPIC_2, message)
        print(f"Published message: '{message}' to topic: '{MQTT_TOPIC_2}'")
    elif event.name == KEY_BUZZ:
        print("BUZZZ")
        message="BUZZZ button pressed"
        client.publish(MQTT_TOPIC_DATA, message)
        
    print()    
    print(f"Press '{KEY_PLAYER_1}' or '{KEY_PLAYER_2}' to simulate a pulse and publish a message to the MQTT topic '{MQTT_TOPIC_2}' or {MQTT_TOPIC_2}'.")
    

# Hook the keyboard event
keyboard.on_press(on_key_press)

# Keep the script running
print(f"Press '{KEY_PLAYER_1}' or '{KEY_PLAYER_2}' or b for button to simulate a pulse and publish a message to the MQTT topic '{MQTT_TOPIC_2}' or {MQTT_TOPIC_2}'.")
keyboard.wait()

# Stop the loop before ending the script
client.loop_stop()
