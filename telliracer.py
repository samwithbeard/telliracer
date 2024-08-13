import queue
import paho.mqtt.client as mqtt
import threading
import keyboard
import time

# Initialize player positions

stepSize=1
scores = []
print("------------------------------------------")
print("------------- telli racer ----------------")
print("------------------------------------------")
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
        client.subscribe(player2.topic)
        client.subscribe(player1.topic)                
        client.subscribe(MQTT_TOPIC_DATA)
        
    else:
        print("Failed to connect, return code %d\n", rc)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, message):
    print(f"Received message: '{message.payload.decode()}' on topic '{message.topic}'")
    try:
        if message.topic == player1.topic:
            player1.position += stepSize
            print(f"Player 1 is at {player1.position}%")
        elif message.topic == player2.topic:
            player2.position += stepSize
            print(f"Player 2 is at {player2.position}%")
        elif message.topic == MQTT_TOPIC_DATA:
            message.payload.decode()
            #print(f"race data {message.payload.decode()}%")
            if message.payload.decode()[:4]=="BUZZ":
                print("BUZZER RECEIVED")
                event_queue.put("buzz")
        else:
            print("othermessage received")
    except:
        print("message reception failed")
    
    message = str(player1.position)+";"+str(player2.position)
    client.publish(MQTT_TOPIC_POSITION, message)

# Create an MQTT client instance
client = mqtt.Client()
# Set the username and password

client.username_pw_set(user, passw)
client.on_connect = on_connect
client.on_message = on_message

# Subscribe to topics
client.subscribe(player1.topic)
client.subscribe(player2.topic)

# Connect to the MQTT broker
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Start the MQTT client loop in a separate thread
client.loop_start()

event_queue = queue.Queue()

def clear_event_queue():
    while not event_queue.empty():
        event_queue.get()
        
# Race function
def run_race():
    clear_event_queue()
    buzz =False
    player1.position=0
    player2.position=0    
    
    message = "race wait to start"
    print("-----state:"+ message)
    clear_event_queue()
    print("wait for button to be pressed..")
    client.publish(MQTT_TOPIC_STATE, message)
    while buzz ==False:              
        if not event_queue.empty():
                event = event_queue.get()
                if event == "buzz":
                    buzz = True 
                    message=print("Buzz start")
                    client.publish(MQTT_TOPIC_STATE, message)                                     
                    print(message)
    buzz =False    
    message = "countdown"
    print("-----state:"+ message)
    client.publish(MQTT_TOPIC_STATE, message)
    
    print("The race starts in:")
    for i in range(3, 0, -1):
        print(i)
        time.sleep(1)
    print("Go!") 
    player1.position=0
    player2.position=0       
    message = "race started"
    print("-----state:"+ message)
    client.publish(MQTT_TOPIC_STATE, message)
    clear_event_queue()
    start_time = time.time()    
    while player1.position < 100 and player2.position < 100 and buzz == False:
        '''
        if keyboard.is_pressed(player1.key):
            player1.position += stepSize
            print(f"Player 1 is at {player1.position}%")
            time.sleep(0.1)
        if keyboard.is_pressed(player2.key):
            player2.position += stepSize
            print(f"Player 2 is at {player2.position}%")
            time.sleep(0.1)
        '''
        
        # Hook the keyboard event
        #keyboard.wait()
        update_output(player1.position,player2.position)
        elapsed=time.time() - start_time
        print("elapsed time "+ str(int(elapsed))+"s")
        if not event_queue.empty():
            event = event_queue.get()
            if event == "buzz":
                buzz = True                    
                message=print("Buzz cancel")
                client.publish(MQTT_TOPIC_STATE, message)                                     
                print(message)
        time.sleep(1)
    print("loopended")
    # Stop the stopwatch
    end_time = time.time()
    race_time = end_time - start_time
    message = "race ended"
    print("-----state:"+ message)
    client.publish(MQTT_TOPIC_STATE, message)
    time.sleep(1)
    if player1.position >= 100 and player2.position >= 100:
        print("It's a tie!")
        winner= 'Player 1'
        scores.append({'player': player1.name, 'time': race_time})
        winner= 'Player 2'
        scores.append({'player': player2.name, 'time': race_time})
        winner="both"
        message="winner both"
        print("-----state:"+ message)    
        client.publish(MQTT_TOPIC_STATE, message) 
    elif player1.position >= 100:
        print("Player 1 wins!")
        winner= 'Player 1'
        scores.append({'player': player1.name, 'time': race_time})
        message="winner 1"
        print("-----state:"+ message)    
        client.publish(MQTT_TOPIC_STATE, message) 
    elif player2.position >= 100:
        print("Player 2 wins!")
        winner= 'Player 2'
        scores.append({'player': player2.name, 'time': race_time})
        message="winner 2"
        print("-----state:"+ message)    
        client.publish(MQTT_TOPIC_STATE, message) 
    else:
        print("no winner !")
        winner= 'none'
        message="winner none"
        print("-----state:"+ message)    
        client.publish(MQTT_TOPIC_STATE, message)  
        
    
    message = "the winner is "+winner+" with "+ str(race_time)    
    client.publish(MQTT_TOPIC_DATA, message) 
    
     # Print the race time
    print(f"Race time: {race_time:.2f} seconds")
    player1.position=0
    player2.position=0
    celebration_time=30#s
    print(str(celebration_time)+"celebration time")
    time.sleep(celebration_time) #celebration time
    # Clean up MQTT client


class StateMachine:       
    def __init__(self):
        self.state = "Idle"

    def transition(self, event):
        if self.state == "Idle":
            if event == "start":
                self.state = "Countdown"
                #state_countdown()
            elif event == "next":
                self.state = "Countdown"
                #state_countdown()
            else:
                print("transition not available")
        elif self.state == "Countdown":
            if event == "next":
                self.state = "Race"
                #state_race()
            elif event == "cancel":
                self.state = "Idle"
                #state_idle()
            else:
                print("transition not available")
        elif self.state == "Race":
            if event == "next":
                self.state = "Winnercelebration"
                #state_winner_cel()
            elif event == "cancel":
                self.state = "Idle"
                #state_idle()
            else:
                print("transition not available")
                
        elif self.state == "Winnercelebration":
            if event == "next":
                self.state = "Idle"
                #state_idle()
            elif event == "cancel":
                self.state = "Idle"
                #state_idle()
            elif event == "Record":
                self.state = "Recordcelebration"
                #state_record_celebration()
            else:
                print("transition not available")
        elif self.state == "Recordcelebration":
            if event == "next":
                self.state = "Idle"
                #state_idle()
            elif event == "cancel":
                self.state = "Idle"
                #state_idle()
            else:
                print("transition not available")
        
        self.print_state()

    def print_state(self):
        print(f"Current state: {self.state}")


# Example usage
sm = StateMachine()
sm.print_state()  # Initial state: Idle




while True:
    time.sleep(0.1)
    try:
        #sm.print_state() 
        run_race()
    except Exception as e:
        print("race aborted" + str(e)) 
           
    print("waiting for next round to be startet")
    time.sleep(0.1)
    clear_event_queue()

client.loop_stop()
client.disconnect()  

# Wait for MQTT thread to finish
mqtt_thread.join()