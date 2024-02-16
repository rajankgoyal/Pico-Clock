import urequests
def get_time():
    # Make an API call
    try:
        response = urequests.get(url='https://worldtimeapi.org/api/timezone/est')
    except Exception as e:
        print('failed to get time')

    data = response.json()
    datetime=data['datetime']
    day_of_week= data['day_of_week']

    x = datetime.split('T')
    date = x[0].split('-')
    timestamp = x[1].split('.')
    time = timestamp[0].split(':')
    print('Time API was called')
    return((int(date[0]),int(date[1]),int(date[2]),int(day_of_week-1),int(time[0]),int(time[1]),int(time[2]),0))

def get_weather():
    # Make an API call
    try:
        response = urequests.get(url='https://api.openweathermap.org/data/2.5/weather?q=Leesburg,us&APPID=8962d5f34baf517175534828154b554f&units=imperial')
    except Exception as e:
        print('failed to get weather')

    data = response.json()
    print('Weather API was called')
    return(int(data['main']['temp']), int(data['main']['temp_min']), int(data['main']['temp_max']), data['weather'][0]['main'])

def get_stock(ticker):
    # Make an API call
    try:
        response = urequests.get(f'https://finnhub.io/api/v1/quote?symbol={ticker}&token=cn3evr1r01qtdiesh270cn3evr1r01qtdiesh27g')
    except Exception as e:
        print('failed to get stock info')
    data = response.json()
    print('Stock API was called')
    return(ticker,str( "%0.2f" % data['c']))
        
        
        
