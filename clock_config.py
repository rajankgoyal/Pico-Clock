import network
import machine
import socket

# Function to load in html page    
def get_html(html_name):
    with open(html_name, 'r') as file:
        html = file.read()
    return html

# Function to write config data
def write_raw(raw):
    f = open('raw.txt', 'w')
    f.write(raw)
    f.close()
    
# Function to read config data
def read_raw():
    f = open('raw.txt', 'r', encoding='utf-8-sig')
    print(f.read())
def get_init():
    ssid = 'PICOCLOCK'
    password = 'picoclock'
    wifi_name = ''
    wifi_pass = ''
    weather_city = ''

    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password)
    ap.active(True)

    while ap.active() == False:
      pass

    print('Connection successful')
    print(ap.ifconfig())

    # HTTP server with socket
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

    s = socket.socket()
    s.bind(addr)
    s.listen(1)

    print('Listening on', addr)

    # Listen for connections
    while True:

        try:
            #Getting Connetion setup
            conn, addr = s.accept()
            print('Got a connection from %s' % str(addr))
            request = conn.recv(1024)
            request = str(request)
            # Getting part of Wifiname from the form
            index = request.find('text=')+5
            index1 = request.find('&text1=')
            # checking the length of returned data Wifi name
            if(len(request[index:index1])<64):
                
                wifi_name = request[index:index1]
                # Getting Wifi password
                index = request.find('text1=')+6
                index1 = request.find('&text2=')
                wifi_pass = request[index:index1]
                # Getting Weather City
                index = request.find('text2=')+6
                index1 = request.find('&textarea=')
                weather_city = request[index:index1]
                # Getting Stock tickers
                index = request.find('&textarea=')+10
                index1 = request.find('&submit=')
                stocks = request[index:index1]
                # Separating out the stock tickers
                stock_tickers = ' '.join(stocks.split('%2C'))
                # writing to the file
                write_raw(f'{wifi_name}\n{wifi_pass}\n{weather_city}\n{stock_tickers}')
                
            # Load html and replace with current data 
            response = get_html('clock.html')
            try:
                f = open('raw.txt', 'r', encoding='utf-8-sig')
                wifi_name_f = f.readline().strip()
                wifi_pass_f = f.readline().strip()
                weather_city_f = f.readline().strip()
                stock_tickers_f = f.readline().strip()
                response = response.replace('wifiname_value', str(wifi_name_f))
                response = response.replace('wifipass_value', str(wifi_pass_f))
                response = response.replace('weather_value', str(','.join(weather_city_f.split('%2C'))))
                response = response.replace('stock_value', str(','.join(stock_tickers_f.split(' '))))
                print(wifi_name_f)
                
            except Exception as e:
                print (e)
                response = response.replace('slider_value', '0')
                print('error showing wifi name')
            conn.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            conn.send(response)
            conn.close()
        except OSError as e:
            conn.close()
            print('Connection closed')

get_init()