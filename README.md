# telliracer
[insta](https://www.instagram.com/stories/highlights/17916792884644910/?hl=en)

Am 31. August 2024 wurde das Tellihochhaus erleuchtet. Auf zwei Hometrainer konnte man die Lichter in den Büros der kantonalen Verwaltung ansteuern. spektakulärer Schabernack:).

Allows to play a race game on a set of home trainers initially on the tellitower in aarau.

<img src="https://github.com/user-attachments/assets/cb14113e-45d7-4f5d-a53e-ed9c31c6189a" width="50%">
<img src="https://github.com/user-attachments/assets/a8e60afb-b0a5-477f-80c8-f8f5abd2c3c9" width="10%">


the game (raceer.py) goes like this:

```
[Start] 
    |
    v
[MQTT Setup]
    |
    v
[Run Race Loop]   <-----------------------------------
    |                                                 |
    v           
[Clear Event Queue]   
    |                         
    v
[Play Wait sequence]   <----    
    |                       |          
    v                       |
<Buzz Button pressed?> -----
    |                             
    v                            
[Countdown 3s]               
    |                             
    v
[Race Execution] <------------------------------
    |                                           |
    v                                           |
<Position < 100% ?  OR  Buzz Button pressed?> --             
    |                            
    v      
[End Race] 
    |                            
    v 
[Celebrate winner 30s]                                ^
    |                                                 |
      ---->  Restart Race Loop -----------------------
```


![telli racer drawio](https://github.com/user-attachments/assets/ba74f221-df28-4278-8a12-5d36fd9a0b26)

![image](https://github.com/user-attachments/assets/02f99a55-94e9-41f4-8498-388bbba5af91)

