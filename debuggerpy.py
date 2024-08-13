import paho.mqtt.client as mqtt
import threading
import keyboard
import time

print("------------------------------------------")
print("------------- debugger mon----------------")
print("------------------------------------------")


stepSize=5
scores = []

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.position = 0
        self.key = "0" 
        self.topic = "race/player" 
        self.speed = 0

    def update_score(self, points):
        self.score += points

    def update_position(self, steps):
        self.position += steps

    def display_info(self):
        print(f"Player: {self.name}, Score: {self.score}, Position: {self.position}")


# Creating two player objects
player1 = Player("Alice")
player2 = Player("Bob")
player1.position = 0
player2.position = 0
# Define keys for each player
player1.key = 'a'  # Player 1's key
player2.key = 'l'  # Player 2's key
GAME_STATE = 'none'

# MQTT setup
broker_address = "192.168.0.101"  # Use your broker address 5672
player1.topic = "race/player1"  # Topic for player 1
player2.topic = "race/player2"  # Topic for player 2

MQTT_BROKER="192.168.0.101"  # Use your broker address 5672
MQTT_PORT = 1883  # Default port for MQTT

MQTT_TOPIC_STATE = "race/gamestate"
MQTT_TOPIC_DEBUG = "race/debug"
MQTT_TOPIC_POSITION = "race/positionreport"
MQTT_TOPIC_DATA = "race/data"
passw = 'telli2456'
user = 'lichtspiel'
# Start the stopwatch

def update_output(player1_position,player2_position):
    #print("|"*player1_position)
    #print("|"*player2_position)
    player1_position=player1_position

# Callback when connecting to the MQTT broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        # Subscribe to the topic once connected
        client.subscribe(player1.topic)
        client.subscribe(player2.topic)
        client.subscribe(MQTT_TOPIC_DEBUG)
        client.subscribe(MQTT_TOPIC_DATA)
        client.subscribe(MQTT_TOPIC_STATE)
        client.subscribe(MQTT_TOPIC_POSITION)        
    else:
        print("Failed to connect, return code %d\n", rc)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, message):
    print(f"Received message: '{message.payload.decode()}' on topic '{message.topic}'")
    if message.topic==MQTT_TOPIC_DEBUG:
        if message.payload.decode()[:14]=="raspi CPU temp":
            temp=int(message.payload.decode()[15:])
            print("|"*temp)
            if temp > 79:
                print("OVERHEATING!!!!!!!!!!!!!!!!!!!!")
    
    

# Create an MQTT client instance
client = mqtt.Client()
# Set the username and password

client.username_pw_set(user, passw)
client.on_connect = on_connect
client.on_message = on_message


# Subscribe to topics
client.subscribe(player1.topic)
client.subscribe(player2.topic)
client.subscribe(MQTT_TOPIC_DEBUG)
client.subscribe(MQTT_TOPIC_DATA)
client.subscribe(MQTT_TOPIC_STATE)
client.subscribe(MQTT_TOPIC_POSITION)

# Connect to the MQTT broker
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Start the MQTT client loop in a separate thread
client.loop_start()



user_ready=True
# Run the race
print("waiting for messages")
while True:
    print("debug monitor running")
    time.sleep(5)
    try:
        time.sleep(5)   
    except:
        print("race aborted")    
    
    time.sleep(10)

client.loop_stop()
client.disconnect()  

# Wait for MQTT thread to finish
mqtt_thread.join()