from machine import Pin, I2C, RTC
from oled import Write, GFX, SSD1306_I2C
from oled.fonts import ubuntu_mono_15, ubuntu_mono_20, bookerly_20
from ssd1306 import SSD1306_I2C
import framebuf, sys, utime, imgfile,wlan,api_caller


# CONSTANTS
DAYS = ['MON','TUE','WED','THU','FRI','SAT','SUN']
MONTHS = ['ZERO_MONTH','JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']

# OLED
i2c_dev = I2C(1,scl=Pin(27),sda=Pin(26),freq=200000)  # start I2C on I2C1 (GPIO 26/27)
oled = SSD1306_I2C(128, 64, i2c_dev) # oled controller
i2c_right = I2C(0,scl=Pin(21),sda=Pin(20),freq=200000)
oled_right = SSD1306_I2C(128, 64, i2c_right)

# TIME
rtc=machine.RTC()
digit_1,digit_2,digit_3,digit_4 = 0,0,0,0


#big fonts
write20 = Write(oled, ubuntu_mono_20)
write20_right = Write(oled_right, ubuntu_mono_20)


def bit_numbers(number):
    buffer,img_res = imgfile.get_img(number) # get the image byte array
    fb = framebuf.FrameBuffer(buffer, img_res[0], img_res[1], framebuf.MONO_HMSB) # MONO_HLSB, MONO_VLSB, MONO_HMSB
    return fb
def init():
    wlan.connect_WLAN('NWRKTEST', 'FASTCARS1')
    rtc.datetime(api_caller.get_time())
    

def main():
    init()
    temp, weather = api_caller.get_weather()
    weather_reload = False
    ## Showing running time with blinking colon indicating seconds
    while True:
        # Clears the OLED
        oled.fill(0)
        oled_right.fill(0)
        # TIME
        timestamp=rtc.datetime()
        # Weather
        if timestamp[5]%15==0 and weather_reload is True:
            temp, weather = api_caller.get_weather()
            weather_reload = False
        if (timestamp[5]-1)%15==0:
            weather_reload = True

        digit_1 = int(timestamp[4]/10)
        digit_2 = timestamp[4]%10
        digit_3 = int(timestamp[5]/10)
        digit_4 = timestamp[5]%10
        oled.blit(bit_numbers(digit_1), -5, 19) # show the image at location (x=0,y=0)
        oled.blit(bit_numbers(digit_2), 25, 19) # show the image at location (x=0,y=0)
        oled.blit(bit_numbers(digit_3), 64, 19) # show the image at location (x=0,y=0)
        oled.blit(bit_numbers(digit_4), 94, 19) # show the image at location (x=0,y=0)
        # CALENDER
        write20.text(MONTHS[timestamp[1]], 50, 0, 1)
        write20.text(str("%02d"%(timestamp[2])), 105, 0, 1)
        write20.text(DAYS[timestamp[3]], 0, 0, 1)
        #STOCKS
        write20_right.text("PLTR", 0, 0, 1)
        write20_right.text('47.45', 75, 0, 1)
        # DIVIDING LINE
        oled_right.vline(63, 25, 35, 2)
        # INSIDE TEMPERATURE
        write20_right.text(weather, 0, 30, 1)
        oled_right.blit(bit_numbers(int(temp/10)), 64, 19) # show the image at location (x=0,y=0)
        oled_right.blit(bit_numbers(temp%10), 94, 19) # show the image at location (x=0,y=0)
#         if timestamp[5]%5==0 and timestamp[6] == 0:
#             print('Weather will work just fine')
#         print(timestamp[5])
#         print(timestamp[6])
#         print('----------')
        for second in range(2):
            oled.fill_rect(60, 30, 5, 5, second)
            oled.fill_rect(60, 50, 5, 5, second)
            try:
                oled.show()
                oled_right.show()
            except:
                continue
            utime.sleep(1)
            
            
if __name__ == "__main__":
    main()