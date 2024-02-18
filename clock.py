from machine import Pin, I2C, RTC
from oled import Write, GFX, SSD1306_I2C
from fonts import ubuntu_mono_15, ubuntu_mono_20
from ssd1306 import SSD1306_I2C
import framebuf, sys, utime, imgfile,wlan,api_caller,clock_config


# CONSTANTS
DAYS = ['MON','TUE','WED','THU','FRI','SAT','SUN']
MONTHS = ['ZERO_MONTH','JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
STOCKS = ['PLTR','IVV','SPCE','AMZN']
# OLED
i2c_dev = I2C(1,scl=Pin(27),sda=Pin(26))  # start I2C on I2C1 (GPIO 26/27)
oled = SSD1306_I2C(128, 64, i2c_dev) # oled controller
i2c_right = I2C(0,scl=Pin(21),sda=Pin(20))
oled_right = SSD1306_I2C(128, 64, i2c_right)

# TIME
rtc=machine.RTC()
digit_1,digit_2,digit_3,digit_4 = 0,0,0,0


#big fonts
write20 = Write(oled, ubuntu_mono_20)
write20_right = Write(oled_right, ubuntu_mono_20)
write15_right = Write(oled_right, ubuntu_mono_15)

def bit_numbers(number):
    buffer,img_res = imgfile.get_img(number) # get the image byte array
    fb = framebuf.FrameBuffer(buffer, img_res[0], img_res[1], framebuf.MONO_HMSB) # MONO_HLSB, MONO_VLSB, MONO_HMSB
    return fb
def init():
    try:
        print('trying')
        f = open('raw.txt', 'r')
        wifi_name = f.readline().strip()
        wifi_pass = f.readline().strip()
        weather_c = f.readline().strip()
        stock_tic = f.readline().split(' ')
        print(f'Got file{wifi_name}, {wifi_pass}, {weather_c}')
        wlan.connect_WLAN(wifi_name, wifi_pass)
        rtc.datetime(api_caller.get_time())
    except:
        print('Failed to get config file')
        clock_config.get_init()
def main():
    init()
    temp, low_temp, high_temp, weather = api_caller.get_weather()
    stock_name, stock_price = api_caller.get_stock(STOCKS[0])
    weather_reload = False
    stock_reload = False
    stock_count = 1
    while True:
        ## Showing running time with blinking colon indicating seconds
        try:
            # Clears the OLED
            oled.fill(0)
            oled_right.fill(0)
            # TIME
            timestamp=rtc.datetime()
            # Weather
            if timestamp[5]%15==0 and weather_reload is True:
                temp, low_temp, high_temp, weather = api_caller.get_weather()
                weather_reload = False
            if (timestamp[5]-1)%15==0:
                weather_reload = True
            # Stocks
            if timestamp[6]%15==0 and stock_reload is True:
                stock_name, stock_price = api_caller.get_stock(STOCKS[stock_count])
                print(timestamp)
                stock_count+=1
                stock_reload = False
            if (timestamp[6]-1)%15==0:
                if len(STOCKS) <= stock_count:
                    stock_count=0
                stock_reload = True
                
            # 12h Clock
            hour = timestamp[4]
            if hour > 12:
                hour -=12

            oled.blit(bit_numbers(int(hour/10)), -5, 19, (1 if hour<10 else 0)) # show the image at location (x=0,y=0)
            oled.blit(bit_numbers(hour%10), 25, 19) # show the image at location (x=0,y=0)
            oled.blit(bit_numbers(int(timestamp[5]/10)), 64, 19) # show the image at location (x=0,y=0)
            oled.blit(bit_numbers(timestamp[5]%10), 94, 19) # show the image at location (x=0,y=0)
            # CALENDER
            write20.text(DAYS[timestamp[3]], 0, 0, 1)
            write20.text(MONTHS[timestamp[1]], 50, 0, 1)
            write20.text(str("%02d"%(timestamp[2])), 105, 0, 1)

            #STOCKS
            write20_right.text(stock_name, 0, 0, 1)
            write20_right.text(stock_price, 49, 0, 1)
            # DIVIDING LINE
            oled_right.vline(63, 25, 35, 2)
            # INSIDE TEMPERATURE
            write20_right.text(weather, 0, 20, 1)
            write20_right.text(f"{low_temp}-{high_temp}", 0, 42, 1)
            oled_right.blit(bit_numbers(int(temp/10)), 64, 19) # show the image at location (x=0,y=0)
            oled_right.blit(bit_numbers(temp%10), 94, 19) # show the image at location (x=0,y=0)
            # SECOND indicator, flashes every second
            oled.fill_rect(60, 30, 5, 5, (timestamp[6]%2))
            oled.fill_rect(60, 50, 5, 5, (timestamp[6]%2))
            
            oled.show()
            oled_right.show()
        except:
            print('FAILED OLED')
            continue
            
if __name__ == "__main__":
    main()




