from pythonosc import udp_client
import time
import os
import paho.mqtt.client as mqtt
import math
#rom pythonping import ping

print("------------------------------------------")
print("------------- osc server  ----------------")
print("------------------------------------------")

#colunms sind die zeilein es gibt col 1 und col2 
#layers sind stockwerke
#clips sind einzelne lampen
#es gibt spezial clips für spezielle states.

RESOLUM_IP='192.168.0.3'
RESOLUM_PORT=5300
MAX_FLOOR=21 #21
MIN_FLOOR=1
GAME_STATE="none"


# MQTT Configuration
MQTT_BROKER = '192.168.1.119'
MQTT_PORT = 1883
POSITION_TOPIC="race/positionreport" 

MQTT_TOPIC_DATA = "race/data"
GAME_STATE_TOPIC="race/gamestate"
PLAYER_TOPIC="race/player2"
passw = 'telli2456'
user = 'lichtspiel'

'''
def check_ping(hostname, name=""):    
    
    response=ping(hostname, size=40, count=1)
    # and then check the response...
    if response == 0:
        pingstatus = name+""+hostname+" reachable"
    else:
        pingstatus = name+""+hostname+" NOT reachable"
    
    return pingstatus

def ping_check_all():
    t2=check_ping(MQTT_BROKER,"mqtt server")
    t1=check_ping("192.168.0.100","raspi")
    t3=check_ping(RESOLUM_IP,"resolum")
    t4=check_ping("192.168.0.2","funk")
    return (t1 and t2 and t3 and t4)
'''
    
 
# Callback when connecting to the MQTT broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(POSITION_TOPIC)
        client.subscribe(GAME_STATE_TOPIC)
        client.subscribe(MQTT_TOPIC_DATA)
        print("subscribed")

# Callback for when a message is received
def on_message(client, userdata, msg):
    print(msg)
    game_data=""
    if msg.topic == POSITION_TOPIC:
        # Parse the position message
        position1, position2 = msg.payload.decode().split(';')
        #turn_on_window_up_to(1, int(percent_to_floor(float(position1.strip()))))
        #turn_on_window_up_to(2, int(percent_to_floor(float(position2.strip()))))
        
        turn_on_window(1, int(percent_to_floor(float(position1.strip()))))
        turn_on_window(2, int(percent_to_floor(float(position2.strip()))))
        print("position topic received: turn on lamp"+str((position1.strip()))+" " +str(position2.strip()))
        
    elif msg.topic == GAME_STATE_TOPIC:
        SLEEP_TO_RESET=0.1
        # Handle game state messages
        game_state = msg.payload.decode()
        GAME_STATE=game_state
        if game_state == "race wait to start":
            turn_off_all()
            time.sleep(SLEEP_TO_RESET)
            special_clips(3)
            '''
            turn_on_window_up_to(1, 100)
            turn_on_window_up_to(2, 100)
            time.sleep(0.3)
            turn_on_window_up_to(1, 50)
            turn_on_window_up_to(2, 50)
            time.sleep(0.3)
            '''
        elif game_state == "countdown":
            print("countdown")
            countdown()   
            
        elif game_state == "race started":
            print("turn off all")
            turn_off_all()
            
        elif game_state == "race ended":
            print("message received race ended")
            time.sleep(SLEEP_TO_RESET)
            turn_off_all()
            time.sleep(SLEEP_TO_RESET)
            special_clips(4)
        elif game_state == "winner 1":  
            print("winner 1" + game_data)
            time.sleep(SLEEP_TO_RESET)
            turn_off_all()
            time.sleep(SLEEP_TO_RESET)
            special_clips(5)
        elif game_state == "winner 2":  
            print("winner 2" + game_data)
            time.sleep(SLEEP_TO_RESET)
            turn_off_all()
            time.sleep(SLEEP_TO_RESET)
            special_clips(6)
        elif game_state == "winner both":  
            print("winner both" + game_data)
            time.sleep(SLEEP_TO_RESET)
            turn_off_all()
            time.sleep(SLEEP_TO_RESET)
            special_clips(7)
        elif game_state == "winner none":  
            print("winner none" + game_data)
            time.sleep(SLEEP_TO_RESET)
            turn_off_all()
            time.sleep(SLEEP_TO_RESET)
            special_clips(8)
        elif game_state == "buzz start":  
            print("received " + game_data)
            hau_den_lukas()
        elif game_state == "buzz cancel":  
            print("received " + game_data)
            hau_den_lukas()
        else:
            print("game state " + game_data +"not handled")
            
    elif msg.topic == MQTT_TOPIC_DATA:
        game_data = msg.payload.decode()
        if game_data=="BUZZZ button pressed":
            print("no action on button pressed")
        else:
            print("game data not handled"+str(game_data))
        
         
             
        
        #todo handle_game_state(game_state)
    else:
        print("other topic")

