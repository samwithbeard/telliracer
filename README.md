# telliracer
Am 31. August 2024 wird das Tellihochhaus erleuchtet. Auf zwei Hometrainer kann man die Lichter in den Büros der kantonalen Verwaltung ansteuern. spektakulärer Schabernack:)
Allows to play a race game on a set of home trainers initially on the tellitowers in aarau.

<img src="https://github.com/user-attachments/assets/cb14113e-45d7-4f5d-a53e-ed9c31c6189a" width="50%">

![hometrainer](https://github.com/user-attachments/assets/a8e60afb-b0a5-477f-80c8-f8f5abd2c3c9)


the game (raceer.py) goes like this:

```
[Start] 
    |
    v
[Initialize Players]
    |
    v
[MQTT Setup]
    |
    v
[Run Race Loop]   <-------------------------------
    |                            
    v           
[Clear Event Queue]   
    |                            
    v                
[Wait for Start]  <--->  [Check Buzz Event?]
    |                             
    v                            
[Countdown 3s]               
    |                             
    v
[Race Execution]
    |                            
    v                   
[Calculate Positions] <---> [Race Continuation? pos < 100%]
    |                             |
    v                             v
[End Race]        <--->  [Check Buzz Event?]
    |                            
    v 
[Celebrate winner 30s]
    |                    
      ---->  Restart Race Loop ------------>
```


![telli racer drawio](https://github.com/user-attachments/assets/ba74f221-df28-4278-8a12-5d36fd9a0b26)
