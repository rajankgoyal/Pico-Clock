import network
import machine
import socket

class Servo:
    def __init__(self, MIN_DUTY=300000, MAX_DUTY=2300000, pin=28, freq=50):
        self.pwm = machine.PWM(machine.Pin(pin))
        self.pwm.freq(freq)
        self.MIN_DUTY = MIN_DUTY
        self.MAX_DUTY = MAX_DUTY
        
    def rotateDeg(self, deg):
        if deg < -90:
            deg = -90
        elif deg > 90:
            deg = 90
        duty_ns = int(self.MAX_DUTY - (deg+90) * (self.MAX_DUTY-self.MIN_DUTY)/180)
        self.pwm.duty_ns(duty_ns)

servo = Servo()
    
ssid = 'PICOCLOCK'
password = 'picoclock'

ap = network.WLAN(network.AP_IF)
ap.config(essid=ssid, password=password)
ap.active(True)

while ap.active() == False:
  pass

print('Connection successful')
print(ap.ifconfig())

# Function to load in html page    
def get_html(html_name):
    with open(html_name, 'r') as file:
        html = file.read()
        
    return html

# HTTP server with socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('Listening on', addr)

# Listen for connections
while True:
    try:
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        # print('Content = %s' % str(request))
        request = str(request)
#         print('---------------- REQUEST --------')
#         print(request)
#         print('---------------- REQUEST --------')
#         print(len(request[index:index1]))
        index = request.find('text=')+5
        index1 = request.find('&text1=')
        
        if(len(request[index:index1])<64):
            f = open("configs.txt", "a")
            f.write(request[index:index1])
            index = request.find('text1=')+6
            index1 = request.find('&text2=')
            f.write(request[index:index1])
            index = request.find('text2=')+6
            index1 = request.find('&textarea=')
            f.write(request[index:index1])
            index = request.find('&textarea=')+10
            index1 = request.find('&submit=')

            strn = request[index:index1]
            substrings = strn.split('%2C')
            f.write(substrings)
            
#             f = open("demofile3.txt", "a")
#             f.write("Woops! I have deleted the content!")
            f.close()
            
        # Load html and replace with current data 
        response = get_html('clock.html')
#         try:
#             response = response.replace('slider_value', str(deg))
#             
#         except Exception as e:
#             response = response.replace('slider_value', '0')
#         
        conn.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        conn.send(response)
        conn.close()
    except OSError as e:
        conn.close()
        print('Connection closed')
