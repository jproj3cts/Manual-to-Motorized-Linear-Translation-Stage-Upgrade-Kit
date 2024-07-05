"""
Copyright (C) 02/10/2022 Joe kelly, 05/07/2024 Nat Mendelsohn
This file is part of the Manual-to-Motorized-Linear-Translation-Stage-Upgrade-Kit <https://github.com/jproj3cts/Manual-to-Motorized-Linear-Translation-Stage-Upgrade-Kit>.
Manual-to-Motorized-Linear-Translation-Stage-Upgrade-Kit is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
Manual-to-Motorized-Linear-Translation-Stage-Upgrade-Kit is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with Manual-to-Motorized-Linear-Translation-Stage-Upgrade-Kit.  If not, see <http://www.gnu.org/licenses/>.

This variant is for the use of gears rather than heat shrink and includes a correction due to changing directions losing contact with the spokes.
"""

# Define SSID and password for the access point.
ssid = "YOUR_NEWORKNAME_HERE"
password = "YOUR_PASSWORD_HERE"

# Settings for stepper motor ramp.
dmin=0.002
dstart=0.003
gradient=0.0001

from machine import Pin
from time import sleep
import socket
import network
import tinyweb


# Hardware.
p2 = Pin(6, Pin.OUT)
p3 = Pin(7, Pin.OUT)
p4 = Pin(9, Pin.OUT)
p5 = Pin(8, Pin.OUT)

ds = 0.01
grad = 0.0005
dmin = ds

def f_step(n,dmin=dmin, dstart=ds,gradient=grad):
    # 512 is one rotation.
    # dmin defines shortest time between motor steps, dstart is intial time between steps as well as the end time, and gradient defines the linear ramp up and down between these values.
    ramp_up = True
    ramp_down = False
    #open tracking textfile to find out current position
    f = open('track.txt')
    pos = int(f.read())
    f.close()
    new_pos = pos+n
    #read previous direction
    f2 = open('direction.txt')
    d = f2.read()
    f2.close()
    if d == 'f':
        pass
    elif d == 'b':
        #add 20 steps (steps between spokes) to correct
        n+=20
        #change textfile to reflect new direction
        f2 = open("direction.txt", "w")
        f2.write('f')
        f2.close()
        
    else:
        print('Error; previous direction not identified')
#     #print(new_pos)
    if new_pos <=24576:
        for i in range(n):
            # Check if ramp down required to reach starting speed with number of steps left.
            if (n-i)*gradient + dmin <= dstart:
                ramp_down = True
                ramp_up = False
                ioffset = i
            # Ramp up logic.
            if ramp_up == True:
                dt = dstart - gradient*i
                # Check if min step time (max speed) reached, finishing ramp up
                if dt <= dmin:
                    ramp_up = False
            # Ramp down logic.
            elif ramp_down == True:
                dt = dmin + gradient*(i-ioffset)
            else:
                dt = dmin

            sleep(dt)
            p2.on()
            p3.off()
            p4.off()
            p5.off()
            
            sleep(dt)
            p2.off()
            p3.on()
            p4.off()
            p5.off()

            sleep(dt)
            p2.off()
            p3.off()
            p4.on()
            p5.off()
            
            sleep(dt)
            p2.off()
            p3.off()
            p4.off()
            p5.on()
            
        sleep(dmin)
        p2.off()
        p3.off()
        p4.off()
        p5.off()
        #overwrite tracking textfile
        f = open("track.txt", "w")
        f.write(str(new_pos))
        f.close()
    else:
        print('error')
   
    
    
def b_step(n,dmin=dmin, dstart=ds,gradient=grad):
    #512 steps is one rotation
    # dmin defines shortest time between motor steps, dstart is intial time between steps as well as the end time, and gradient defines the linear ramp up and down between these values.
    #print('running')
    ramp_up = True
    ramp_down = False
    #open tracking textfile to find out current position
    f = open('track.txt')
    pos = int(f.read())
    f.close()
    new_pos = pos-n
    #read previous direction
    f2 = open('direction.txt')
    d = f2.read()
    f2.close()
    if d == 'b':
        pass
    elif d == 'f':
        #add 20 steps (steps between spokes) to correct
        n+=20
        #change textfile to reflect new direction
        f2 = open("direction.txt", "w")
        f2.write('b')
        f2.close()
    else:
        print('Error; previous direction not identified')
    if new_pos >=0:
        for i in range(n):
            # Check if ramp down required to reach starting speed with number of steps left.
            if (n-i)*gradient + dmin <= dstart:
                ramp_down = True
                ramp_up = False
                ioffset = i
            # Ramp up logic.
            if ramp_up == True:
                dt = dstart - gradient*i
                # Check if min step time (max speed) reached, finishing ramp up
                if dt <= dmin:
                    ramp_up = False
            # Ramp down logic.
            elif ramp_down == True:
                dt = dmin + gradient*(i-ioffset)
            else:
                dt = dmin

            sleep(dt)
            p2.off()
            p3.off()
            p4.off()
            p5.on()
            
            sleep(dt)
            p2.off()
            p3.off()
            p4.on()
            p5.off()
            
            sleep(dt)
            p2.off()
            p3.on()
            p4.off()
            p5.off()
            
            sleep(dt)
            p2.on()
            p3.off()
            p4.off()
            p5.off()
        
        sleep(dmin)
        p2.off()
        p3.off()
        p4.off()
        p5.off()
        #overwrite tracking textfile
        f = open("track.txt", "w")
        f.write(str(new_pos))
        f.close()
    else:
        print('error')


# The following HTML defines the webpage that is served.
html = """<!DOCTYPE html><html>
<head><meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body><center><h1>Stepper Motor Controller</h1></center><br><br>
<form><center>
<center> <label for="steps">Steps:</label><br> <input type="number" id="fname" name="steps" value="0"><br>
<br><br>
<br><br>
<p>512 steps is equal to 360 degrees; postive numbers are clockwise rotations and negative are anticlockwise rotations.<p></body></html>
</html>
"""

### Setting Up network Access point
ap = network.WLAN(network.AP_IF)
ap.config(essid=ssid, password=password)
ap.active(True)

# Wait until it is active.
while ap.active == False:
    pass

print("Access point active")
# Print out IP information.
print(ap.ifconfig())

# Start up a tiny web server
app = tinyweb.webserver()

@app.route('/')
async def index(request, response):
    # Start HTTP response with content-type text/html
    await response.start_html()
    # Send actual HTML page
    await response.send(html)
    
    print("Client connected")

    try:
        steps = int(request.query_string[6:])
    except:
        steps = 0
    if abs(steps) < 10241:
        if steps > 0:
            f_step(steps)
        elif steps < 0:
            b_step(abs(steps))

# Run the web server as the sole process
app.run(host="0.0.0.0", port=80)


