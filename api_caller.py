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
    return((int(date[0]),int(date[1]),int(date[2]),int(day_of_week-1),int(time[0]),int(time[1]),int(time[2]),0))

def get_weather():
    # Make an API call
    try:
        response = urequests.get(url='https://api.openweathermap.org/data/2.5/weather?q=Loudoun%20County,us&APPID=8962d5f34baf517175534828154b554f&&units=imperial')
    except Exception as e:
        print('failed to get weather')

    data = response.json()
    return(data['main']['temp'], data['weather'][0]['main'])