def send_osc_command(ip, port, address, value):
    client = udp_client.SimpleUDPClient(ip, port)
    client.send_message(address, value)
    print(f"Sent OSC message to {ip}:{port} with address {address} and value {value}")

def turn_on_window(col, floor):
    # Define the OSC address and value
    osc_address = f"/composition/layers/{int(floor)}/clips/{int(col)}/connect"  # Example OSC address to trigger a clip
    osc_value = 1  # Example value, typically 1 to trigger the clip
    # Send the OSC command
    send_osc_command(RESOLUM_IP, RESOLUM_PORT, osc_address, osc_value)

def turn_on_col(col=1):
    # ganze column starten
    osc_address = f"/composition/columns/{int(col)}/connect"  # Example OSC address to trigger a clip
    osc_value = 1  # Example value, typically 1 to trigger the clip
    # Send the OSC command
    send_osc_command(RESOLUM_IP, RESOLUM_PORT, osc_address, osc_value)

def turn_off_all():
    # Define the OSC address and value   
    osc_address = "/composition/disconnectall"  # Example OSC address to trigger a clip
    osc_value = 1  # Example value, typically 1 to trigger the clip
    # Send the OSC command
    send_osc_command(RESOLUM_IP, RESOLUM_PORT, osc_address, osc_value)

def turn_on_window_up_to( col, floor):
    # Define the OSC address and value
    print(f"turn on col{int(col)} from {int(floor)} to {MIN_FLOOR}")
    while floor>=MIN_FLOOR:
        osc_address = f"/composition/layers/{int(floor)}/clips/{int(col)}/connect"  # Example OSC address to trigger a clip
        osc_value = 1  # Example value, typically 1 to trigger the clip
        print(osc_address)
        # Send the OSC command
        send_osc_command(RESOLUM_IP, RESOLUM_PORT, osc_address, osc_value)
        floor = floor - 1

def special_clips(index):
    # Define the OSC address and value
    osc_address = f"/composition/layers/{int(index)}/clips/3/connect"  # Example OSC address to trigger a clip
    osc_value = 1  # Example value, typically 1 to trigger the clip
    # Send the OSC command
    send_osc_command(RESOLUM_IP, RESOLUM_PORT, osc_address, osc_value)
    
def countdown():
    special_clips(9)

def percent_to_floor(percent):
    floors=MAX_FLOOR-MIN_FLOOR
    floor=((percent*floors)/100)+MIN_FLOOR
    return floor

        
def hau_den_lukas(g=9.81):
    turn_off_all()
    print("hau den lukas")
    # This will control the overall timing; tweak this to change the speed of the entire motion.
    BASE_PAUSE = 1.0 / g  # The base pause is inversely proportional to gravity

    for floor in range(1, MAX_FLOOR + 1):
        # On the way up, the pause increases as the object slows down
        pause = BASE_PAUSE * math.sqrt((2 * (MAX_FLOOR - floor)) / g)
        turn_on_window(1, floor)
        turn_on_window(1, floor)
        time.sleep(pause)
        
    for floor in range(MAX_FLOOR - 1, 0, -1):
        # On the way down, the pause decreases as the object speeds up
        pause = BASE_PAUSE * math.sqrt((2 * (MAX_FLOOR - floor)) / g)
        turn_on_window(1, floor)
        turn_on_window(1, floor)
        time.sleep(pause)
        

def test():
    print("start")
    floor_30_percent=percent_to_floor(30)
    print(f"30% floor is {floor_30_percent}")
    floor_1_percent=percent_to_floor(1)
    print(f"1% floor is {floor_1_percent}")
    floor_100_percent=percent_to_floor(100)
    print(f"100% floor is {floor_100_percent}")
    floor_99_9_percent=percent_to_floor(99.9)
    print(f"99.9% floor is {floor_99_9_percent}")
    turn_off_all()
    turn_on_window(1, 7)
    time.sleep(1)
    turn_on_window_up_to(2, 7)
    time.sleep(1)
    turn_off_all()
    time.sleep(0.3)
    turn_on_col(1)
    time.sleep(1)
    turn_on_col(2)
    time.sleep(1)
    turn_off_all()

#test()
#ping_check_all()
turn_off_all()
print("testbeendet")
print("start mqtt client ..")
# Create an MQTT client instance
client = mqtt.Client()

# Set the username and password if your MQTT broker requires them

client.username_pw_set(user, passw)

# Assign the on_connect and on_message callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
except Exception as e:
    print("mqtt server not reachable on "+MQTT_BROKER+" check switch and IP adresses. "+e)

# Start the MQTT client loop in a separate thread
client.loop_start()


# Keep the script running
try:
    while True:
        time.sleep(10)
        print("osc client is waiting for mqtt message end with ctrl+c ..")
except KeyboardInterrupt:
    print("Script interrupted by user")

# Stop the loop and cleanup GPIO before ending the script
client.loop_stop()
print("loop stopped ..")